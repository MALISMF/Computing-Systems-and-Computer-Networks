import networkx as nx


def calculate_vertex_degrees(input_file, output_file):

    G = nx.Graph()
    
    with open(input_file, 'r') as f:

        first_line = f.readline().strip().split()
        N = int(first_line[0])  # число вершин
        E = int(first_line[1])  # число рёбер
        
        # Читаем рёбра и добавляем их в граф
        for _ in range(E):
            line = f.readline().strip().split()
            u = int(line[0])
            v = int(line[1])
            G.add_edge(u, v)

    # Выводим степени вершин от 1 до N
    degrees = [G.degree(i) for i in range(1, N + 1)]
    
    # Записываем результаты в выходной файл
    with open(output_file, 'w') as f:
        result = [str(d) for d in degrees]
        f.write(' '.join(result))
        print(' '.join(result))


if __name__ == '__main__':
    calculate_vertex_degrees('degree_dataset_1000_vertices.txt.txt', 'output.txt')

