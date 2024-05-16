from copy import deepcopy
from random import randint


# Функция перехода из комнаты в комнату
def go(room):
    def func(state):
        return dict(state, room=room)

    return func


# Структура игры. Комнаты и допустимые в них действия
game = {
    'room0': dict(
        left=go('room1'),
        up=go('room2'),
        right=go('room3')
    ),
    'room1': dict(
        up=go('room2'),
        right=go('room0')
    ),
    'room2': dict(
    ),
    'room3': dict(
        up=go('room4'),
        right=go('room5')
    ),
    'room4': dict(
        down=go('room3'),
        right=go('room5')
    ),
    'room5': dict(
        up=go('room4'),
        left=go('room3')
    )
}

# Стартовое состояние
START_STATE = dict(room='room0')


def is_goal_state(state):
    '''
    Проверить, является ли состояние целевым.
    '''
    return state['room'] == 'room2'


def get_current_room(state):
    '''
    Выдать комнату, в которой находится игрок.
    '''
    return state['room']


from collections import deque


def make_model(game, start_state):
    graph = {}  # Инициализация графа
    visited = set()  # Множество посещенных состояний
    queue = deque([start_state])  # Очередь для BFS

    while queue:
        current_state = queue.popleft()  # Берем текущее состояние из очереди

        if current_state['room'] not in visited:

            visited.add(current_state['room'])
            graph[current_state['room']] = {}  # Инициализация переходов из текущей комнаты

            # Проверяем доступные действия в текущей комнате
            for action, transition_func in game[current_state['room']].items():
                new_state = transition_func(current_state)  # Применяем действие
                next_room = new_state['room']

                if next_room not in graph[current_state['room']]:
                    graph[current_state['room']][next_room] = action  # Добавляем переход в граф

                if next_room not in visited:
                    queue.append(new_state)  # Добавляем новое состояние в очередь

    return graph, visited


def has_path(graph, start, goal):
    visited = set()
    queue = deque([start])

    while queue:
        current_room = queue.popleft()

        if current_room in goal:
            return True

        visited.add(current_room)

        # Добавляем в очередь все комнаты, в которые можно перейти из текущей комнаты
        for neighbor_room in graph.get(current_room, {}).keys():
            if neighbor_room not in visited:
                queue.append(neighbor_room)

    return False


def find_dead_ends(graph, goal):
    vertex = graph.keys()
    dead_ends = []
    for vert in vertex:
        if not has_path(graph, vert, goal):
            dead_ends.append(vert)
    return dead_ends


# Проверка работы функции
graph1, visited1 = make_model(game, START_STATE)

n_len_keys = len(visited1)
game['room3']['left'] = go('room0')
graph2, visited2 = make_model(game, START_STATE)
for key in list(graph2.keys()):
    n_key = f"room{int(key[4:]) + n_len_keys}"
    graph2[n_key] = graph2[key]
    del graph2[key]
    for key2 in list(graph2[n_key].keys()):
        n_key2 = f"room{int(key2[4:]) + n_len_keys}"
        graph2[n_key][n_key2] = graph2[n_key][key2]
        del graph2[n_key][key2]


from graphviz import Digraph


def print_dot(graph, start_key, goal_state=None, dead_ends=None):
    dot = Digraph()

    for n, (room, transitions) in enumerate(graph.items()):
        if room == start_key:
            dot.node(str(n), style="filled", fillcolor="dodgerblue", shape="circle")
        elif goal_state and room in goal_state:
            dot.node(str(n), style="filled", fillcolor="green", shape="circle")
        elif dead_ends and room in dead_ends:
            dot.node(str(n), style="filled", fillcolor="red", shape="circle")
        else:
            dot.node(str(n), shape="circle")

    for n, (room, transitions) in enumerate(graph.items()):
        for next_room in transitions.keys():
            m = list(graph.keys()).index(next_room)
            dot.edge(str(n), str(m))

    dot.render('SIXTHREE', format='png', cleanup=True)  # Сохраняем граф в файл 'graph.png'



START_STATE = dict(
    player='alice',
    alice_room='west room',
    bob_room='east room',
    red_key='east room',
    blue_key='west room',
    green_key='east room'
)

