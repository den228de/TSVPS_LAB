"""
Модуль для поиска клик в графе
Конвертировано из C++ версии
"""

import random
from itertools import combinations
from typing import List, Tuple


class Graph:
    """Класс для представления графа через матрицу смежности"""
    
    def __init__(self, num_vertices: int, num_edges: int):
        """
        Инициализация графа
        
        Args:
            num_vertices: количество вершин
            num_edges: количество рёбер
        """
        self.num_vertices = num_vertices
        self.adjacency_matrix = [[0] * num_vertices for _ in range(num_vertices)]
        self._generate_random_edges(num_edges)
    
    def _generate_random_edges(self, num_edges: int):
        """Генерация случайных рёбер в графе"""
        max_edges = self.num_vertices * (self.num_vertices - 1) // 2
        num_edges = min(num_edges, max_edges)
        
        # Создаём список всех возможных пар вершин
        all_pairs = []
        for i in range(self.num_vertices):
            for j in range(i + 1, self.num_vertices):
                all_pairs.append((i, j))
        
        # Перемешиваем и выбираем нужное количество рёбер
        random.shuffle(all_pairs)
        for i in range(num_edges):
            u, v = all_pairs[i]
            self.adjacency_matrix[u][v] = 1
            self.adjacency_matrix[v][u] = 1
    
    def has_edge(self, u: int, v: int) -> bool:
        """Проверка наличия ребра между вершинами u и v"""
        return self.adjacency_matrix[u][v] == 1
    
    def get_matrix_string(self) -> str:
        """Получение строкового представления матрицы смежности"""
        result = []
        for row in self.adjacency_matrix:
            result.append(' '.join(map(str, row)))
        return '\n'.join(result)


def is_clique(adjacency_matrix: List[List[int]], vertices: List[int]) -> bool:
    """
    Проверка, является ли подмножество вершин кликой
    
    Клика - это подмножество вершин, в котором каждая пара вершин соединена ребром
    
    Args:
        adjacency_matrix: матрица смежности графа
        vertices: список вершин для проверки
    
    Returns:
        True если vertices образуют клику, False иначе
    """
    n = len(vertices)
    if n <= 1:
        return True
    
    # Проверяем все пары вершин
    for i in range(n):
        for j in range(i + 1, n):
            u = vertices[i]
            v = vertices[j]
            # Если между вершинами нет ребра - это не клика
            if adjacency_matrix[u][v] == 0:
                return False
    
    return True


def find_clique_greater_than_b(adjacency_matrix: List[List[int]], b: int) -> List[int]:
    """
    Поиск клики размером больше B
    
    Алгоритм перебирает все возможные комбинации вершин размером от B+1 до n,
    и возвращает первую найденную клику минимального размера больше B
    
    Args:
        adjacency_matrix: матрица смежности графа
        b: минимальный размер клики
    
    Returns:
        Список вершин клики или пустой список, если клика не найдена
    """
    num_vertices = len(adjacency_matrix)
    
    # Перебираем размеры клики от B+1 до количества вершин
    for k in range(b + 1, num_vertices + 1):
        # Генерируем все комбинации из k вершин
        for combo in combinations(range(num_vertices), k):
            combo_list = list(combo)
            # Проверяем, является ли комбинация кликой
            if is_clique(adjacency_matrix, combo_list):
                return combo_list
    
    return []


def find_max_clique(adjacency_matrix: List[List[int]], callback=None) -> List[int]:
    """
    Поиск максимальной клики в графе с выводом процесса
    
    Алгоритм использует обратный перебор - начинает с максимального возможного размера
    и уменьшает его, пока не найдёт клику. Это оптимизация, так как мы ищем
    максимальную клику.
    
    Args:
        adjacency_matrix: матрица смежности графа
        callback: функция обратного вызова для вывода процесса (опционально)
    
    Returns:
        Список вершин максимальной клики
    """
    num_vertices = len(adjacency_matrix)
    max_clique = []
    
    # Перебираем размеры от максимального к минимальному
    for k in range(num_vertices, 0, -1):
        combo_count = 0
        
        if callback:
            callback(f"\nn={num_vertices}, k={k}, все комбинации №{num_vertices - k + 1}:\n")
        
        # Генерируем все комбинации из k вершин
        for combo in combinations(range(num_vertices), k):
            combo_count += 1
            combo_list = list(combo)
            
            # Формируем строку для вывода комбинации
            combo_str = "{"
            for i in range(len(combo_list)):
                if i + 1 < len(combo_list) and adjacency_matrix[combo_list[i]][combo_list[i + 1]] == 1:
                    combo_str += f"{combo_list[i]} - "
                else:
                    combo_str += f"{combo_list[i]}" + (", " if i < len(combo_list) - 1 else "")
            combo_str += "}"
            
            output = f"{combo_str}, №{combo_count}"
            
            # Проверяем, является ли комбинация кликой
            if is_clique(adjacency_matrix, combo_list):
                output += "     - клика"
                if len(combo_list) > len(max_clique):
                    max_clique = combo_list
                    output += " - максимальная клика"
                    if callback:
                        callback(output + "\n")
                    # Нашли максимальную клику, можно выходить
                    return max_clique
            
            if callback:
                callback(output + "\n")
    
    return max_clique


