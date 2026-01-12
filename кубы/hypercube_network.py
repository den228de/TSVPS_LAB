"""
Модуль для работы с сетью гиперкубов.
Реализует классы SingleHypercube и MultiCubeNetwork для симуляции
топологии гиперкубов и поиска кратчайших путей между процессорами.
"""

from collections import deque
from typing import List, Tuple, Optional


class SingleHypercube:
    """
    Класс для представления одного гиперкуба.
    
    Гиперкуб размерности n содержит 2^n процессоров, где каждый процессор
    соединен с n соседями (по одному на каждое измерение).
    """
    
    def __init__(self, dimension: int):
        """
        Инициализация гиперкуба.
        
        Args:
            dimension: Размерность гиперкуба (количество измерений)
        """
        self.dimension = dimension
        self.total_processors = 2 ** dimension
        self.adjacency_matrix = [[0] * self.total_processors for _ in range(self.total_processors)]
        self._build_hypercube()
    
    def _build_hypercube(self):
        """
        Построение матрицы смежности гиперкуба.
        
        Два процессора соединены, если их бинарные представления
        отличаются ровно в одном бите.
        """
        for i in range(self.total_processors):
            for j in range(self.dimension):
                # XOR для инвертирования j-го бита
                neighbor = i ^ (1 << j)
                # Устанавливаем связь (неориентированный граф)
                self.adjacency_matrix[i][neighbor] = 1
                self.adjacency_matrix[neighbor][i] = 1
    
    def get_binary_representation(self, processor_id: int) -> str:
        """
        Получить бинарное представление процессора.
        
        Args:
            processor_id: ID процессора
            
        Returns:
            Бинарное представление в виде строки
        """
        return format(processor_id, f'0{self.dimension}b')
    
    def get_neighbors(self, processor_id: int) -> List[int]:
        """
        Получить список соседей процессора внутри куба.
        
        Args:
            processor_id: ID процессора
            
        Returns:
            Список ID соседних процессоров
        """
        neighbors = []
        for neighbor_id in range(self.total_processors):
            if self.adjacency_matrix[processor_id][neighbor_id]:
                neighbors.append(neighbor_id)
        return neighbors


