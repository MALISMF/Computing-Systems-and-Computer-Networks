N = int(input("Кол-во вершин: "))
# Создаем списки соседей
graph = [[] for _ in range(N + 1)]

print("Рёбра (пустая строка - конец):")
while True:
    line = input()
    if line == "":
        break
    u, v = map(int, line.split())
    graph[u].append(v)
    graph[v].append(u)

# Сортируем списки соседей
for u in range(1, N+1):
    graph[u].sort()
    
visited = [False] * (N + 1)
islands = 0  

def dfs(u):
    visited[u] = True
    for v in graph[u]:
        if not visited[v]:
            dfs(v)
            
# Запускаем DFS из каждой непосещённой вершины
for start_v in range(1, N + 1):
    if not visited[start_v]:
        dfs(start_v)
        islands += 1

nodes = islands - 1 #Количество рёбер для связности графа (кол-во островков - 1)

print(f"Кол-во ребер для связности графа: {nodes}")
