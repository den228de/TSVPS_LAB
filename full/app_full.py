"""
GUI приложение для визуализации результатов анализа алгоритмов.
ПОЛНАЯ ВЕРСИЯ - использует полное тестирование (stone_partition.py)
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import sys
from io import StringIO
import threading
from stone_partition import run_tests


class StonePartitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Анализ алгоритмов разделения камней [ПОЛНАЯ ВЕРСИЯ]")
        self.root.geometry("1400x800")
        self.root.configure(bg='#2b2b2b')
        
        # Результаты тестов
        self.results = None
        
        # Создаем интерфейс
        self.create_widgets()
    
    def create_widgets(self):
        """Создание элементов интерфейса"""
        
        # Заголовок
        title_frame = tk.Frame(self.root, bg='#2b2b2b')
        title_frame.pack(pady=10)
        
        title_label = tk.Label(
            title_frame,
            text="Анализ алгоритмов разделения камней на две кучи",
            font=("Arial", 18, "bold"),
            bg='#2b2b2b',
            fg='#00ff00'
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Сравнение полного перебора и эвристического алгоритма",
            font=("Arial", 12),
            bg='#2b2b2b',
            fg='#888888'
        )
        subtitle_label.pack()
        
        mode_label = tk.Label(
            title_frame,
            text="🔬 ПОЛНАЯ ВЕРСИЯ (все тесты, может занять 30-60 секунд)",
            font=("Arial", 9, "bold"),
            bg='#2b2b2b',
            fg='#ff6600'
        )
        mode_label.pack()
        
        # Кнопка запуска
        button_frame = tk.Frame(self.root, bg='#2b2b2b')
        button_frame.pack(pady=10)
        
        self.run_button = tk.Button(
            button_frame,
            text="▶ Запустить полное тестирование",
            command=self.run_analysis_threaded,
            font=("Arial", 14, "bold"),
            bg='#00aa00',
            fg='white',
            activebackground='#00cc00',
            activeforeground='white',
            padx=20,
            pady=10,
            cursor='hand2'
        )
        self.run_button.pack()
        
        # Прогресс-бар
        self.progress_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 10),
            bg='#2b2b2b',
            fg='#00ff00'
        )
        self.progress_label.pack()
        
        # Notebook для вкладок
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Стиль для вкладок
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TNotebook', background='#2b2b2b', borderwidth=0)
        style.configure('TNotebook.Tab', background='#3c3c3c', foreground='white', 
                       padding=[20, 10], font=('Arial', 10, 'bold'))
        style.map('TNotebook.Tab', background=[('selected', '#00aa00')], 
                 foreground=[('selected', 'white')])
        
        # Вкладка с результатами
        self.results_tab = tk.Frame(self.notebook, bg='#1e1e1e')
        self.notebook.add(self.results_tab, text='📊 Результаты')
        
        self.results_text = scrolledtext.ScrolledText(
            self.results_tab,
            font=("Consolas", 10),
            bg='#1e1e1e',
            fg='#00ff00',
            insertbackground='white',
            wrap=tk.WORD
        )
        self.results_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Вкладки для графиков
        self.graph_tabs = []
        self.canvases = []
        
        for i, weight in enumerate([10, 20, 40]):
            tab = tk.Frame(self.notebook, bg='#1e1e1e')
            self.notebook.add(tab, text=f'📈 График: Вес 1-{weight}')
            self.graph_tabs.append(tab)
    
    def run_analysis_threaded(self):
        """Запуск анализа в отдельном потоке"""
        thread = threading.Thread(target=self.run_analysis, daemon=True)
        thread.start()
    
    def run_analysis(self):
        """Запуск анализа алгоритмов"""
        self.run_button.config(state='disabled', text='⏳ Выполняется (может занять минуту)...')
        self.progress_label.config(text='⏳ Полное тестирование в процессе... Пожалуйста, подождите.')
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, "Запуск полного тестирования...\n\n")
        self.results_text.insert(tk.END, "Это займет 30-60 секунд, так как выполняется полный перебор для 23 камней.\n")
        self.results_text.insert(tk.END, "Всего будет выполнено: 3 уровня × 10 размеров × 10 итераций = 300 тестов\n\n")
        
        # Перехватываем вывод в консоль
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        try:
            # Запускаем тесты
            self.results = run_tests()
            
            # Получаем вывод
            output = sys.stdout.getvalue()
            sys.stdout = old_stdout
            
            # Отображаем результаты
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(1.0, output)
            
            # Строим графики
            self.plot_graphs()
            
            self.progress_label.config(text='✓ Полное тестирование завершено успешно!')
            
        except Exception as e:
            sys.stdout = old_stdout
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(1.0, f"Ошибка: {str(e)}\n\n{type(e).__name__}")
            import traceback
            self.results_text.insert(tk.END, f"\n\n{traceback.format_exc()}")
            self.progress_label.config(text='✗ Ошибка при выполнении')
        
        finally:
            self.run_button.config(state='normal', text='▶ Запустить полное тестирование')
    
    def plot_graphs(self):
        """Построение графиков для каждого уровня сложности"""
        if not self.results:
            return
        
        # Очищаем старые графики
        for canvas in self.canvases:
            canvas.get_tk_widget().destroy()
        self.canvases.clear()
        
        weights = [10, 20, 40]
        
        for idx, (tab, weight) in enumerate(zip(self.graph_tabs, weights)):
            # Создаем фигуру
            fig = Figure(figsize=(12, 6), facecolor='#1e1e1e')
            ax = fig.add_subplot(111)
            
            # Данные для графика
            data_points = len(self.results['brute_force'][idx])
            x_values = [2 * (i + 1) for i in range(data_points)]
            x_labels = [str(5 + 2 * i) for i in range(data_points)]
            
            bf_data = self.results['brute_force'][idx]
            greedy_data = self.results['greedy'][idx]
            
            # Строим линии
            ax.plot(x_values, bf_data, 'o-', color='#3399ff', linewidth=2, 
                   markersize=8, label='Полный перебор', markeredgecolor='white', markeredgewidth=1)
            ax.plot(x_values, greedy_data, 's-', color='#00ff00', linewidth=2, 
                   markersize=8, label='Эвристика', markeredgecolor='white', markeredgewidth=1)
            
            # Настройка осей
            ax.set_xlabel('Количество камней', fontsize=12, color='white', fontweight='bold')
            ax.set_ylabel('Средняя разница весов (%)', fontsize=12, color='white', fontweight='bold')
            ax.set_title(f'Сравнение алгоритмов (Вес камней: 1-{weight})', 
                        fontsize=14, color='white', fontweight='bold', pad=20)
            
            # Устанавливаем метки по оси X
            ax.set_xticks(x_values)
            ax.set_xticklabels(x_labels)
            
            # Сетка
            ax.grid(True, alpha=0.3, linestyle='--', color='#555555')
            ax.set_facecolor('#2b2b2b')
            
            # Легенда
            legend = ax.legend(loc='upper right', fontsize=11, framealpha=0.9)
            legend.get_frame().set_facecolor('#3c3c3c')
            legend.get_frame().set_edgecolor('white')
            for text in legend.get_texts():
                text.set_color('white')
            
            # Цвет осей и меток
            ax.tick_params(colors='white', labelsize=10)
            for spine in ax.spines.values():
                spine.set_edgecolor('#555555')
            
            fig.tight_layout()
            
            # Добавляем график на вкладку
            canvas = FigureCanvasTkAgg(fig, master=tab)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True, padx=5, pady=5)
            self.canvases.append(canvas)


def main():
    """Главная функция запуска приложения"""
    root = tk.Tk()
    app = StonePartitionApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
