import sys

def dfs_update(u, n, matrix, distances):
    current_dist = distances[u]
    
    for v in range(n):
        if matrix[u][v] == 1:
            if distances[v] > current_dist + 1:
                distances[v] = current_dist + 1
                dfs_update(v, n, matrix, distances)

def main():

    N = 6
    adj_matrix = [
        [0, 1, 1, 0, 0, 0],
        [1, 0, 0, 1, 0, 0],
        [1, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 1],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0]
    ]

    print("Вершины графа: 0(A), 1(B), 2(C), 3(D), 4(E), 5(F)")
    
    try:
        start_vertex_raw = int(input("Введите номер начальной вершины K (например, 0): "))
    except ValueError:
        print("Ошибка: введите целое число.")
        return

    if start_vertex_raw < 0 or start_vertex_raw >= N:
        print("Ошибка: такой вершины нет в графе.")
        return


    infinity = 1000000
    distances = [infinity] * N
    distances[start_vertex_raw] = 0


    dfs_update(start_vertex_raw, N, adj_matrix, distances)

    print("\nРезультат (Вершина Длина):")
    for i in range(N):
        vertex_name = chr(ord('A') + i)
        
        dist_out = distances[i]
        if dist_out == infinity:
            dist_out = "Недостижима"
            
        print(f"{vertex_name} {dist_out}")

if __name__ == "__main__":
    main()