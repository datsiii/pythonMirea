def shell_sort(array):
    # Инициализация интервала
    interval = len(array) // 2

    while interval > 0:
        for i in range(interval, len(array)):
            temp = array[i]
            j = i
            # Сортировка подмассива с интервалом interval
            while j >= interval and array[j - interval] > temp:
                array[j] = array[j - interval]
                j -= interval
            array[j] = temp
        # Уменьшение интервала
        interval //= 2


array_size = 8  # Размер массива
array = [12, 4, 5, 6, 1, 8, 3, 2]  # Пример значений массива

# Вызов сортировки Шелла
shell_sort(array)

# Вывод отсортированного массива
print("Отсортированный массив:")
print(array)