import os
import argparse


def generate_graphviz_tree(start_path):
    def _generate_tree(path, parent_id=None):
        nonlocal node_count
        node_count += 1
        current_id = node_count
        if os.path.isdir(path):
            print(f'\t{current_id} [label="{os.path.basename(path)}" shape=folder]')
            if parent_id is not None:
                print(f'\t{parent_id} -> {current_id}')
            for item in os.listdir(path):
                _generate_tree(os.path.join(path, item), current_id)
        else:
            print(f'\t{current_id} [label="{os.path.basename(path)}" shape=file]')
            if parent_id is not None:
                print(f'\t{parent_id} -> {current_id}')

    node_count = 0
    print('digraph {')
    _generate_tree(start_path)
    print('}')


def main():
    parser = argparse.ArgumentParser(description='Generate directory tree in Graphviz format.')
    parser.add_argument('path', type=str, help='path to the directory to generate tree from')
    args = parser.parse_args()

    if not os.path.exists(args.path):
        print(f'Error: Path "{args.path}" does not exist.')
        return

    generate_graphviz_tree(args.path)


if __name__ == '__main__':
    main()
