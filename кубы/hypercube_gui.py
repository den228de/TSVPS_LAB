"""
GUI приложение для симуляции сети гиперкубов.
Позволяет визуализировать топологию гиперкубов и находить кратчайшие пути.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
from hypercube_network import MultiCubeNetwork
import numpy as np


class HypercubeGUI:
    """Графический интерфейс для работы с сетью гиперкубов."""
    
    def __init__(self, root):
        """Инициализация GUI."""
        self.root = root
        self.root.title("Симуляция сети гиперкубов")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2b2b2b')
        
        self.network = None
        self.graph = None
        self.pos = None
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Создание виджетов интерфейса."""
        # Стиль
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TLabel', background='#2b2b2b', foreground='#00ff00', font=('Consolas', 10))
        style.configure('TButton', background='#3c3c3c', foreground='#00ff00', font=('Consolas', 10, 'bold'))
        style.configure('TEntry', fieldbackground='#1e1e1e', foreground='#00ff00', font=('Consolas', 10))
        style.configure('TRadiobutton', background='#2b2b2b', foreground='#00ff00', font=('Consolas', 10))
        
        # Заголовок
        title_label = tk.Label(
            self.root,
            text="СИМУЛЯЦИЯ СЕТИ ГИПЕРКУБОВ",
            font=('Consolas', 18, 'bold'),
            bg='#2b2b2b',
            fg='#00ff00'
        )
        title_label.pack(pady=10)
        
        # Основной контейнер
        main_container = tk.Frame(self.root, bg='#2b2b2b')
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Левая панель (настройки)
        left_panel = tk.Frame(main_container, bg='#2b2b2b', width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Правая панель (визуализация и результаты)
        right_panel = tk.Frame(main_container, bg='#2b2b2b')
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # === ЛЕВАЯ ПАНЕЛЬ ===
        
        # Выбор метода поиска
        method_frame = tk.LabelFrame(
            left_panel,
            text="Метод поиска",
            bg='#2b2b2b',
            fg='#00ff00',
            font=('Consolas', 10, 'bold')
        )
        method_frame.pack(fill=tk.X, pady=5)
        
        self.search_method = tk.IntVar(value=2)
        
        ttk.Radiobutton(
            method_frame,
            text="BFS (один куб)",
            variable=self.search_method,
            value=1,
            command=self._on_method_change
        ).pack(anchor=tk.W, padx=5, pady=2)
        
        ttk.Radiobutton(
            method_frame,
            text="BFS (несколько кубов)",
            variable=self.search_method,
            value=2,
            command=self._on_method_change
        ).pack(anchor=tk.W, padx=5, pady=2)
        
        # Параметры сети
        params_frame = tk.LabelFrame(
            left_panel,
            text="Параметры сети",
            bg='#2b2b2b',
            fg='#00ff00',
            font=('Consolas', 10, 'bold')
        )
        params_frame.pack(fill=tk.X, pady=5)
        
        # Размерность куба
        ttk.Label(params_frame, text="Размерность куба (1-10):").pack(anchor=tk.W, padx=5, pady=2)
        self.dimension_entry = ttk.Entry(params_frame, width=20)
        self.dimension_entry.insert(0, "3")
        self.dimension_entry.pack(padx=5, pady=2)
        
        # Количество кубов
        ttk.Label(params_frame, text="Количество кубов:").pack(anchor=tk.W, padx=5, pady=2)
        self.num_cubes_entry = ttk.Entry(params_frame, width=20)
        self.num_cubes_entry.insert(0, "2")
        self.num_cubes_entry.pack(padx=5, pady=2)
        
        # Кнопка создания сети
        create_btn = tk.Button(
            params_frame,
            text="Создать сеть",
            command=self._create_network,
            bg='#3c3c3c',
            fg='#00ff00',
            font=('Consolas', 10, 'bold'),
            cursor='hand2'
        )
        create_btn.pack(pady=10)
        
        # Поиск пути
        path_frame = tk.LabelFrame(
            left_panel,
            text="Поиск кратчайшего пути",
            bg='#2b2b2b',
            fg='#00ff00',
            font=('Consolas', 10, 'bold')
        )
        path_frame.pack(fill=tk.X, pady=5)
        
        # Исходный процессор
        ttk.Label(path_frame, text="Исходный процессор:").pack(anchor=tk.W, padx=5, pady=2)
        self.source_entry = ttk.Entry(path_frame, width=20)
        self.source_entry.insert(0, "0")
        self.source_entry.pack(padx=5, pady=2)
        
        # Конечный процессор
        ttk.Label(path_frame, text="Конечный процессор:").pack(anchor=tk.W, padx=5, pady=2)
        self.destination_entry = ttk.Entry(path_frame, width=20)
        self.destination_entry.insert(0, "7")
        self.destination_entry.pack(padx=5, pady=2)
        
        # Кнопка поиска пути
        find_btn = tk.Button(
            path_frame,
            text="Найти путь",
            command=self._find_path,
            bg='#3c3c3c',
            fg='#00ff00',
            font=('Consolas', 10, 'bold'),
            cursor='hand2'
        )
        find_btn.pack(pady=10)
        
        # === ПРАВАЯ ПАНЕЛЬ ===
        
        # Визуализация графа
        self.figure = plt.Figure(figsize=(8, 5), facecolor='#1e1e1e')
        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor('#1e1e1e')
        
        self.canvas = FigureCanvasTkAgg(self.figure, right_panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Текстовое поле для результатов
        result_frame = tk.LabelFrame(
            right_panel,
            text="Результаты",
            bg='#2b2b2b',
            fg='#00ff00',
            font=('Consolas', 10, 'bold')
        )
        result_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        self.result_text = scrolledtext.ScrolledText(
            result_frame,
            height=10,
            bg='#1e1e1e',
            fg='#00ff00',
            font=('Consolas', 9),
            insertbackground='#00ff00'
        )
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Начальное сообщение
        self._show_welcome_message()
    
    def _show_welcome_message(self):
        """Показать приветственное сообщение."""
        welcome = """
╔════════════════════════════════════════════════════════════════╗
║         ДОБРО ПОЖАЛОВАТЬ В СИМУЛЯТОР ГИПЕРКУБОВ               ║
╚════════════════════════════════════════════════════════════════╝

Инструкции:
1. Выберите метод поиска (один куб или несколько кубов)
2. Укажите размерность куба (1-10)
3. Укажите количество кубов (для метода с несколькими кубами)
4. Нажмите "Создать сеть"
5. Введите ID исходного и конечного процессора
6. Нажмите "Найти путь"

Гиперкуб - это граф, где каждая вершина соединена с вершинами,
отличающимися ровно в одном бите бинарного представления.
        """
        self.result_text.insert(tk.END, welcome)
        self._draw_welcome_graph()
    
    def _draw_welcome_graph(self):
        """Нарисовать приветственный граф."""
        self.ax.clear()
        self.ax.text(
            0.5, 0.5,
            'Создайте сеть для визуализации',
            ha='center', va='center',
            fontsize=16, color='#00ff00',
            transform=self.ax.transAxes
        )
        self.ax.axis('off')
        self.canvas.draw()
    
    def _on_method_change(self):
        """Обработчик изменения метода поиска."""
        if self.search_method.get() == 1:
            self.num_cubes_entry.delete(0, tk.END)
            self.num_cubes_entry.insert(0, "1")
            self.num_cubes_entry.config(state='disabled')
        else:
            self.num_cubes_entry.config(state='normal')
            if self.num_cubes_entry.get() == "1":
                self.num_cubes_entry.delete(0, tk.END)
                self.num_cubes_entry.insert(0, "2")
    
    def _create_network(self):
        """Создать сеть гиперкубов."""
        try:
            dimension = int(self.dimension_entry.get())
            num_cubes = int(self.num_cubes_entry.get())
            
            if dimension < 1 or dimension > 10:
                messagebox.showerror("Ошибка", "Размерность должна быть от 1 до 10")
                return
            
            if num_cubes < 1:
                messagebox.showerror("Ошибка", "Количество кубов должно быть >= 1")
                return
            
            # Создаем сеть
            self.network = MultiCubeNetwork(num_cubes, dimension)
            
            # Обновляем результаты
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, self.network.get_topology_info())
            self.result_text.insert(tk.END, "\n\n✓ Сеть успешно создана!\n")
            
            # Визуализируем граф
            self._visualize_network()
            
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные числовые значения")
    
    def _visualize_network(self):
        """Визуализировать сеть гиперкубов."""
        if self.network is None:
            return
        
        # Создаем граф NetworkX
        self.graph = nx.Graph()
        
        # Добавляем вершины и ребра
        for i in range(self.network.total_processors):
            self.graph.add_node(i)
        
        for i in range(self.network.total_processors):
            for j in range(i + 1, self.network.total_processors):
                if self.network.combined_adjacency_matrix[i][j]:
                    self.graph.add_edge(i, j)
        
        # Вычисляем позиции вершин
        if self.network.num_cubes == 1 and self.network.dimension_per_cube <= 3:
            # Для малых кубов используем специальную раскладку
            self.pos = self._get_hypercube_layout(self.network.dimension_per_cube)
        else:
            # Для больших сетей используем spring layout
            self.pos = nx.spring_layout(self.graph, k=2, iterations=50, seed=42)
        
        # Рисуем граф
        self._draw_graph()
    
    def _get_hypercube_layout(self, dimension):
        """Получить специальную раскладку для гиперкуба малой размерности."""
        pos = {}
        n = 2 ** dimension
        
        if dimension == 1:
            pos = {0: (0, 0), 1: (1, 0)}
        elif dimension == 2:
            pos = {0: (0, 0), 1: (1, 0), 2: (0, 1), 3: (1, 1)}
        elif dimension == 3:
            # 3D куб в 2D проекции
            pos = {
                0: (0, 0), 1: (2, 0), 2: (0, 2), 3: (2, 2),
                4: (0.5, 0.5), 5: (2.5, 0.5), 6: (0.5, 2.5), 7: (2.5, 2.5)
            }
        
        return pos
    
    def _draw_graph(self, path=None):
        """
        Нарисовать граф.
        
        Args:
            path: Список вершин в пути (для подсветки)
        """
        self.ax.clear()
        
        # Цвета вершин
        node_colors = []
        for node in self.graph.nodes():
            if path and node in path:
                if node == path[0]:
                    node_colors.append('#00ff00')  # Начало - зеленый
                elif node == path[-1]:
                    node_colors.append('#ff0000')  # Конец - красный
                else:
                    node_colors.append('#ffff00')  # Путь - желтый
            else:
                cube_id, _ = self.network._decode_address(node)
                # Разные цвета для разных кубов
                colors = ['#4080ff', '#ff8040', '#40ff80', '#ff40ff', '#40ffff']
                node_colors.append(colors[cube_id % len(colors)])
        
        # Рисуем ребра
        nx.draw_networkx_edges(
            self.graph, self.pos, ax=self.ax,
            edge_color='#404040', width=1.5, alpha=0.6
        )
        
        # Подсвечиваем ребра пути
        if path:
            path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
            nx.draw_networkx_edges(
                self.graph, self.pos, ax=self.ax,
                edgelist=path_edges,
                edge_color='#00ff00', width=3, alpha=1
            )
        
        # Рисуем вершины
        nx.draw_networkx_nodes(
            self.graph, self.pos, ax=self.ax,
            node_color=node_colors,
            node_size=500,
            edgecolors='white',
            linewidths=2
        )
        
        # Рисуем метки
        nx.draw_networkx_labels(
            self.graph, self.pos, ax=self.ax,
            font_size=8,
            font_color='black',
            font_weight='bold'
        )
        
        self.ax.set_title(
            f'Сеть гиперкубов: {self.network.num_cubes} куб(а/ов), размерность {self.network.dimension_per_cube}',
            color='#00ff00',
            fontsize=12,
            pad=10
        )
        self.ax.axis('off')
        self.canvas.draw()
    
    def _find_path(self):
        """Найти кратчайший путь между процессорами."""
        if self.network is None:
            messagebox.showwarning("Предупреждение", "Сначала создайте сеть!")
            return
        
        try:
            source = int(self.source_entry.get())
            destination = int(self.destination_entry.get())
            
            if source < 0 or source >= self.network.total_processors:
                messagebox.showerror("Ошибка", f"ID исходного процессора должен быть от 0 до {self.network.total_processors - 1}")
                return
            
            if destination < 0 or destination >= self.network.total_processors:
                messagebox.showerror("Ошибка", f"ID конечного процессора должен быть от 0 до {self.network.total_processors - 1}")
                return
            
            # Находим путь
            path = self.network.find_shortest_path(source, destination)
            
            # Выводим результаты
            self.result_text.delete(1.0, tk.END)
            
            if path:
                method_name = "BFS (один куб)" if self.search_method.get() == 1 else "BFS (несколько кубов)"
                self.result_text.insert(tk.END, f"\n{'='*60}\n")
                self.result_text.insert(tk.END, f"КРАТЧАЙШИЙ ПУТЬ (метод: {method_name})\n")
                self.result_text.insert(tk.END, f"{'='*60}\n\n")
                
                self.result_text.insert(tk.END, f"Исходный процессор: {self.network.format_processor_info(source)}\n")
                self.result_text.insert(tk.END, f"Конечный процессор: {self.network.format_processor_info(destination)}\n\n")
                
                self.result_text.insert(tk.END, f"Длина пути: {len(path) - 1} ребер\n\n")
                
                self.result_text.insert(tk.END, "Путь:\n")
                for i, node in enumerate(path):
                    self.result_text.insert(tk.END, f"  {i+1}. {self.network.format_processor_info(node)}\n")
                    if i < len(path) - 1:
                        self.result_text.insert(tk.END, "     ↓\n")
                
                self.result_text.insert(tk.END, f"\n{'='*60}\n")
                
                # Визуализируем путь
                self._draw_graph(path)
            else:
                self.result_text.insert(tk.END, "\n✗ Путь не найден!\n")
                
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные числовые значения")


def main():
    """Главная функция."""
    root = tk.Tk()
    app = HypercubeGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
