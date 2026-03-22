import time
import random

from balanced_tree_insertion_by_pos import PositionalBalancedBinaryTree


def run_experiment(n):
    # Python list test
    py_list = []
    start_time = time.time()
    for i in range(n):
        pos = random.randint(0, len(py_list)) if py_list else 0
        py_list.insert(pos, i)
    list_time = time.time() - start_time
    print(f"Python List: {n} insertions, {list_time:.4f} sec")

    # Tree check
    tree = PositionalBalancedBinaryTree()
    start_time = time.time()
    for i in range(n):
        pos = random.randint(1, i + 1) if i > 0 else 1
        tree.insert(pos, i)
    tree_time = time.time() - start_time
    print(f"Tree: {n} insertions, {tree_time:.4f} sec")

    print(f"\nResult: {list_time / tree_time:.1f} speed ratio")


run_experiment(200000)
