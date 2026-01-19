"""
Детальное тестирование нейронной сети
Проверка на переобучение
"""
import numpy as np
from neural_network import NeuralNetwork

print("=" * 70)
print("ДЕТАЛЬНОЕ ТЕСТИРОВАНИЕ - ПРОВЕРКА НА ПЕРЕОБУЧЕНИЕ")
print("=" * 70)

# Создание нейронной сети
nn = NeuralNetwork(10, 100, 100, 10, learning_rate=0.1)

# Обучающие данные
training_input = np.array([0.82, 0.68, 0.58, 0.52, 0.5, 0.52, 0.58, 0.68, 0.82, 1.0])
training_output = np.array([0.82, 0.68, 0.58, 0.52, 0.5, 0.52, 0.58, 0.68, 0.82, 1.0])

print("\n📚 ОБУЧЕНИЕ:")
print(f"Вход:  {training_input}")
print(f"Выход: {training_output}")

# Обучение
error_history = nn.train(training_input, training_output, epochs=500, verbose=False)

# Проверка на обучающих данных
print("\n✅ ТЕСТ 1: Обучающие данные")
train_pred = nn.predict(training_input)
train_error = np.sum((training_output - train_pred) ** 2)
print(f"Вход:        {training_input}")
print(f"Ожидаемое:   {training_output}")
print(f"Предсказание: {train_pred}")
print(f"Ошибка: {train_error:.6f}")
print(f"Макс. разница: {np.max(np.abs(training_output - train_pred)):.6f}")

# Тест 2: Новые данные (должны работать как identity function)
print("\n❌ ТЕСТ 2: Новые данные (тестовые)")
test_input = np.array([0.28, -0.28, -0.68, -0.92, -1.0, -0.92, -0.68, -0.28, 0.28, 1.0])
test_pred = nn.predict(test_input)
test_error = np.sum((test_input - test_pred) ** 2)  # Ожидаем, что выход = вход
print(f"Вход:        {test_input}")
print(f"Ожидаемое:   {test_input}  (должно быть = вход)")
print(f"Предсказание: {test_pred}")
print(f"Ошибка: {test_error:.6f}")
print(f"Макс. разница: {np.max(np.abs(test_input - test_pred)):.6f}")

# Тест 3: Простые данные
print("\n❌ ТЕСТ 3: Простые данные (все нули)")
simple_input = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
simple_pred = nn.predict(simple_input)
simple_error = np.sum((simple_input - simple_pred) ** 2)
print(f"Вход:        {simple_input}")
print(f"Ожидаемое:   {simple_input}")
print(f"Предсказание: {simple_pred}")
print(f"Ошибка: {simple_error:.6f}")

# Тест 4: Единицы
print("\n❌ ТЕСТ 4: Все единицы")
ones_input = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0])
ones_pred = nn.predict(ones_input)
ones_error = np.sum((ones_input - ones_pred) ** 2)
print(f"Вход:        {ones_input}")
print(f"Ожидаемое:   {ones_input}")
print(f"Предсказание: {ones_pred}")
print(f"Ошибка: {ones_error:.6f}")

print("\n" + "=" * 70)
print("ВЫВОДЫ:")
print("=" * 70)
print("❌ ПРОБЛЕМА: Сеть переобучилась на одном примере!")
print("   Она запомнила конкретные значения, но не научилась общему правилу.")
print("\n💡 РЕШЕНИЕ: Нужно обучать на МНОЖЕСТВЕ примеров, а не на одном!")
print("=" * 70)
