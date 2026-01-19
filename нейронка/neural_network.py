"""
Нейронная сеть с двумя скрытыми слоями
Реализация на Python (конвертировано из C++)
"""

import numpy as np
from typing import List, Tuple


class NeuralNetwork:
    """
    Класс нейронной сети с двумя скрытыми слоями
    Архитектура: Input -> Hidden1 -> Hidden2 -> Output
    """
    
    def __init__(self, input_size: int, hidden_size1: int, hidden_size2: int, 
                 output_size: int, learning_rate: float = 0.1):
        """
        Инициализация нейронной сети
        
        Args:
            input_size: Размер входного слоя
            hidden_size1: Размер первого скрытого слоя
            hidden_size2: Размер второго скрытого слоя
            output_size: Размер выходного слоя
            learning_rate: Скорость обучения
        """
        self.input_size = input_size
        self.hidden_size1 = hidden_size1
        self.hidden_size2 = hidden_size2
        self.output_size = output_size
        self.learning_rate = learning_rate
        
        # Инициализация слоев
        self.input_layer = np.zeros(input_size)
        self.hidden_layer1 = np.zeros(hidden_size1)
        self.hidden_layer2 = np.zeros(hidden_size2)
        self.output_layer = np.zeros(output_size)
        
        # Сохранение предыдущих значений для обучения
        self.last_input_layer = np.zeros(input_size)
        self.last_hidden_layer1 = np.zeros(hidden_size1)
        self.last_hidden_layer2 = np.zeros(hidden_size2)
        
        # Инициализация весов случайными значениями в диапазоне [-0.5, 0.5]
        np.random.seed(42)  # Для воспроизводимости результатов
        self.weights1 = np.random.uniform(-0.5, 0.5, (input_size, hidden_size1))
        self.weights2 = np.random.uniform(-0.5, 0.5, (hidden_size1, hidden_size2))
        self.weights3 = np.random.uniform(-0.5, 0.5, (hidden_size2, output_size))
    
    @staticmethod
    def sigmoid(x: np.ndarray) -> np.ndarray:
        """Функция активации сигмоида"""
        return 1.0 / (1.0 + np.exp(-np.clip(x, -500, 500)))
    
    @staticmethod
    def sigmoid_derivative(x: np.ndarray) -> np.ndarray:
        """Производная функции сигмоиды"""
        return x * (1.0 - x)
    
    def forward_propagation(self, input_data: np.ndarray) -> np.ndarray:
        """
        Прямое распространение сигнала через сеть
        
        Args:
            input_data: Входные данные
            
        Returns:
            Выходные данные сети
        """
        if len(input_data) != self.input_size:
            raise ValueError(f"Размер входных данных ({len(input_data)}) не соответствует "
                           f"размеру входного слоя ({self.input_size})")
        
        # Входной слой
        self.input_layer = np.array(input_data)
        self.last_input_layer = self.input_layer.copy()
        
        # Первый скрытый слой
        hidden1_sum = np.dot(self.input_layer, self.weights1)
        self.hidden_layer1 = self.sigmoid(hidden1_sum)
        self.last_hidden_layer1 = self.hidden_layer1.copy()
        
        # Второй скрытый слой
        hidden2_sum = np.dot(self.hidden_layer1, self.weights2)
        self.hidden_layer2 = self.sigmoid(hidden2_sum)
        self.last_hidden_layer2 = self.hidden_layer2.copy()
        
        # Выходной слой
        output_sum = np.dot(self.hidden_layer2, self.weights3)
        self.output_layer = self.sigmoid(output_sum)
        
        return self.output_layer
    
    def backpropagate(self, expected_output: np.ndarray):
        """
        Обратное распространение ошибки и обновление весов
        
        Args:
            expected_output: Ожидаемые выходные данные
        """
        if len(expected_output) != self.output_size:
            raise ValueError(f"Размер ожидаемых выходных данных не соответствует "
                           f"размеру выходного слоя")
        
        # Вычисление ошибки выходного слоя
        output_errors = (expected_output - self.output_layer) * \
                       self.sigmoid_derivative(self.output_layer)
        
        # Вычисление ошибки второго скрытого слоя
        hidden2_errors = np.dot(output_errors, self.weights3.T) * \
                        self.sigmoid_derivative(self.hidden_layer2)
        
        # Вычисление ошибки первого скрытого слоя
        hidden1_errors = np.dot(hidden2_errors, self.weights2.T) * \
                        self.sigmoid_derivative(self.hidden_layer1)
        
        # Обновление весов weights3 (Hidden2 -> Output)
        self.weights3 += self.learning_rate * \
                        np.outer(self.last_hidden_layer2, output_errors)
        
        # Обновление весов weights2 (Hidden1 -> Hidden2)
        self.weights2 += self.learning_rate * \
                        np.outer(self.last_hidden_layer1, hidden2_errors)
        
        # Обновление весов weights1 (Input -> Hidden1)
        self.weights1 += self.learning_rate * \
                        np.outer(self.last_input_layer, hidden1_errors)
    
    def train(self, input_data: np.ndarray, expected_output: np.ndarray, 
              epochs: int = 1000, verbose: bool = True) -> List[float]:
        """
        Обучение сети на одном примере
        
        Args:
            input_data: Входные данные для обучения
            expected_output: Ожидаемые выходные данные
            epochs: Количество эпох обучения
            verbose: Выводить ли информацию о процессе обучения
            
        Returns:
            Список ошибок для каждой эпохи
        """
        error_history = []
        
        if verbose:
            print("\n--- Начало обучения ---")
            print(f"Ожидаемый выход: {expected_output}")
        
        # Начальное состояние (эпоха 0)
        self.forward_propagation(input_data)
        initial_error = np.sum((expected_output - self.output_layer) ** 2)
        error_history.append(initial_error)
        
        if verbose:
            print(f"\nЭпоха 0/{epochs}")
            print(f"Ошибка: {initial_error:.6f}")
        
        # Основной цикл обучения
        for epoch in range(1, epochs + 1):
            self.forward_propagation(input_data)
            self.backpropagate(expected_output)
            
            # Вычисление текущей ошибки
            self.forward_propagation(input_data)
            current_error = np.sum((expected_output - self.output_layer) ** 2)
            error_history.append(current_error)
            
            # Вывод информации
            if verbose and (epoch == 1 or epoch % 100 == 0 or epoch == epochs):
                print(f"\nЭпоха {epoch}/{epochs}")
                print(f"Ошибка: {current_error:.6f}")
        
        if verbose:
            print("\n--- Обучение завершено ---")
        
        return error_history
    
    def train_on_dataset(self, training_samples: List[np.ndarray], 
                        epochs: int = 10, verbose: bool = True) -> List[float]:
        """
        Обучение сети на множестве примеров для лучшего обобщения
        
        Args:
            training_samples: Список обучающих примеров (каждый пример - это массив)
            epochs: Количество эпох обучения
            verbose: Выводить ли информацию о процессе обучения
            
        Returns:
            Список средних ошибок для каждой эпохи
        """
        error_history = []
        num_samples = len(training_samples)
        
        if verbose:
            print("\n--- Начало обучения на множестве примеров ---")
            print(f"Количество примеров: {num_samples}")
            print(f"Количество эпох: {epochs}")
        
        # Вычисление начальной ошибки
        total_error = 0
        for sample in training_samples:
            self.forward_propagation(sample)
            error = np.sum((sample - self.output_layer) ** 2)
            total_error += error
        avg_error = total_error / num_samples
        error_history.append(avg_error)
        
        if verbose:
            print(f"\nЭпоха 0/{epochs}")
            print(f"Средняя ошибка: {avg_error:.6f}")
        
        # Основной цикл обучения
        for epoch in range(1, epochs + 1):
            total_error = 0
            
            # Обучение на каждом примере
            for sample in training_samples:
                # Для задачи identity function: выход должен быть равен входу
                self.forward_propagation(sample)
                self.backpropagate(sample)
                
                # Вычисляем ошибку
                prediction = self.output_layer
                error = np.sum((sample - prediction) ** 2)
                total_error += error
            
            avg_error = total_error / num_samples
            error_history.append(avg_error)
            
            # Вывод информации
            if verbose and (epoch == 1 or epoch % 2 == 0 or epoch == epochs):
                print(f"\nЭпоха {epoch}/{epochs}")
                print(f"Средняя ошибка: {avg_error:.6f}")
        
        if verbose:
            print("\n--- Обучение завершено ---")
        
        return error_history
    
    def predict(self, input_data: np.ndarray) -> np.ndarray:
        """
        Предсказание для новых данных
        
        Args:
            input_data: Входные данные
            
        Returns:
            Предсказанные выходные данные
        """
        return self.forward_propagation(input_data)
    
    def get_network_state(self) -> dict:
        """
        Получить текущее состояние сети
        
        Returns:
            Словарь с состоянием всех слоев
        """
        return {
            'input_layer': self.input_layer.copy(),
            'hidden_layer1': self.hidden_layer1.copy(),
            'hidden_layer2': self.hidden_layer2.copy(),
            'output_layer': self.output_layer.copy()
        }
    
    def print_state(self):
        """Вывод текущего состояния сети"""
        print("\nВходной слой:")
        print(self.input_layer)
        print("\nСкрытый слой 1:")
        print(self.hidden_layer1)
        print("\nСкрытый слой 2:")
        print(self.hidden_layer2)
        print("\nВыходной слой (предсказание):")
        print(self.output_layer)


