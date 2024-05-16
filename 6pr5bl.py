filename = 'messages.csv'

# 5.1//////////////////////////
def scan(filename):
    with open(filename, 'r') as file:
        for line in file:
            yield line.strip().split(',')

for row in scan(filename):
    print(row)


# 5.2//////////////////////////////////////
def print_table(parent):
    for row in parent:
        print(row)

data = [[1, 'Alice'], [2, 'Bob']]
print_table(data)


# 5.3/////////////////////////
def eq(x, y):
    return x == y

def ne(x, y):
    return x != y

def value(x):
    return x

def field(x):
    return x

def filter_gen(pred, filename):
    for row in scan(filename):
        if pred(*row):
            yield row

filtered_data = filter_gen(eq, filename)
for row in filtered_data:
    print(row)


# 5.4///////////////////////////
def project(new_schema, parent_schema, parent):
    indices = [parent_schema.index(col) for col in new_schema]
    for row in parent:
        yield [row[i] for i in indices]

data = [['Alice', 25, 'Engineer'], ['Bob', 30, 'Doctor']]
for row in project(['Name', 'Age'], ['Name', 'Age', 'Occupation'], data):
    print(row)


# 5.5///////////////////////////////////////////
def join(left, right):
    for row_left in left:
        for row_right in right:
            if row_left[0] == row_right[0]:  # Сравниваем по ключу (например, time)
                yield row_left + row_right[1:]  # Объединяем строки

left_data = [[1, 'A'], [2, 'B']]
right_data = [[1, 'X'], [2, 'Y']]
for row in join(left_data, right_data):
    print(row)