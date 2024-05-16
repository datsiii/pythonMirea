from networkx.classes import digraph

digraph finite_state_machine {
    rankdir=LR;
    node [shape = circle]; S;
    node [shape = doublecircle]; F;

    S -> q0 [label="0-9,A-Z"];
    q0 -> q1 [label="0-9,A-Z"];
    q1 -> q2 [label="0-9,A-Z"];
    q2 -> q3 [label="0-9,A-Z"];
    q3 -> F [label="0-9,A-Z"];
}