class MultiCubeNetwork:
    """
    Класс для представления сети из нескольких гиперкубов,
    соединенных в кольцевую топологию.
    """
    
    def __init__(self, num_cubes: int, dimension_per_cube: int):
        """
        Инициализация сети гиперкубов.
        
        Args:
            num_cubes: Количество гиперкубов в сети
            dimension_per_cube: Размерность каждого гиперкуба
        """
        self.num_cubes = num_cubes
        self.dimension_per_cube = dimension_per_cube
        self.processors_per_cube = 2 ** dimension_per_cube
        self.total_processors = num_cubes * self.processors_per_cube
        
        # Создаем отдельные гиперкубы
        self.cubes = [SingleHypercube(dimension_per_cube) for _ in range(num_cubes)]
        
        # Создаем объединенную матрицу смежности
        self.combined_adjacency_matrix = [[0] * self.total_processors for _ in range(self.total_processors)]
        self._build_combined_topology()
    
    def _build_combined_topology(self):
        """
        Построение объединенной топологии сети.
        
        1. Копируем связи внутри каждого куба
        2. Соединяем соответствующие вершины соседних кубов (кольцо)
        """
        # Копируем связи внутри каждого куба
        for cube_id in range(self.num_cubes):
            adj_matrix = self.cubes[cube_id].adjacency_matrix
            for proc_in_cube in range(self.processors_per_cube):
                for neighbor_in_cube in range(self.processors_per_cube):
                    if adj_matrix[proc_in_cube][neighbor_in_cube]:
                        global_proc1 = self._encode_address(cube_id, proc_in_cube)
                        global_proc2 = self._encode_address(cube_id, neighbor_in_cube)
                        self.combined_adjacency_matrix[global_proc1][global_proc2] = 1
                        self.combined_adjacency_matrix[global_proc2][global_proc1] = 1
        
        # Соединяем соответствующие вершины соседних кубов (кольцо)
        for cube_id in range(self.num_cubes):
            next_cube_id = (cube_id + 1) % self.num_cubes
            for proc_in_cube in range(self.processors_per_cube):
                global_proc_current = self._encode_address(cube_id, proc_in_cube)
                global_proc_next = self._encode_address(next_cube_id, proc_in_cube)
                self.combined_adjacency_matrix[global_proc_current][global_proc_next] = 1
                self.combined_adjacency_matrix[global_proc_next][global_proc_current] = 1
    
    def _encode_address(self, cube_id: int, processor_id_within_cube: int) -> int:
        """
        Кодирование адреса процессора в глобальный ID.
        
        Args:
            cube_id: ID куба
            processor_id_within_cube: ID процессора внутри куба
            
        Returns:
            Глобальный ID процессора
        """
        return cube_id * self.processors_per_cube + processor_id_within_cube
    
    def _decode_address(self, global_id: int) -> Tuple[int, int]:
        """
        Декодирование глобального ID в адрес процессора.
        
        Args:
            global_id: Глобальный ID процессора
            
        Returns:
            Кортеж (cube_id, processor_id_within_cube)
        """
        processor_id_within_cube = global_id % self.processors_per_cube
        cube_id = global_id // self.processors_per_cube
        return cube_id, processor_id_within_cube
    
    def find_shortest_path(self, source: int, destination: int) -> List[int]:
        """
        Поиск кратчайшего пути между двумя процессорами методом BFS.
        
        Args:
            source: Глобальный ID исходного процессора
            destination: Глобальный ID конечного процессора
            
        Returns:
            Список глобальных ID процессоров в пути (от source до destination)
        """
        if source == destination:
            return [source]
        
        # BFS
        queue = deque([source])
        parent = {source: None}
        visited = {source}
        
        found = False
        while queue and not found:
            current = queue.popleft()
            
            if current == destination:
                found = True
                break
            
            # Проверяем всех соседей
            for neighbor in range(self.total_processors):
                if self.combined_adjacency_matrix[current][neighbor] and neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current
                    queue.append(neighbor)
        
        # Восстанавливаем путь
        if not found:
            return []
        
        path = []
        current = destination
        while current is not None:
            path.append(current)
            current = parent[current]
        
        path.reverse()
        return path
    
    def format_processor_info(self, global_id: int) -> str:
        """
        Форматирование информации о процессоре.
        
        Args:
            global_id: Глобальный ID процессора
            
        Returns:
            Строка с информацией о процессоре
        """
        cube_id, proc_id = self._decode_address(global_id)
        binary_repr = self.cubes[cube_id].get_binary_representation(proc_id)
        return f"Глобально {global_id} (Куб {cube_id}, Процессор {proc_id}, ID: {binary_repr})"
    
    def get_topology_info(self) -> str:
        """
        Получить информацию о топологии сети.
        
        Returns:
            Строка с описанием топологии
        """
        info = []
        info.append("=" * 60)
        info.append("ТОПОЛОГИЯ СЕТИ ГИПЕРКУБОВ")
        info.append("=" * 60)
        info.append(f"Количество кубов: {self.num_cubes}")
        info.append(f"Размерность каждого куба: {self.dimension_per_cube}")
        info.append(f"Процессоров в каждом кубе: {self.processors_per_cube}")
        info.append(f"Общее количество процессоров: {self.total_processors}")
        info.append("=" * 60)
        info.append("")
        
        # Информация о каждом процессоре и его соседях
        for global_id in range(self.total_processors):
            cube_id, proc_id = self._decode_address(global_id)
            binary_repr = self.cubes[cube_id].get_binary_representation(proc_id)
            
            line = f"Процессор {global_id:3d} (Куб {cube_id}, ID: {binary_repr}) -> Соседи: "
            
            neighbors = []
            for neighbor_id in range(self.total_processors):
                if self.combined_adjacency_matrix[global_id][neighbor_id]:
                    neighbor_cube_id, neighbor_proc_id = self._decode_address(neighbor_id)
                    neighbors.append(f"{neighbor_id} (Куб {neighbor_cube_id})")
            
            line += ", ".join(neighbors)
            info.append(line)
        
        info.append("=" * 60)
        return "\n".join(info)
