import regex as re
from graphviz import Digraph
import random


def generate_random_regex():
    chars = "0123456789abcdefABCDEF#"
    operators = ['|', '*', '(', ')']
    length = random.randint(10, 20)
    regex = ''

    regex += random.choice(chars)

    for _ in range(length - 1):
        if random.random() < 0.3:

            regex += random.choice(chars)
        else:

            regex += random.choice(operators)

        if regex[0] in operators and regex[0] != '(':
            regex = random.choice(chars) + regex[1:]

    open_parens = regex.count('(')
    close_parens = regex.count(')')
    regex += ')' * (open_parens - close_parens) if open_parens > close_parens else ''

    return regex


def regex_to_fsm(regex):
    stack = []
    fsm_states = 0
    transitions = []

    def add_transition(source, symbol, target):
        transitions.append((source, symbol, target))

    for char in regex:
        if char == '(':
            stack.append(fsm_states)
            fsm_states += 1
        elif char == ')':
            accept = fsm_states
            fsm_states += 1
            start = stack.pop()
            add_transition(start, 'ε', accept)
            stack.append(start)
            stack.append(accept)
        elif char == '|':
            or_state = fsm_states
            fsm_states += 1
            left = stack.pop()
            right = stack.pop()
            add_transition(or_state, 'ε', left)
            add_transition(or_state, 'ε', right)
            stack.append(or_state)
        elif char == '*':
            accept = fsm_states
            fsm_states += 1
            start = stack.pop()
            add_transition(start, 'ε', accept)
            add_transition(accept, 'ε', start)
            stack.append(start)
            stack.append(accept)
        else:
            accept = fsm_states
            fsm_states += 1
            add_transition(fsm_states - 1, char, accept)
            stack.append(fsm_states - 1)
            stack.append(accept)
    return transitions


def visualize_fsm(transitions):
    dot = Digraph()
    dot.attr(rankdir='LR')

    for transition in transitions:
        source, symbol, target = transition
        dot.node(str(source), shape='circle')
        dot.node(str(target), shape='circle')
        label = f"{symbol} [{source}-{target}]"
        dot.edge(str(source), str(target), label=label)

    dot.render('fsm', format='png', cleanup=True)


random_regex = generate_random_regex()
print("Generated Regex:", random_regex)

fsm_transitions = regex_to_fsm(random_regex)

visualize_fsm(fsm_transitions)
