from graphviz import Digraph


def generate_graph():
    graph = Digraph('finite_state_machine', filename='fsm.gv')
    graph.attr(rankdir='LR', size='8,5')

    # Define nodes
    graph.node('S', shape='circle')
    graph.node('F', shape='doublecircle')
    graph.node('', shape='none', label='')

    # Define transitions
    graph.edge('', 'S')
    graph.edge('S', 'F', label='[0-9]')

    return graph


# Generate and render the graph
generate_graph().render(format='png', cleanup=True)
