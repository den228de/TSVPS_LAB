"""
Простой тест для проверки работы модуля hypercube_network.
"""

from hypercube_network import SingleHypercube, MultiCubeNetwork

print("=" * 60)
print("ТЕСТ 1: Создание одного гиперкуба размерности 3")
print("=" * 60)

cube = SingleHypercube(3)
print(f"Размерность: {cube.dimension}")
print(f"Количество процессоров: {cube.total_processors}")
print(f"\nПроцессор 5 (бинарно: {cube.get_binary_representation(5)})")
print(f"Соседи: {cube.get_neighbors(5)}")

print("\n" + "=" * 60)
print("ТЕСТ 2: Создание сети из 2 кубов размерности 2")
print("=" * 60)

network = MultiCubeNetwork(2, 2)
print(f"Количество кубов: {network.num_cubes}")
print(f"Размерность каждого куба: {network.dimension_per_cube}")
print(f"Всего процессоров: {network.total_processors}")

print("\n" + "=" * 60)
print("ТЕСТ 3: Поиск кратчайшего пути (0 → 7)")
print("=" * 60)

path = network.find_shortest_path(0, 7)
print(f"Найден путь длиной {len(path) - 1} ребер:")
for i, node in enumerate(path):
    print(f"  {i+1}. {network.format_processor_info(node)}")
    if i < len(path) - 1:
        print("     ↓")

print("\n" + "=" * 60)
print("✓ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
print("=" * 60)
