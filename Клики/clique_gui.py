"""
GUI приложение для поиска клик в графе
Использует tkinter для интерфейса и matplotlib для визуализации
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import math
from clique_finder import Graph, find_clique_greater_than_b, find_max_clique, is_clique


class CliqueFinderGUI:
    """Графический интерфейс для поиска клик в графе"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Поиск клик в графе")
        self.root.geometry("1200x800")
        
        # Переменные для хранения данных
        self.graph = None
        self.clique_b = []
        self.max_clique = []
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Создание виджетов интерфейса"""
        
        # Основной контейнер
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Настройка растягивания
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # === Панель ввода параметров ===
        input_frame = ttk.LabelFrame(main_frame, text="Параметры графа", padding="10")
        input_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Количество вершин
        ttk.Label(input_frame, text="Количество вершин:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.vertices_var = tk.StringVar(value="8")
        vertices_entry = ttk.Entry(input_frame, textvariable=self.vertices_var, width=10)
        vertices_entry.grid(row=0, column=1, padx=5)
        
        # Количество рёбер
        ttk.Label(input_frame, text="Количество рёбер:").grid(row=0, column=2, sticky=tk.W, padx=5)
        self.edges_var = tk.StringVar(value="15")
        edges_entry = ttk.Entry(input_frame, textvariable=self.edges_var, width=10)
        edges_entry.grid(row=0, column=3, padx=5)
        
        # Значение B
        ttk.Label(input_frame, text="Значение B:").grid(row=0, column=4, sticky=tk.W, padx=5)
        self.b_var = tk.StringVar(value="3")
        b_entry = ttk.Entry(input_frame, textvariable=self.b_var, width=10)
        b_entry.grid(row=0, column=5, padx=5)
        
        # Кнопка запуска
        run_button = ttk.Button(input_frame, text="Найти клики", command=self._run_algorithm)
        run_button.grid(row=0, column=6, padx=20)
        
        # === Панель результатов ===
        results_frame = ttk.LabelFrame(main_frame, text="Результаты и процесс поиска", padding="10")
        results_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        results_frame.rowconfigure(0, weight=1)
        results_frame.columnconfigure(0, weight=1)
        
        # Текстовое поле для вывода
        self.output_text = scrolledtext.ScrolledText(results_frame, width=60, height=30, wrap=tk.WORD)
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # === Панель визуализации ===
        viz_frame = ttk.LabelFrame(main_frame, text="Визуализация графа", padding="10")
        viz_frame.grid(row=1, column=1, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))
        viz_frame.rowconfigure(0, weight=1)
        viz_frame.columnconfigure(0, weight=1)
        
        # Создаём фигуру matplotlib
        self.fig = Figure(figsize=(6, 6), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=viz_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # === Панель матрицы смежности ===
        matrix_frame = ttk.LabelFrame(main_frame, text="Матрица смежности", padding="10")
        matrix_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        matrix_frame.rowconfigure(0, weight=1)
        matrix_frame.columnconfigure(0, weight=1)
        
        self.matrix_text = scrolledtext.ScrolledText(matrix_frame, width=60, height=10, wrap=tk.NONE)
        self.matrix_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    def _log(self, message):
        """Вывод сообщения в текстовое поле"""
        self.output_text.insert(tk.END, message)
        self.output_text.see(tk.END)
        self.root.update_idletasks()
    
    def _run_algorithm(self):
        """Запуск алгоритма поиска клик"""
        try:
            # Получаем параметры
            num_vertices = int(self.vertices_var.get())
            num_edges = int(self.edges_var.get())
            b = int(self.b_var.get())
            
            # Валидация
            if num_vertices < 1:
                messagebox.showerror("Ошибка", "Количество вершин должно быть больше 0")
                return
            
            max_edges = num_vertices * (num_vertices - 1) // 2
            if num_edges > max_edges:
                messagebox.showerror("Ошибка", f"Максимальное количество рёбер: {max_edges}")
                return
            
            # Очищаем вывод
            self.output_text.delete(1.0, tk.END)
            self.matrix_text.delete(1.0, tk.END)
            
            # Создаём граф
            self._log(f"Создание графа с {num_vertices} вершинами и {num_edges} рёбрами...\n\n")
            self.graph = Graph(num_vertices, num_edges)
            
            # Выводим матрицу смежности
            self._log("Матрица смежности:\n")
            matrix_str = self.graph.get_matrix_string()
            self.matrix_text.insert(1.0, matrix_str)
            
            # Поиск клики больше B
            self._log(f"\nПоиск клики размером больше {b}...\n")
            self.clique_b = find_clique_greater_than_b(self.graph.adjacency_matrix, b)
            
            if self.clique_b:
                self._log(f"✓ В графе существует клика больше, чем {b}.\n")
                self._log(f"  Вершины этой клики: {', '.join(map(str, self.clique_b))}\n")
                self._log(f"  Размер клики: {len(self.clique_b)}\n\n")
            else:
                self._log(f"✗ В графе не существует клики больше, чем {b}.\n\n")
            
            # Поиск максимальной клики
            self._log("=" * 60 + "\n")
            self._log("Поиск максимальной клики (с выводом процесса):\n")
            self._log("=" * 60 + "\n")
            
            self.max_clique = find_max_clique(self.graph.adjacency_matrix, callback=self._log)
            
            self._log("\n" + "=" * 60 + "\n")
            self._log("РЕЗУЛЬТАТ:\n")
            self._log("=" * 60 + "\n")
            self._log(f"Максимальная клика в графе:\n")
            self._log(f"  Размер клики: {len(self.max_clique)}\n")
            self._log(f"  Вершины клики: {', '.join(map(str, self.max_clique))}\n")
            
            # Визуализация
            self._visualize_graph()
            
        except ValueError as e:
            messagebox.showerror("Ошибка", f"Неверный формат ввода: {e}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")
    
    def _visualize_graph(self):
        """Визуализация графа с помощью matplotlib"""
        if self.graph is None:
            return
        
        self.ax.clear()
        
        num_vertices = self.graph.num_vertices
        adjacency_matrix = self.graph.adjacency_matrix
        
        # Вычисляем позиции вершин по кругу
        positions = {}
        for i in range(num_vertices):
            angle = 2.0 * math.pi * i / num_vertices
            x = math.cos(angle)
            y = math.sin(angle)
            positions[i] = (x, y)
        
        # Рисуем рёбра
        for i in range(num_vertices):
            for j in range(i + 1, num_vertices):
                if adjacency_matrix[i][j] == 1:
                    x1, y1 = positions[i]
                    x2, y2 = positions[j]
                    self.ax.plot([x1, x2], [y1, y2], 'gray', linewidth=1, alpha=0.5, zorder=1)
        
        # Определяем цвета вершин
        colors = []
        sizes = []
        for i in range(num_vertices):
            if i in self.max_clique:
                colors.append('#FF4444')  # Красный для максимальной клики
                sizes.append(800)
            elif i in self.clique_b:
                colors.append('#FFA500')  # Оранжевый для клики B
                sizes.append(600)
            else:
                colors.append('#4444FF')  # Синий для обычных вершин
                sizes.append(400)
        
        # Рисуем вершины
        for i in range(num_vertices):
            x, y = positions[i]
            self.ax.scatter(x, y, c=colors[i], s=sizes[i], zorder=2, edgecolors='black', linewidths=2)
            self.ax.text(x, y, str(i), ha='center', va='center', fontsize=12, fontweight='bold', zorder=3)
        
        # Легенда
        legend_elements = [
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#4444FF', 
                      markersize=10, label='Обычная вершина'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#FFA500', 
                      markersize=12, label=f'Клика > {self.b_var.get()}'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#FF4444', 
                      markersize=14, label='Максимальная клика')
        ]
        self.ax.legend(handles=legend_elements, loc='upper right')
        
        self.ax.set_xlim(-1.5, 1.5)
        self.ax.set_ylim(-1.5, 1.5)
        self.ax.set_aspect('equal')
        self.ax.axis('off')
        self.ax.set_title('Граф с выделенными кликами', fontsize=14, fontweight='bold')
        
        self.canvas.draw()


def main():
    """Главная функция запуска приложения"""
    root = tk.Tk()
    app = CliqueFinderGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
