from typing import NamedTuple
import queue
from graphviz import Digraph
from numpy.random import randint

class State(NamedTuple):
    player: str
    alice: str
    bob: str
    dude: str
    red_key: str
    blue_key: str
    green_key: str

def go(room, req):
    def func(state):
        if state.player == 'alice' and state.alice == 'red room':
            return []
        if state.player == 'bob' and state.bob == 'blue room':
            return []
        if state.player == 'dude' and state.dude == 'green room':
            return []

        states = []
        new_state = list(state)
        player_ind = ['alice', 'bob', 'dude'].index(state.player) + 1
        req_ind = ['red_key', 'blue_key', 'green_key'].index(req) + 4
        if new_state[player_ind] == new_state[req_ind]:
            new_state[player_ind] = room
            new_state[req_ind] = room
            states.append(State(*new_state))
            for i in range(1, 3):
                if new_state[((req_ind + i) % 3) + 4] == state[player_ind]:
                    new_state[((req_ind + i) % 3) + 4] = room
                    states.append(State(*new_state))

        return states

    return func


def switch_player():
    def func(state):
        new_state = list(state)
        players = ['alice', 'bob', 'dude']
        ind = (players.index(state.player) + 1) % 3
        new_state[0] = players[ind]
        return [State(*new_state)]

    return func


game = {
    'east room': dict(
        up=go('blue room', 'blue_key'),
        left=go('west room', 'green_key'),
        switch=switch_player()
    ),
    'west room': dict(
        up=go('red room', 'red_key'),
        right=go('east room', 'green_key'),
        switch=switch_player()
    ),
    'red room': dict(
        down=go('west room', 'red_key'),
        switch=switch_player()
    ),
    'blue room': dict(
        down=go('east room', 'blue_key'),
        switch=switch_player()
    ),

    'green room': dict(
        down=go('east room', 'green_key'),
        switch=switch_player()
    )

}

START_STATE = State(
    player='alice',
    alice='west room',
    bob='east room',
    dude='west room',
    red_key='east room',
    blue_key='west room',
    green_key='east room'
)


def is_goal_state(state):
    return state.alice == 'red room' and state.bob == 'blue room' #or state.dude == 'green room'


def find_dead_ends(states):
    reverse_states = dict.fromkeys(states)
    dead_ends = []

    for node in states:
        for connected_node in states[node]:
            if reverse_states[connected_node] is not None:
                reverse_states[connected_node].append(node)
            else:
                reverse_states[connected_node] = [node]

    winnable = set()
    nodes_to_check = queue.Queue()
    for state in states:
        if state.alice == 'red room' and state.bob == 'blue room': #or state.dude == 'green room':
            nodes_to_check.put(state)
            winnable.add(state)

    while not nodes_to_check.empty():
        step = nodes_to_check.get()
        for connected_room in reverse_states[step]:
            if connected_room in winnable:
                continue
            winnable.add(connected_room)
            nodes_to_check.put(connected_room)

    for state in states:
        if state not in winnable:
            dead_ends.append(state)

    return dead_ends


def make_model(game, start_state):
    states = dict()

    def iterate(current_state):
        nonlocal states
        if current_state in states:
            return

        states[current_state] = set()
        active_player_ind = ['alice', 'bob', 'dude'].index(current_state.player) + 1
        options = game[current_state.alice if current_state.player == 'alice' else current_state.bob].copy()
        for option in options:
            next_states = options[option](current_state)
            for next_state in next_states:
                states[current_state].add(next_state)
                iterate(next_state)

    iterate(start_state)
    dead_ends = find_dead_ends(states)

    dot = Digraph("Possible states")
    graph_keys = list(states.keys())
    for state in states:
        n = graph_keys.index(state)
        if state == start_state:
            dot.node(f'n{n}', style="filled", fillcolor="dodgerblue", shape="circle")
        elif is_goal_state(state):
            dot.node(f'n{n}', style="filled", fillcolor="green", shape="circle")
        elif state in dead_ends:
            dot.node(f'n{n}', style="filled", fillcolor="red", shape="circle")
        else:
            dot.node(f'n{n}', shape="circle")
    for state1 in states:
        n1 = graph_keys.index(state1)
        for state2 in states[state1]:
            n2 = graph_keys.index(state2)
            dot.edge(f'n{n1}', f'n{n2}')

    dot.node(f'alice: {start_state[1]}')
    dot.node(f'bob: {start_state[2]}')
    dot.node(f'dude: {start_state[3]}')
    dot.node(f'red key: {start_state[4]}')
    dot.node(f'blue key: {start_state[5]}')
    dot.node(f'green key: {start_state[6]}')

    dot.render(outfile='tttm.svg')

START_STATE = State(
    player='alice',
    alice='west room',
    bob='east room',
    dude='west room',
    red_key='east room',
    blue_key='west room',
    green_key='east room'
)



def is_goal_state(state):
    """
    Проверить, является ли состояние целевым.
    """
    return state.alice == 'red room' and state.bob == 'blue room' and state.dude == 'green room'