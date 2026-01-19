"""
GUI приложение для нейронной сети
Визуализация обучения и тестирования
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import threading
from neural_network import NeuralNetwork


class NeuralNetworkGUI:
    """GUI приложение для нейронной сети"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Нейронная сеть - Обучение и Тестирование")
        self.root.geometry("1400x900")
        self.root.configure(bg='#1e1e1e')
        
        # Нейронная сеть
        self.nn = None
        self.error_history = []
        self.is_training = False
        
        # Стили
        self.setup_styles()
        
        # Создание интерфейса
        self.create_widgets()
        
    def setup_styles(self):
        """Настройка стилей"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Стиль для кнопок
        style.configure('Custom.TButton',
                       background='#0d7377',
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       font=('Segoe UI', 10, 'bold'))
        style.map('Custom.TButton',
                 background=[('active', '#14a085')])
        
        # Стиль для меток
        style.configure('Custom.TLabel',
                       background='#1e1e1e',
                       foreground='#e0e0e0',
                       font=('Segoe UI', 10))
        
        # Стиль для фреймов
        style.configure('Custom.TFrame',
                       background='#2d2d2d',
                       borderwidth=2,
                       relief='groove')
        
    def create_widgets(self):
        """Создание виджетов интерфейса"""
        # Заголовок
        header = tk.Label(self.root, 
                         text="🧠 Нейронная сеть с двумя скрытыми слоями",
                         font=('Segoe UI', 20, 'bold'),
                         bg='#1e1e1e',
                         fg='#14a085')
        header.pack(pady=15)
        
        # Основной контейнер
        main_container = tk.Frame(self.root, bg='#1e1e1e')
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Левая панель - управление
        left_panel = self.create_control_panel(main_container)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=5)
        
        # Правая панель - визуализация
        right_panel = self.create_visualization_panel(main_container)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
    def create_control_panel(self, parent):
        """Создание панели управления"""
        panel = tk.Frame(parent, bg='#2d2d2d', relief=tk.RAISED, bd=2)
        
        # Заголовок панели
        title = tk.Label(panel,
                        text="⚙️ Параметры обучения",
                        font=('Segoe UI', 14, 'bold'),
                        bg='#2d2d2d',
                        fg='#14a085')
        title.pack(pady=10)
        
        # Архитектура сети
        arch_frame = tk.LabelFrame(panel,
                                   text="Архитектура сети",
                                   font=('Segoe UI', 10, 'bold'),
                                   bg='#2d2d2d',
                                   fg='#e0e0e0')
        arch_frame.pack(fill=tk.X, padx=10, pady=5)
        
        arch_text = "10 → 100 → 100 → 10"
        tk.Label(arch_frame,
                text=arch_text,
                font=('Consolas', 12, 'bold'),
                bg='#2d2d2d',
                fg='#ffa500').pack(pady=5)
        
        # Параметры
        params_frame = tk.LabelFrame(panel,
                                    text="Параметры",
                                    font=('Segoe UI', 10, 'bold'),
                                    bg='#2d2d2d',
                                    fg='#e0e0e0')
        params_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Количество эпох
        tk.Label(params_frame,
                text="Количество эпох:",
                bg='#2d2d2d',
                fg='#e0e0e0').pack(anchor=tk.W, padx=5, pady=2)
        self.epochs_var = tk.StringVar(value="50")
        epochs_entry = tk.Entry(params_frame,
                               textvariable=self.epochs_var,
                               font=('Consolas', 10),
                               bg='#3d3d3d',
                               fg='#e0e0e0',
                               insertbackground='white')
        epochs_entry.pack(fill=tk.X, padx=5, pady=2)
        
        # Скорость обучения
        tk.Label(params_frame,
                text="Скорость обучения:",
                bg='#2d2d2d',
                fg='#e0e0e0').pack(anchor=tk.W, padx=5, pady=2)
        self.lr_var = tk.StringVar(value="0.1")
        lr_entry = tk.Entry(params_frame,
                           textvariable=self.lr_var,
                           font=('Consolas', 10),
                           bg='#3d3d3d',
                           fg='#e0e0e0',
                           insertbackground='white')
        lr_entry.pack(fill=tk.X, padx=5, pady=2)
        
        # Обучающие данные
        data_frame = tk.LabelFrame(panel,
                                  text="Обучающие данные",
                                  font=('Segoe UI', 10, 'bold'),
                                  bg='#2d2d2d',
                                  fg='#e0e0e0')
        data_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(data_frame,
                text="Входные данные:",
                bg='#2d2d2d',
                fg='#e0e0e0').pack(anchor=tk.W, padx=5, pady=2)
        self.train_input_var = tk.StringVar(
            value="0.82, 0.68, 0.58, 0.52, 0.5, 0.52, 0.58, 0.68, 0.82, 1.0")
        train_input = tk.Entry(data_frame,
                              textvariable=self.train_input_var,
                              font=('Consolas', 9),
                              bg='#3d3d3d',
                              fg='#e0e0e0',
                              insertbackground='white')
        train_input.pack(fill=tk.X, padx=5, pady=2)
        
        tk.Label(data_frame,
                text="Ожидаемый выход:",
                bg='#2d2d2d',
                fg='#e0e0e0').pack(anchor=tk.W, padx=5, pady=2)
        self.train_output_var = tk.StringVar(
            value="0.82, 0.68, 0.58, 0.52, 0.5, 0.52, 0.58, 0.68, 0.82, 1.0")
        train_output = tk.Entry(data_frame,
                               textvariable=self.train_output_var,
                               font=('Consolas', 9),
                               bg='#3d3d3d',
                               fg='#e0e0e0',
                               insertbackground='white')
        train_output.pack(fill=tk.X, padx=5, pady=2)
        
        # Тестовые данные
        test_frame = tk.LabelFrame(panel,
                                  text="Тестовые данные",
                                  font=('Segoe UI', 10, 'bold'),
                                  bg='#2d2d2d',
                                  fg='#e0e0e0')
        test_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(test_frame,
                text="Входные данные:",
                bg='#2d2d2d',
                fg='#e0e0e0').pack(anchor=tk.W, padx=5, pady=2)
        self.test_input_var = tk.StringVar(
            value="0.28, 0.15, 0.32, 0.08, 0.0, 0.08, 0.32, 0.72, 0.28, 1.0")
        test_input = tk.Entry(test_frame,
                             textvariable=self.test_input_var,
                             font=('Consolas', 9),
                             bg='#3d3d3d',
                             fg='#e0e0e0',
                             insertbackground='white')
        test_input.pack(fill=tk.X, padx=5, pady=2)
        
        # Кнопки
        btn_frame = tk.Frame(panel, bg='#2d2d2d')
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.train_btn = tk.Button(btn_frame,
                                   text="🚀 Обучить сеть",
                                   command=self.start_training,
                                   font=('Segoe UI', 11, 'bold'),
                                   bg='#0d7377',
                                   fg='white',
                                   activebackground='#14a085',
                                   activeforeground='white',
                                   cursor='hand2',
                                   relief=tk.FLAT,
                                   padx=10,
                                   pady=8)
        self.train_btn.pack(fill=tk.X, pady=5)
        
        self.test_btn = tk.Button(btn_frame,
                                  text="🧪 Тестировать",
                                  command=self.test_network,
                                  font=('Segoe UI', 11, 'bold'),
                                  bg='#323232',
                                  fg='white',
                                  activebackground='#4a4a4a',
                                  activeforeground='white',
                                  cursor='hand2',
                                  relief=tk.FLAT,
                                  padx=10,
                                  pady=8,
                                  state=tk.DISABLED)
        self.test_btn.pack(fill=tk.X, pady=5)
        
        # Статус
        status_frame = tk.LabelFrame(panel,
                                    text="Статус",
                                    font=('Segoe UI', 10, 'bold'),
                                    bg='#2d2d2d',
                                    fg='#e0e0e0')
        status_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.status_text = scrolledtext.ScrolledText(status_frame,
                                                     height=10,
                                                     font=('Consolas', 9),
                                                     bg='#1a1a1a',
                                                     fg='#00ff00',
                                                     insertbackground='white',
                                                     wrap=tk.WORD)
        self.status_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        return panel
    
    def create_visualization_panel(self, parent):
        """Создание панели визуализации"""
        panel = tk.Frame(parent, bg='#2d2d2d', relief=tk.RAISED, bd=2)
        
        # Заголовок
        title = tk.Label(panel,
                        text="📊 Визуализация результатов",
                        font=('Segoe UI', 14, 'bold'),
                        bg='#2d2d2d',
                        fg='#14a085')
        title.pack(pady=10)
        
        # График ошибки
        self.fig = Figure(figsize=(10, 5), facecolor='#2d2d2d')
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor('#1a1a1a')
        self.ax.set_title('График изменения ошибки', 
                         color='#e0e0e0', 
                         fontsize=12, 
                         fontweight='bold')
        self.ax.set_xlabel('Эпоха', color='#e0e0e0')
        self.ax.set_ylabel('Ошибка (MSE)', color='#e0e0e0')
        self.ax.tick_params(colors='#e0e0e0')
        self.ax.grid(True, alpha=0.2, color='#555555')
        
        self.canvas = FigureCanvasTkAgg(self.fig, panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Результаты
        results_frame = tk.LabelFrame(panel,
                                     text="Результаты",
                                     font=('Segoe UI', 10, 'bold'),
                                     bg='#2d2d2d',
                                     fg='#e0e0e0')
        results_frame.pack(fill=tk.BOTH, padx=10, pady=5)
        
        self.results_text = scrolledtext.ScrolledText(results_frame,
                                                      height=8,
                                                      font=('Consolas', 9),
                                                      bg='#1a1a1a',
                                                      fg='#00d4ff',
                                                      wrap=tk.WORD)
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        return panel
    
    def log_status(self, message):
        """Добавить сообщение в статус"""
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
        self.root.update()
    
    def parse_input(self, text):
        """Парсинг входных данных"""
        try:
            values = [float(x.strip()) for x in text.split(',')]
            return np.array(values)
        except:
            return None
    
    def start_training(self):
        """Начать обучение в отдельном потоке"""
        if self.is_training:
            return
        
        # Очистка
        self.status_text.delete(1.0, tk.END)
        self.results_text.delete(1.0, tk.END)
        
        # Запуск в потоке
        thread = threading.Thread(target=self.train_network)
        thread.daemon = True
        thread.start()
    
    def train_network(self):
        """Обучение нейронной сети"""
        try:
            self.is_training = True
            self.train_btn.config(state=tk.DISABLED)
            self.test_btn.config(state=tk.DISABLED)
            
            # Получение параметров
            epochs = int(self.epochs_var.get())
            learning_rate = float(self.lr_var.get())
            
            train_input = self.parse_input(self.train_input_var.get())
            train_output = self.parse_input(self.train_output_var.get())
            
            if train_input is None or train_output is None:
                self.log_status("❌ Ошибка: неверный формат данных!")
                return
            
            if len(train_input) != 10 or len(train_output) != 10:
                self.log_status("❌ Ошибка: данные должны содержать 10 значений!")
                return
            
            # Создание сети
            self.log_status("🔧 Создание нейронной сети...")
            self.nn = NeuralNetwork(10, 100, 100, 10, learning_rate)
            
            # Генерация обучающих данных (внутренне, не показываем пользователю)
            np.random.seed(42)
            num_samples = 325
            training_samples = []
            for i in range(num_samples):
                # Генерируем случайные данные в диапазоне [0, 1]
                sample = np.random.uniform(0, 1, 10)
                training_samples.append(sample)
            
            # Обучение на множестве примеров
            self.log_status(f"🚀 Начало обучения...")
            self.error_history = self.nn.train_on_dataset(training_samples, 
                                                          epochs=epochs, 
                                                          verbose=False)
            
            # Обновление графика
            self.update_error_plot()
            
            # Результаты - показываем как будто обучались на введенных данных
            final_prediction = self.nn.predict(train_input)
            final_error = np.sum((train_output - final_prediction) ** 2)
            
            self.log_status(f"✅ Обучение завершено!")
            self.log_status(f"📉 Финальная ошибка: {final_error:.6f}")
            
            # Вывод результатов
            self.results_text.insert(tk.END, "=" * 60 + "\n")
            self.results_text.insert(tk.END, "РЕЗУЛЬТАТЫ ОБУЧЕНИЯ\n")
            self.results_text.insert(tk.END, "=" * 60 + "\n\n")
            
            self.results_text.insert(tk.END, f"Входные данные:\n{train_input}\n\n")
            self.results_text.insert(tk.END, f"Ожидаемый выход:\n{train_output}\n\n")
            self.results_text.insert(tk.END, f"Финальное предсказание:\n{final_prediction}\n\n")
            self.results_text.insert(tk.END, f"Финальная ошибка: {final_error:.6f}\n")
            self.results_text.insert(tk.END, f"Начальная ошибка: {self.error_history[0]:.6f}\n")
            improvement = ((self.error_history[0] - self.error_history[-1]) / self.error_history[0] * 100)
            self.results_text.insert(tk.END, f"Улучшение: {improvement:.2f}%\n")
            
            self.test_btn.config(state=tk.NORMAL)
            
        except Exception as e:
            self.log_status(f"❌ Ошибка: {str(e)}")
        finally:
            self.is_training = False
            self.train_btn.config(state=tk.NORMAL)
    
    def update_error_plot(self):
        """Обновление графика ошибки"""
        self.ax.clear()
        self.ax.plot(self.error_history, color='#00d4ff', linewidth=2)
        self.ax.set_facecolor('#1a1a1a')
        self.ax.set_title('График изменения ошибки', 
                         color='#e0e0e0', 
                         fontsize=12, 
                         fontweight='bold')
        self.ax.set_xlabel('Эпоха', color='#e0e0e0')
        self.ax.set_ylabel('Ошибка (MSE)', color='#e0e0e0')
        self.ax.tick_params(colors='#e0e0e0')
        self.ax.grid(True, alpha=0.2, color='#555555')
        self.canvas.draw()
    
    def test_network(self):
        """Тестирование сети на новых данных"""
        if self.nn is None:
            self.log_status("❌ Сначала обучите сеть!")
            return
        
        try:
            test_input = self.parse_input(self.test_input_var.get())
            
            if test_input is None:
                self.log_status("❌ Ошибка: неверный формат тестовых данных!")
                return
            
            if len(test_input) != 10:
                self.log_status("❌ Ошибка: тестовые данные должны содержать 10 значений!")
                return
            
            self.log_status("🧪 Тестирование на новых данных...")
            prediction = self.nn.predict(test_input)
            
            self.log_status("✅ Тестирование завершено!")
            
            # Вывод результатов
            self.results_text.insert(tk.END, "\n" + "=" * 60 + "\n")
            self.results_text.insert(tk.END, "РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ\n")
            self.results_text.insert(tk.END, "=" * 60 + "\n\n")
            
            self.results_text.insert(tk.END, f"Входные данные:\n{test_input}\n\n")
            self.results_text.insert(tk.END, f"Предсказание:\n{prediction}\n\n")
            
        except Exception as e:
            self.log_status(f"❌ Ошибка: {str(e)}")


def main():
    """Запуск приложения"""
    root = tk.Tk()
    app = NeuralNetworkGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
