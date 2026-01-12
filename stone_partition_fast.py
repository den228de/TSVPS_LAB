"""
Быстрая версия для тестирования GUI (уменьшенное количество итераций)
"""

import random
from typing import List, Tuple


def brute_force_partition(stones: List[int], n: int) -> Tuple[List[int], List[int]]:
    """Полный перебор всех возможных разбиений"""
    min_diff = float('inf')
    best_partition = ([], [])
    
    for i in range(1 << n):
        group1 = []
        group2 = []
        sum1 = 0
        sum2 = 0
        
        for j in range(n):
            if (i >> j) & 1:
                group1.append(stones[j])
                sum1 += stones[j]
            else:
                group2.append(stones[j])
                sum2 += stones[j]
        
        diff = abs(sum1 - sum2)
        if diff < min_diff:
            min_diff = diff
            best_partition = (group1, group2)
    
    return best_partition


def greedy_partition(stones: List[int]) -> Tuple[List[int], List[int]]:
    """Эвристический алгоритм"""
    sorted_stones = stones.copy()
    n = len(sorted_stones)
    
    for i in range(n):
        for j in range(n - 1, i, -1):
            if sorted_stones[j] < sorted_stones[j - 1]:
                sorted_stones[j], sorted_stones[j - 1] = sorted_stones[j - 1], sorted_stones[j]
    
    group1 = []
    group2 = []
    sum1 = 0
    sum2 = 0
    
    for i in range(n - 1, -1, -1):
        if sum1 < sum2:
            group1.append(sorted_stones[i])
            sum1 += sorted_stones[i]
        else:
            group2.append(sorted_stones[i])
            sum2 += sorted_stones[i]
    
    return group1, group2


def run_tests():
    """Быстрая версия тестов для GUI (меньше итераций)"""
    random.seed(42)
    
    results = {
        'brute_force': [[], [], []],
        'greedy': [[], [], []],
        'difference': [[], [], []]
    }
    
    buff = 10
    
    for complexity_level in range(3):
        print(f"\n{'='*70}")
        print(f"Уровень сложности {complexity_level + 1}: Вес камней от 1 до {buff}")
        print(f"{'='*70}")
        
        stone_count = 5
        
        # Уменьшено до 7 размеров (вместо 10) и до 15 камней max (вместо 23)
        for size_idx in range(7):
            bf_results = []
            greedy_results = []
            diff_results = []
            
            # Уменьшено до 5 итераций (вместо 10)
            for iteration in range(5):
                stones = [random.randint(1, buff) for _ in range(stone_count)]
                total_weight = sum(stones)
                
                bf_partition = brute_force_partition(stones, stone_count)
                bf_diff = abs(sum(bf_partition[0]) - sum(bf_partition[1]))
                bf_percent = (bf_diff / total_weight) * 100
                bf_results.append(bf_percent)
                
                greedy_partition_result = greedy_partition(stones)
                greedy_diff = abs(sum(greedy_partition_result[0]) - sum(greedy_partition_result[1]))
                greedy_percent = (greedy_diff / total_weight) * 100
                greedy_results.append(greedy_percent)
                
                diff_results.append(abs(bf_percent - greedy_percent))
            
            avg_bf = sum(bf_results) / 5
            avg_greedy = sum(greedy_results) / 5
            avg_diff = sum(diff_results) / 5
            
            results['brute_force'][complexity_level].append(avg_bf)
            results['greedy'][complexity_level].append(avg_greedy)
            results['difference'][complexity_level].append(avg_diff)
            
            print(f"Камней: {stone_count:2d} | Перебор: {avg_bf:5.2f}% | Эвристика: {avg_greedy:5.2f}% | Разница: {avg_diff:5.2f}%")
            
            stone_count += 2
        
        buff *= 2
    
    print(f"\n{'='*70}")
    print("ИТОГОВЫЕ СРЕДНИЕ ЗНАЧЕНИЯ ПО ВСЕМ РАЗМЕРАМ")
    print(f"{'='*70}")
    
    for complexity_level in range(3):
        weight_range = 10 * (2 ** complexity_level)
        bf_avg = sum(results['brute_force'][complexity_level]) / len(results['brute_force'][complexity_level])
        greedy_avg = sum(results['greedy'][complexity_level]) / len(results['greedy'][complexity_level])
        diff_avg = sum(results['difference'][complexity_level]) / len(results['difference'][complexity_level])
        
        print(f"\nВес 1-{weight_range}:")
        print(f"  Перебор:    {bf_avg:.4f}%")
        print(f"  Эвристика:  {greedy_avg:.4f}%")
        print(f"  Разница:    {diff_avg:.4f}%")
    
    # Дополняем результаты до 10 точек для графиков (копируем последние значения)
    for complexity_level in range(3):
        while len(results['brute_force'][complexity_level]) < 10:
            results['brute_force'][complexity_level].append(results['brute_force'][complexity_level][-1])
            results['greedy'][complexity_level].append(results['greedy'][complexity_level][-1])
            results['difference'][complexity_level].append(results['difference'][complexity_level][-1])
    
    return results


if __name__ == "__main__":
    print("Запуск быстрого тестирования для GUI...")
    results = run_tests()
    print("\n✓ Тестирование завершено!")
