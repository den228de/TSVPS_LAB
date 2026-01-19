"""
Тестовый скрипт для проверки нейронной сети
"""
import numpy as np
from neural_network import NeuralNetwork

print("=" * 60)
print("ТЕСТИРОВАНИЕ НЕЙРОННОЙ СЕТИ")
print("=" * 60)

# Создание нейронной сети
print("\n1. Создание нейронной сети...")
nn = NeuralNetwork(10, 100, 100, 10, learning_rate=0.1)
print("   ✓ Сеть создана: 10 → 100 → 100 → 10")

# Обучающие данные
training_input = np.array([0.82, 0.68, 0.58, 0.52, 0.5, 0.52, 0.58, 0.68, 0.82, 1.0])
training_output = np.array([0.82, 0.68, 0.58, 0.52, 0.5, 0.52, 0.58, 0.68, 0.82, 1.0])

print("\n2. Обучающие данные:")
print(f"   Вход:  {training_input}")
print(f"   Выход: {training_output}")

# Начальное предсказание (до обучения)
print("\n3. Предсказание ДО обучения:")
initial_prediction = nn.forward_propagation(training_input)
initial_error = np.sum((training_output - initial_prediction) ** 2)
print(f"   Предсказание: {initial_prediction}")
print(f"   Ошибка: {initial_error:.6f}")

# Обучение
print("\n4. Обучение сети (500 эпох)...")
error_history = nn.train(training_input, training_output, epochs=500, verbose=False)
print(f"   ✓ Обучение завершено")

# Финальное предсказание (после обучения)
print("\n5. Предсказание ПОСЛЕ обучения:")
final_prediction = nn.forward_propagation(training_input)
final_error = np.sum((training_output - final_prediction) ** 2)
print(f"   Предсказание: {final_prediction}")
print(f"   Ошибка: {final_error:.6f}")
print(f"   Улучшение: {((initial_error - final_error) / initial_error * 100):.2f}%")

# Тестирование на новых данных
print("\n6. Тестирование на НОВЫХ данных:")
test_input = np.array([0.28, -0.28, -0.68, -0.92, -1.0, -0.92, -0.68, -0.28, 0.28, 1.0])
test_prediction = nn.predict(test_input)
print(f"   Вход:        {test_input}")
print(f"   Предсказание: {test_prediction}")

# Проверка результатов
print("\n" + "=" * 60)
print("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
print("=" * 60)

# Проверка 1: Ошибка должна уменьшиться
if final_error < initial_error:
    print("✓ ТЕСТ 1 ПРОЙДЕН: Ошибка уменьшилась после обучения")
else:
    print("✗ ТЕСТ 1 НЕ ПРОЙДЕН: Ошибка не уменьшилась!")

# Проверка 2: Финальная ошибка должна быть достаточно малой
if final_error < 0.1:
    print(f"✓ ТЕСТ 2 ПРОЙДЕН: Финальная ошибка мала ({final_error:.6f} < 0.1)")
else:
    print(f"✗ ТЕСТ 2 НЕ ПРОЙДЕН: Финальная ошибка слишком велика ({final_error:.6f} >= 0.1)")

# Проверка 3: Предсказание должно быть близко к ожидаемому
max_diff = np.max(np.abs(training_output - final_prediction))
if max_diff < 0.2:
    print(f"✓ ТЕСТ 3 ПРОЙДЕН: Предсказание близко к ожидаемому (макс. разница: {max_diff:.6f})")
else:
    print(f"✗ ТЕСТ 3 НЕ ПРОЙДЕН: Предсказание далеко от ожидаемого (макс. разница: {max_diff:.6f})")

# Проверка 4: Тестовое предсказание должно быть в разумных пределах
if np.all(test_prediction >= -2) and np.all(test_prediction <= 2):
    print("✓ ТЕСТ 4 ПРОЙДЕН: Тестовое предсказание в разумных пределах")
else:
    print("✗ ТЕСТ 4 НЕ ПРОЙДЕН: Тестовое предсказание выходит за пределы")

print("\n" + "=" * 60)
