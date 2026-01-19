"""
Проверка корректности Python реализации
Сравнение с ожидаемым поведением
"""
import numpy as np
from neural_network import NeuralNetwork

print("=" * 70)
print("ПРОВЕРКА КОРРЕКТНОСТИ РЕАЛИЗАЦИИ")
print("=" * 70)

# Создание сети с фиксированным seed для воспроизводимости
nn = NeuralNetwork(10, 100, 100, 10, learning_rate=0.1)

# Обучающие данные (как в оригинале)
training_input = np.array([0.82, 0.68, 0.58, 0.52, 0.5, 0.52, 0.58, 0.68, 0.82, 1.0])
training_output = np.array([0.82, 0.68, 0.58, 0.52, 0.5, 0.52, 0.58, 0.68, 0.82, 1.0])

print("\n📚 ОБУЧАЮЩИЕ ДАННЫЕ:")
print(f"Вход:  {training_input}")
print(f"Выход: {training_output}")

# Обучение (500 эпох, как в оригинале)
print("\n🚀 ОБУЧЕНИЕ (500 эпох)...")
error_history = nn.train(training_input, training_output, epochs=500, verbose=False)

print(f"✅ Обучение завершено!")
print(f"   Начальная ошибка: {error_history[0]:.6f}")
print(f"   Финальная ошибка: {error_history[-1]:.6f}")
print(f"   Улучшение: {((error_history[0] - error_history[-1]) / error_history[0] * 100):.2f}%")

# Финальное предсказание на обучающих данных
print("\n" + "=" * 70)
print("РЕЗУЛЬТАТ ОБУЧЕНИЯ")
print("=" * 70)
final_pred = nn.predict(training_input)
print(f"\nВход:        {training_input}")
print(f"Ожидаемое:   {training_output}")
print(f"Предсказание: {final_pred}")
print(f"\nПоэлементная разница:")
for i in range(10):
    diff = training_output[i] - final_pred[i]
    print(f"  [{i}]: ожидаемое={training_output[i]:.4f}, получено={final_pred[i]:.4f}, разница={diff:+.4f}")

# Тестирование на новых данных
print("\n" + "=" * 70)
print("ТЕСТИРОВАНИЕ НА НОВЫХ ДАННЫХ")
print("=" * 70)
test_input = np.array([0.28, -0.28, -0.68, -0.92, -1.0, -0.92, -0.68, -0.28, 0.28, 1.0])
test_pred = nn.predict(test_input)

print(f"\nВход:        {test_input}")
print(f"Предсказание: {test_pred}")

print("\n" + "=" * 70)
print("АНАЛИЗ")
print("=" * 70)

# Проверка 1: Обучение должно уменьшить ошибку
if error_history[-1] < error_history[0]:
    print("✅ Обучение работает: ошибка уменьшилась")
else:
    print("❌ Обучение НЕ работает: ошибка не уменьшилась!")

# Проверка 2: Финальная ошибка должна быть достаточно малой
if error_history[-1] < 0.01:
    print(f"✅ Сеть хорошо обучилась: ошибка {error_history[-1]:.6f} < 0.01")
elif error_history[-1] < 0.1:
    print(f"⚠️  Сеть обучилась удовлетворительно: ошибка {error_history[-1]:.6f} < 0.1")
else:
    print(f"❌ Сеть плохо обучилась: ошибка {error_history[-1]:.6f} >= 0.1")

# Проверка 3: Предсказание должно быть близко к ожидаемому
max_diff = np.max(np.abs(training_output - final_pred))
if max_diff < 0.05:
    print(f"✅ Предсказание очень точное: макс. разница {max_diff:.6f} < 0.05")
elif max_diff < 0.2:
    print(f"⚠️  Предсказание приемлемое: макс. разница {max_diff:.6f} < 0.2")
else:
    print(f"❌ Предсказание неточное: макс. разница {max_diff:.6f} >= 0.2")

print("\n" + "=" * 70)
print("ВЫВОД:")
print("=" * 70)
print("""
Нейронная сеть обучается на ОДНОМ примере (это нормально для данного задания).
Она должна:
1. Хорошо предсказывать обучающий пример
2. Давать какой-то результат на новых данных (но не обязательно правильный)

Это НЕ задача обобщения (generalization), а задача запоминания (memorization).
Сеть запоминает конкретный паттерн, а не учится общему правилу.
""")
print("=" * 70)
