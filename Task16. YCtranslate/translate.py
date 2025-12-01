import os
import requests
import json

INPUT_FILE = "input.txt"
FOLDER_ID = "b1gg308ep3p6nui9g8r0"
target_language = "ru"

def read_api_key(path: str) -> str:
    full_path = os.path.join(os.getcwd(), path)
    with open(full_path, encoding="utf-8") as f:
        return f.read().strip()

API_KEY = read_api_key("api_key.txt")

def read_texts(path: str) -> list[str]:
    full_path = os.path.join(os.getcwd(), path)
    with open(full_path, encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]
    return [line for line in lines if line]

def create_translated_txt(response: requests.Response):
    try:
        response.raise_for_status()
        data = response.json()
        translations = data.get("translations", [])
        translated_texts = [translation.get("text", "") for translation in translations]
        
        with open("translated.txt", "w", encoding="utf-8") as f:
            for text in translated_texts:
                f.write(text + "\n")
        
        print(f"Переведено {len(translated_texts)} строк. Результат сохранен в translated.txt")
    except requests.exceptions.HTTPError as e:
        print(f"Ошибка HTTP: {e}")
        print(f"Ответ сервера: {response.text}")
    except json.JSONDecodeError as e:
        print(f"Ошибка парсинга JSON: {e}")
        print(f"Ответ сервера: {response.text}")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")



def main():
    texts = read_texts(INPUT_FILE)

    if not texts:
        print("Файл с текстом пустой или содержит только пустые строки.")
        return

    body = {
        "targetLanguageCode": target_language,
        "texts": texts,
        "folderId": FOLDER_ID,
    }

    json_data = json.dumps(body, ensure_ascii=False).encode('utf-8')

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {API_KEY}",
    }

    response = requests.post(
        "https://translate.api.cloud.yandex.net/translate/v2/translate",
        data=json_data,
        headers=headers,
    )

    create_translated_txt(response)


if __name__ == "__main__":
    main()