def generate_ascii_graph(adjacency_matrix: List[List[int]], 
                        clique_b: List[int], 
                        max_clique: List[int],
                        width: int = 90, 
                        height: int = 60) -> str:
    """
    Генерация ASCII визуализации графа
    
    Вершины располагаются по кругу. Используются разные символы:
    - 'o' - обычная вершина
    - '*' - вершина из клики B
    - '#' - вершина из максимальной клики
    
    Args:
        adjacency_matrix: матрица смежности графа
        clique_b: вершины клики размером больше B
        max_clique: вершины максимальной клики
        width: ширина поля для рисования
        height: высота поля для рисования
    
    Returns:
        Строка с ASCII представлением графа
    """
    import math
    
    num_vertices = len(adjacency_matrix)
    center_x = width // 2
    center_y = height // 2
    radius = min(center_x, center_y) * 0.8
    
    # Вычисляем позиции вершин по кругу
    positions = []
    for i in range(num_vertices):
        angle = 2.0 * math.pi * i / num_vertices
        x = int(center_x + radius * math.cos(angle))
        y = int(center_y + radius * math.sin(angle))
        positions.append((x, y))
    
    # Создаём пустое поле
    screen = [[' ' for _ in range(width)] for _ in range(height)]
    
    # Отмечаем вершины из клик
    is_clique_b_vertex = [False] * num_vertices
    for v in clique_b:
        if 0 <= v < num_vertices:
            is_clique_b_vertex[v] = True
    
    is_max_clique_vertex = [False] * num_vertices
    for v in max_clique:
        if 0 <= v < num_vertices:
            is_max_clique_vertex[v] = True
    
    # Рисуем рёбра (линии между вершинами)
    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):
            if adjacency_matrix[i][j] == 1:
                x1, y1 = positions[i]
                x2, y2 = positions[j]
                
                # Алгоритм Брезенхема для рисования линии
                dx = abs(x2 - x1)
                dy = abs(y2 - y1)
                sx = 1 if x1 < x2 else -1
                sy = 1 if y1 < y2 else -1
                err = dx - dy
                
                x, y = x1, y1
                while True:
                    if 0 <= x < width and 0 <= y < height and screen[y][x] == ' ':
                        screen[y][x] = '-'
                    
                    if x == x2 and y == y2:
                        break
                    
                    e2 = 2 * err
                    if e2 > -dy:
                        err -= dy
                        x += sx
                    if e2 < dx:
                        err += dx
                        y += sy
    
    # Рисуем вершины (поверх рёбер)
    for i in range(num_vertices):
        x, y = positions[i]
        if 0 <= x < width and 0 <= y < height:
            # Выбираем символ в зависимости от типа вершины
            if is_max_clique_vertex[i]:
                vertex_char = '#'
            elif is_clique_b_vertex[i]:
                vertex_char = '*'
            else:
                vertex_char = 'o'
            
            screen[y][x] = vertex_char
            
            # Добавляем номер вершины
            id_str = str(i)
            if x + 1 < width:
                screen[y][x + 1] = id_str[0]
            if len(id_str) > 1 and x + 2 < width:
                screen[y][x + 2] = id_str[1]
    
    # Преобразуем в строку
    result = []
    for row in screen:
        result.append(''.join(row))
    
    return '\n'.join(result)


if __name__ == "__main__":
    # Пример использования
    random.seed()
    
    print("Введите количество вершин: ", end="")
    num_vertices = int(input())
    
    max_edges = num_vertices * (num_vertices - 1) // 2
    print(f"Введите количество соединений (максимум {max_edges}): ", end="")
    num_edges = int(input())
    
    # Создаём граф
    graph = Graph(num_vertices, num_edges)
    
    print("\nМатрица смежности:")
    print(graph.get_matrix_string())
    
    print("\nВведите значение B: ", end="")
    b = int(input())
    
    # Ищем клику больше B
    clique_b = find_clique_greater_than_b(graph.adjacency_matrix, b)
    if clique_b:
        print(f"\nВ графе существует клика больше, чем {b}.")
        print(f"Вершины этой клики: {', '.join(map(str, clique_b))}")
    else:
        print(f"\nВ графе не существует клики больше, чем {b}.")
    
    # Ищем максимальную клику
    print("\nПоиск максимальной клики:")
    max_clique = find_max_clique(graph.adjacency_matrix, callback=print)
    
    print(f"\nМаксимальная клика в графе")
    print(f"Размер клики: {len(max_clique)}")
    print(f"Вершины клики: {', '.join(map(str, max_clique))}")
    
    # Визуализация
    print("\nВизуализация графа:")
    print(generate_ascii_graph(graph.adjacency_matrix, clique_b, max_clique))