from itertools import *


class Room:
    def __init__(self, dictt=None, east=None, west=None, blue=None, red=None):
        if red is None:
            red = []
        if blue is None:
            blue = []
        if west is None:
            west = ["A", "blue"]
        if east is None:

            east = ["B", "green", 'red']
        self.value = {
            "east": east,
            "west": west,
            "blue": blue,
            "red": red,
        }
        if dictt:
            self.value = deepcopy(dictt)

    @staticmethod
    def foo(room, rules):
        cnt = rules.count("A") + rules.count("B")

        states = []
        if cnt == 0:
            return []
        for i in range(2, len(rules) - cnt + 2):
            for j in combinations(rules, i):

                cnt = j.count("A") + j.count("B")
                if cnt != 1:
                    continue
                arr = []
                for k in rules:
                    if not k in j:
                        arr.append(k)
                k = sorted(list(j))
                if room == "east":
                    if "blue" in j:
                        states.append([{"blue": list(j)}, arr])
                    if "green" in j:
                        states.append([{"west": list(j)}, arr])
                elif room == "west":
                    if "red" in j:
                        states.append([{"red": list(j)}, arr])
                    if "green" in j:
                        states.append([{"east": list(j)}, arr])
                elif room == "red":
                    if "red" in j:
                        states.append([{"west": list(j)}, arr])
                elif room == "blue":
                    if "blue" in j:
                        states.append([{"east": list(j)}, arr])
        return states
    def new_states(self):
        states = []

        for a, b in self.value.items():
            state = self.foo(a, b)
            for i in state:

                n_state = deepcopy(self.value)
                n_state[a] = sorted(i[1])
                n_state[list(i[0].keys())[0]] += sorted(list(i[0].values())[0])
                n_state[list(i[0].keys())[0]] = sorted(n_state[list(i[0].keys())[0]])
                if randint(0,100) > 33:
                    if ("A" in n_state["red"] and "blue" in n_state["red"]) :
                        continue
                elif randint(0,100) < 33:
                    if "B" in n_state["blue"] and "red" in n_state["blue"] :
                        continue
                else:
                    if ("B" in n_state["blue"] and "red" in n_state["blue"]) or ("A" in n_state["red"] and "blue" in n_state["red"]):
                        continue

                if not str([str(self.value), str(n_state)]) in edged_str:
                    edged.append([str(self.value), str(n_state)])
                    edged_str.append(str([str(self.value), str(n_state)]))
                if not str(n_state) in rooms_str:
                    rooms.append(Room(dictt=n_state))
                    rooms_str.append(str(n_state))

nodes = []
nodes_str = []
edged = []
edged_str = []
rooms = []
rooms_str = []
r = Room()
rooms.append(r)
rooms_str.append(str(r.value))
nodes.append(r)
nodes_str.append(str(r.value))
r.new_states()
for j in range(100):

    for i in list(rooms)[::]:
        i.new_states()

dott = Digraph()
ii = 0
enumirated_arr = dict()
for i in rooms_str:
    enumirated_arr[i] = str(ii)
    ii += 1
wins = []
looses = []
for i in rooms:
    if "B" in i.value["blue"] and "A" in i.value["red"]:
        wins.append(enumirated_arr[str(i.value)])
    # if ("A" in i.value["red"] and "blue" in i.value["red"]) or ("B" in i.value["blue"] and "red" in i.value["blue"]):
    #     looses.append(enumirated_arr[str(i.value)])

for i in rooms_str:
    if enumirated_arr[i] in wins:
        dott.node(enumirated_arr[i], style = "filled", fillcolor = "green", shape = "circle")
    elif enumirated_arr[i] in looses:
        dott.node(enumirated_arr[i],  style = "filled", fillcolor = "red", shape = "circle")
    elif enumirated_arr[i] == "0":
        dott.node(enumirated_arr[i], style="filled", fillcolor="dodgerblue", shape="circle")

    else:
        dott.node(enumirated_arr[i], shape="circle")
for i in edged:
    dott.edge(enumirated_arr[i[0]], enumirated_arr[i[1]])
dott.render('tttm', format='png', cleanup=True)