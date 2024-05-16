# 2.1---------------------------
# Создайте функцию pair(head, tail), которая порождает элемент списка. Не используйте ветвления.
# Создайте также функции head(lst) (возвращает значение головы списка) и tail(lst) (возвращает хвост списка).

def pair(head, tail=None):
    return lambda i: head if i == 0 else tail


def head(args):
    return args(0)


def tail(args):
    return args(1)


# 2.2----------------------------------
# Создайте функцию make_list(*args), которая создает список на основе аргументов.
def make_list(*args):
    if not args:
        return None
    elif callable(args[0]):
        return args[0]
    else:
        return pair(args[0], make_list(*args[1:]))


def print_list(lst):
    if callable(lst):
        print(lst(0), end=' ')
        print_list(lst(1))
    else:
        print(lst)


if __name__ == "__main__":
    print("Ex 6.2.2: ")
    my_list = make_list(1, 2, 3, 4, 5)
    print_list( my_list)


# 2.3----------------------------------
# Создайте функцию list_to_string(lst), возвращающую строку, содержащую элементы списка.
def list_to_string(lst) -> str:
    if callable(lst):
        return str(lst(0)) + " " + list_to_string(lst(1))
    else:
        return ""


if __name__ == "__main__":
    print("Ex 6.2.3: ", list_to_string(make_list(1, 2, 3, 4, 5)))


# 2.4----------------------------------
#Создайте функцию list_range(low, high), возвращающую список чисел от low до high включительно.
def list_range(low, high):
    if low > high:
        high = low
    return make_list(*range(low, high + 1))


if __name__ == "__main__":
    print("Ex 6.2.4: ",list_to_string(list_range(1, 7)))


# 2.5----------------------------------
#Создайте функцию foldl(func, lst, acc), вычисляющую свертку элементов списка, аналогично reduce.
#foldl - Функция высшего порядка,
# которая производит преобразование структуры данных
# к единственному атомарному значению при помощи заданной функции.
def foldl(func, lst):
    if callable(tail(lst)):
        if lst(1)(0) is not None:
            return foldl(func, make_list(func(lst(0), lst(1)(0)), tail(tail(lst))))
    return lst(0)


if __name__ == "__main__":
    print("Ex 6.2.5: ",foldl(lambda x, y: x + y, list_range(1, 10)))


# 2.6----------------------------------
#Создайте функцию list_sum(lst) для вычисления суммы элементов списка с помощью foldl.
def list_sum(lst):
    return foldl(lambda x, y: x + y, lst)


if __name__ == "__main__":
    print("Ex 6.2.6: ",list_sum(list_range(1, 100)))


# 2.7----------------------------------
#Создайте функцию fact(n) для вычисления факториала с помощью foldl и list_range.
def fact(n):
    return foldl(lambda x, y: x * y, list_range(1, n))


if __name__ == "__main__":
    print("Ex 6.2.7: ",fact(6))


# 2.8----------------------------------
#Создайте функцию list_to_py(lst) для преобразования списка в обычный список Питона с помощью foldl.
def list_to_py(lst) -> list:
    def sum_list(list1, list2):
        if not type(list1) is list:
            list1 = [list1]
        if not type(list2) is list:
            list2 = [list2]

        list1.extend(list2)
        return list1

    return foldl(sum_list, lst)


if __name__ == "__main__":
    print("Ex 6.2.8: ",list_to_py(make_list(1, 2, "3", -4, 5, dict(next=6), 7)))


# 2.14----------------------------------
#Создайте функцию list_concat(lst1, lst2) для соединения двух списков.
def concat(xs, ys):
    if xs is None:
        return ys
    else:
        return pair(head(xs), concat(tail(xs), ys))


if __name__ == "__main__":
    print("Ex 6.2.14: ")
    print_list(concat(make_list(1, 2, 3), make_list(9, 8, 7)))


# 2.9----------------------------------
#Создайте функцию list_reverse(lst) для разворота списка в обратном направлении с помощью foldl.
def list_reverse(lst):
    if lst is None:
        return lst
    else:
        return concat(list_reverse(tail(lst)), pair(head(lst), None))


def print_list(lst):
    if callable(lst):
        print_list(lst(0))
        print_list(lst(1))
    elif lst is not None:
        print(lst, end=' ')


if __name__ == "__main__":
    print("Ex 6.2.9: ")
    print_list(list_reverse(make_list(1, 2, 3, 4, 5, 6)))


# 2.10----------------------------------
#Создайте функцию foldr(func, lst, acc), вычисляющую свертку справа для элементов списка.
def make_list(*args):
    if not args:
        return None
    elif callable(args[0]):
        return args[0]
    else:
        return pair(args[0], make_list(*args[1:]))


def foldl(func, lst):
    if callable(tail(lst)):
        if lst(1)(0) is not None:
            return foldl(func, make_list(func(lst(0), lst(1)(0)), tail(tail(lst))))
    return lst(0)


def foldr(func, lst):
    return foldl(func, list_reverse(lst))


if __name__ == "__main__":
    print("Ex 6.2.10: ")
    print(foldr(lambda x, y: x + y, list_range(1, 10)))
    print(foldr(lambda x, y: x - y, list_range(1, 10)))
    print(foldr(lambda x, y: x * y, list_range(1, 7)))


# 2.11----------------------------------
#Создайте функцию list_map(func, lst), аналог map, с помощью foldr.
def list_map(func, lst):
    if not lst:
        return lst
    if not lst(0):
        return list_map(func, lst(1))
    return make_list(func(lst(0)), list_map(func, lst(1)))


if __name__ == "__main__":
    print("Ex 6.2.11: ")
    print_list(list_map(lambda x: x * 2 + 3, make_list(10, 15, 21, 33, 42, 55)))


# 2.12----------------------------------
#Создайте функцию list_filter(pred, lst), аналог filter, с помощью foldr.
def list_filter(func, lst):
    if lst is None:
        return lst
    elif not func(lst(0)):
        return list_filter(func, lst(1))
    return make_list(lst(0), list_filter(func, lst(1)))


if __name__ == "__main__":
    print("Ex 6.2.12: ")
    print([11, False, 18, 21, "", 12, 34, 0, [], {}])
    print_list(list_filter(lambda x: bool(x), make_list(11, False, 18, 21, "", 12, 34, 0, [], {})))
    print()
    print_list(list_filter(lambda x: x[0].lower() in 'aeiou', make_list("Petya", "Alesha", "Vasya", "Misha", "Olezha")))


# 2.13----------------------------------
#Создайте функцию sum_odd_squares для вычисления суммы квадратов нечетных чисел списка с помощью list_sum, list_map и list_filter.
def sum_odd_squares(lst):
    return list_sum(list_map(lambda x: x ** 2, list_filter(lambda y: y % 2 == 1, lst)))


if __name__ == "__main__":
    print("Ex 6.2.13: ")
    print(sum_odd_squares(list_range(1, 10)))

    a = []
    for i in range(11):
        if i % 2 == 1:
            a.append(i ** 2)
    print(sum(a))


# 2.15----------------------------------
#Создайте функцию list_replace(lst, index, value) для изменения элемента списка по индексу.
def list_replace(lst, index, value):
    if index == 0:
        return make_list(value, lst(1))
    return make_list(lst(0), list_replace(lst(1), index - 1, value))


if __name__ == "__main__":
    print("Ex 6.2.15: ")
    a = list_range(1, 10)
    print_list(a)
    print()
    print_list(list_replace(a, 4, "LET'S GO!!!"))
