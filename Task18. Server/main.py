import random
import secrets
from typing import Dict, List, Optional, Set

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel, Field


# ---------- Data models ----------
class RegisterRequest(BaseModel):
    nickname: str
    password: str


class TokenRequest(BaseModel):
    accessToken: str = Field(alias="accessToken")


class CreateRoomRequest(TokenRequest):
    pass


class EnterRoomRequest(TokenRequest):
    gameId: int


class PickRequest(TokenRequest):
    cards: List[int]


class GameRoom:
    def __init__(self, game_id: int):
        self.id = game_id
        self.deck = self._generate_deck()
        random.shuffle(self.deck)
        self.field: List[int] = []
        self.scores: Dict[str, int] = {}
        self.players: Set[str] = set()
        self.websockets: Set[WebSocket] = set()
        self._deal_initial()

    @staticmethod
    def _generate_deck() -> List[int]:

        return list(range(81))

    @staticmethod
    def card_to_props(card_id: int) -> Dict[str, int]:

        props = []
        value = card_id
        for _ in range(4):
            props.append(value % 3 + 1)
            value //= 3
        color, shape, fill, count = props  
        return {
            "id": card_id,
            "color": color,
            "shape": shape,
            "fill": fill,
            "count": count,
        }

    @staticmethod
    def _is_set(cards: List[int]) -> bool:
        if len(cards) != 3:
            return False

        props = [GameRoom.card_to_props(c) for c in cards]
        keys = ["color", "shape", "fill", "count"]
        for key in keys:
            values = {p[key] for p in props}
            if len(values) not in (1, 3):
                return False
        return True

    def _deal_initial(self) -> None:
        while len(self.field) < 12 and self.deck:
            self.field.append(self.deck.pop())

    def add_player(self, nickname: str) -> None:
        self.players.add(nickname)
        self.scores.setdefault(nickname, 0)

    def add_cards(self, amount: int = 3) -> None:
        for _ in range(amount):
            if self.deck:
                self.field.append(self.deck.pop())

    def pick(self, nickname: str, cards: List[int]) -> Dict[str, int]:
        if not all(card in self.field for card in cards):
            return {"isSet": False, "score": self.scores.get(nickname, 0)}

        is_set = self._is_set(cards)
        if is_set:
            for card in cards:
                self.field.remove(card)
            self.add_cards(max(0, 12 - len(self.field)))
            self.scores[nickname] = self.scores.get(nickname, 0) + 1
        return {"isSet": is_set, "score": self.scores.get(nickname, 0)}

    def status(self) -> str:
        if self.deck or self._any_sets_on_field():
            return "ongoing"
        return "ended"

    def _any_sets_on_field(self) -> bool:
        cards = self.field
        n = len(cards)
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    if self._is_set([cards[i], cards[j], cards[k]]):
                        return True
        return False

    def field_state(self, nickname: str) -> Dict:
        return {
            "cards": [self.card_to_props(c) for c in self.field],
            "status": self.status(),
            "score": self.scores.get(nickname, 0),
        }


# ---------- Application ----------
app = FastAPI(title="Set Game Server")

users: Dict[str, Dict[str, str]] = {}
tokens: Dict[str, str] = {}
games: Dict[int, GameRoom] = {}
next_game_id = 0


# ---------- Helpers ----------
def get_nickname_by_token(token: str) -> str:
    nickname = tokens.get(token)
    if not nickname:
        raise HTTPException(status_code=401, detail="Invalid access token")
    return nickname


async def broadcast(game: GameRoom, payload: Dict) -> None:
    dead = []
    for ws in game.websockets:
        try:
            await ws.send_json(payload)
        except WebSocketDisconnect:
            dead.append(ws)
    for ws in dead:
        game.websockets.discard(ws)


# ---------- Routes ----------
@app.post("/user/register")
def register(body: RegisterRequest):
    if body.nickname in users:
        raise HTTPException(status_code=400, detail="Nickname already exists")
    token = secrets.token_urlsafe(8)
    users[body.nickname] = {"password": body.password, "token": token}
    tokens[token] = body.nickname
    return {"nickname": body.nickname, "accessToken": token}


@app.post("/set/room/create")
def create_room(body: CreateRoomRequest):
    global next_game_id
    nickname = get_nickname_by_token(body.accessToken)
    game = GameRoom(next_game_id)
    game.add_player(nickname)
    games[next_game_id] = game
    next_game_id += 1
    return {"success": True, "exception": None, "gameId": game.id}


@app.post("/set/room/list")
def list_rooms(body: TokenRequest):
    get_nickname_by_token(body.accessToken)
    return {"games": [{"id": gid} for gid in games.keys()]}


@app.post("/set/room/enter")
def enter_room(body: EnterRoomRequest):
    nickname = get_nickname_by_token(body.accessToken)
    game = games.get(body.gameId)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    game.add_player(nickname)
    return {"success": True, "exception": None, "gameId": game.id}


@app.post("/set/field")
def field(body: TokenRequest):
    nickname = get_nickname_by_token(body.accessToken)
    game = _find_player_game(nickname)
    if not game:
        raise HTTPException(status_code=400, detail="Player not in a game")
    return game.field_state(nickname)


@app.post("/set/pick")
async def pick(body: PickRequest):
    nickname = get_nickname_by_token(body.accessToken)
    game = _find_player_game(nickname)
    if not game:
        raise HTTPException(status_code=400, detail="Player not in a game")

    result = game.pick(nickname, body.cards)

    await broadcast(
        game,
        {
            "type": "field",
            "field": game.field_state(nickname),
            "scores": game.scores,
        },
    )
    return result


@app.post("/set/add")
async def add_cards(body: TokenRequest):
    nickname = get_nickname_by_token(body.accessToken)
    game = _find_player_game(nickname)
    if not game:
        raise HTTPException(status_code=400, detail="Player not in a game")
    game.add_cards()
    await broadcast(game, {"type": "field", "field": game.field_state(nickname)})
    return {"success": True, "exception": None}


@app.post("/set/scores")
def scores(body: TokenRequest):
    nickname = get_nickname_by_token(body.accessToken)
    game = _find_player_game(nickname)
    if not game:
        raise HTTPException(status_code=400, detail="Player not in a game")
    return {
        "success": True,
        "exception": None,
        "users": [{"name": name, "score": score} for name, score in game.scores.items()],
    }


@app.websocket("/set")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    try:
        token_msg = await ws.receive_json()
        token = token_msg.get("accessToken")
        nickname = get_nickname_by_token(token)
        game = _find_player_game(nickname)
        if not game:
            await ws.send_json({"success": False, "exception": {"message": "Join a game first"}})
            await ws.close()
            return
        game.websockets.add(ws)
        await ws.send_json({"success": True, "nickname": nickname, "gameId": game.id})
        await ws.send_json({"type": "field", "field": game.field_state(nickname), "scores": game.scores})
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        pass
    finally:
        for game in games.values():
            game.websockets.discard(ws)


# ---------- Utilities ----------
def _find_player_game(nickname: str) -> Optional[GameRoom]:
    for game in games.values():
        if nickname in game.players:
            return game
    return None


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

