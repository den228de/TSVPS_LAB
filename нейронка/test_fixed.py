"""
Исправленная версия обучения нейронной сети
Обучение на множестве примеров для избежания переобучения
"""
import numpy as np
from neural_network import NeuralNetwork

print("=" * 70)
print("ПРАВИЛЬНОЕ ОБУЧЕНИЕ - НА МНОЖЕСТВЕ ПРИМЕРОВ")
print("=" * 70)

# Создание нейронной сети
nn = NeuralNetwork(10, 100, 100, 10, learning_rate=0.1)

# Генерация множества обучающих примеров
# Для задачи "выход = вход" нужно много разных примеров
print("\n📚 Генерация обучающих данных...")
np.random.seed(42)
num_samples = 100  # Количество обучающих примеров

training_samples = []
for i in range(num_samples):
    # Генерируем случайные входные данные в диапазоне [-1, 1]
    sample = np.random.uniform(-1, 1, 10)
    training_samples.append(sample)

print(f"Создано {num_samples} обучающих примеров")

# Обучение на всех примерах
print("\n🚀 Обучение сети...")
epochs_per_sample = 10  # Эпох на каждый пример

for epoch in range(epochs_per_sample):
    total_error = 0
    for sample in training_samples:
        nn.forward_propagation(sample)
        nn.backpropagate(sample)  # Выход должен быть = вход
        
        # Вычисляем ошибку
        prediction = nn.output_layer
        error = np.sum((sample - prediction) ** 2)
        total_error += error
    
    avg_error = total_error / num_samples
    if epoch % 2 == 0 or epoch == epochs_per_sample - 1:
        print(f"Эпоха {epoch + 1}/{epochs_per_sample}, Средняя ошибка: {avg_error:.6f}")

print("✅ Обучение завершено!")

# Тестирование
print("\n" + "=" * 70)
print("ТЕСТИРОВАНИЕ")
print("=" * 70)

# Тест 1: Оригинальные данные
print("\n✅ ТЕСТ 1: Оригинальные обучающие данные")
test1_input = np.array([0.82, 0.68, 0.58, 0.52, 0.5, 0.52, 0.58, 0.68, 0.82, 1.0])
test1_pred = nn.predict(test1_input)
test1_error = np.sum((test1_input - test1_pred) ** 2)
print(f"Вход:        {test1_input}")
print(f"Предсказание: {test1_pred}")
print(f"Ошибка: {test1_error:.6f}")
print(f"Макс. разница: {np.max(np.abs(test1_input - test1_pred)):.6f}")

# Тест 2: Новые данные
print("\n✅ ТЕСТ 2: Новые тестовые данные")
test2_input = np.array([0.28, -0.28, -0.68, -0.92, -1.0, -0.92, -0.68, -0.28, 0.28, 1.0])
test2_pred = nn.predict(test2_input)
test2_error = np.sum((test2_input - test2_pred) ** 2)
print(f"Вход:        {test2_input}")
print(f"Предсказание: {test2_pred}")
print(f"Ошибка: {test2_error:.6f}")
print(f"Макс. разница: {np.max(np.abs(test2_input - test2_pred)):.6f}")

# Тест 3: Нули
print("\n✅ ТЕСТ 3: Все нули")
test3_input = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
test3_pred = nn.predict(test3_input)
test3_error = np.sum((test3_input - test3_pred) ** 2)
print(f"Вход:        {test3_input}")
print(f"Предсказание: {test3_pred}")
print(f"Ошибка: {test3_error:.6f}")

# Тест 4: Единицы
print("\n✅ ТЕСТ 4: Все единицы")
test4_input = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0])
test4_pred = nn.predict(test4_input)
test4_error = np.sum((test4_input - test4_pred) ** 2)
print(f"Вход:        {test4_input}")
print(f"Предсказание: {test4_pred}")
print(f"Ошибка: {test4_error:.6f}")

# Тест 5: Случайные новые данные
print("\n✅ ТЕСТ 5: Случайные новые данные")
test5_input = np.random.uniform(-1, 1, 10)
test5_pred = nn.predict(test5_input)
test5_error = np.sum((test5_input - test5_pred) ** 2)
print(f"Вход:        {test5_input}")
print(f"Предсказание: {test5_pred}")
print(f"Ошибка: {test5_error:.6f}")

print("\n" + "=" * 70)
print("РЕЗУЛЬТАТЫ:")
print("=" * 70)

# Проверка всех тестов
all_errors = [test1_error, test2_error, test3_error, test4_error, test5_error]
avg_test_error = np.mean(all_errors)
max_test_error = np.max(all_errors)

print(f"Средняя ошибка на тестах: {avg_test_error:.6f}")
print(f"Максимальная ошибка: {max_test_error:.6f}")

if max_test_error < 0.5:
    print("\n✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ! Сеть работает корректно!")
else:
    print(f"\n⚠️  Сеть работает, но есть ошибки. Нужно больше эпох обучения.")

print("=" * 70)