def main():
    """Основная функция для тестирования"""
    print("=" * 50)
    print("Тестирование нейронной сети")
    print("=" * 50)
    
    # Создание нейронной сети: 10 входов, 100 нейронов в первом скрытом слое,
    # 100 нейронов во втором скрытом слое, 10 выходов
    nn = NeuralNetwork(10, 100, 100, 10, learning_rate=0.1)
    
    # Генерация обучающих данных
    print("\n--- Генерация обучающих данных ---")
    np.random.seed(42)
    num_samples = 325
    training_samples = []
    
    for i in range(num_samples):
        # Генерируем случайные данные в диапазоне [0, 1] (только положительные)
        sample = np.random.uniform(0, 1, 10)
        training_samples.append(sample)
    
    print(f"Создано {num_samples} обучающих примеров")
    
    # Обучение сети на множестве примеров
    print("\nОбучение займет некоторое время...")
    error_history = nn.train_on_dataset(training_samples, epochs=500, verbose=False)
    print(f"Обучение завершено! Финальная ошибка: {error_history[-1]:.6f}")
    
    # Тестирование на оригинальных данных
    print("\n" + "=" * 50)
    print("ТЕСТИРОВАНИЕ")
    print("=" * 50)
    
    # Тест 1: Оригинальные обучающие данные
    print("\n--- Тест 1: Оригинальные данные ---")
    test1_input = np.array([0.82, 0.68, 0.58, 0.52, 0.5, 0.52, 0.58, 0.68, 0.82, 1.0])
    test1_prediction = nn.predict(test1_input)
    test1_error = np.sum((test1_input - test1_prediction) ** 2)
    
    print(f"Вход:        {test1_input}")
    print(f"Предсказание: {test1_prediction}")
    print(f"Ошибка: {test1_error:.6f}")
    print(f"Макс. разница: {np.max(np.abs(test1_input - test1_prediction)):.6f}")
    
    # Тест 2: Новые тестовые данные (только положительные)
    print("\n--- Тест 2: Новые тестовые данные ---")
    test2_input = np.array([0.28, 0.15, 0.32, 0.08, 0.0, 0.08, 0.32, 0.72, 0.28, 1.0])
    test2_prediction = nn.predict(test2_input)
    test2_error = np.sum((test2_input - test2_prediction) ** 2)
    
    print(f"Вход:        {test2_input}")
    print(f"Предсказание: {test2_prediction}")
    print(f"Ошибка: {test2_error:.6f}")
    print(f"Макс. разница: {np.max(np.abs(test2_input - test2_prediction)):.6f}")
    
    # Тест 3: Случайные новые данные (только положительные)
    print("\n--- Тест 3: Случайные новые данные ---")
    np.random.seed(123)  # Другой seed для разнообразия
    test3_input = np.random.uniform(0, 1, 10)
    test3_prediction = nn.predict(test3_input)
    test3_error = np.sum((test3_input - test3_prediction) ** 2)
    
    print(f"Вход:        {test3_input}")
    print(f"Предсказание: {test3_prediction}")
    print(f"Ошибка: {test3_error:.6f}")
    print(f"Макс. разница: {np.max(np.abs(test3_input - test3_prediction)):.6f}")
    
    # Сводная информация
    print("\n" + "=" * 50)
    print("Сводная информация")
    print("=" * 50)
    
    print(f"\nАрхитектура: {nn.input_size}-{nn.hidden_size1}-{nn.hidden_size2}-{nn.output_size}")
    print(f"Обучено на {num_samples} примерах")
    print(f"Финальная средняя ошибка: {error_history[-1]:.6f}")
    
    avg_test_error = (test1_error + test2_error + test3_error) / 3
    print(f"\nСредняя ошибка на тестах: {avg_test_error:.6f}")
    
    if avg_test_error < 0.5:
        print("\n✅ Сеть хорошо обобщает! Ошибка на тестах минимальная.")
    else:
        print("\n⚠️  Сеть работает, но требует больше обучения.")
    
    print("\n" + "=" * 50)



if __name__ == "__main__":
    main()
