from binarytree import Node as VisualRankNode


class RankNode:
    def __init__(self, value):
        self.value = value
        self.left: RankNode | None = None
        self.right: RankNode | None = None
        self.rank = 1
        self.height = 0


class PositionalBalancedBinaryTree:
    def __init__(self) -> None:
        self.root: RankNode | None = None

    def find(self, pos):
        if not self.root:
            print("Tree is empty")
            return

        curr_node = self.root
        while curr_node is not None:
            if pos > curr_node.rank:
                pos -= curr_node.rank
                curr_node = curr_node.right

            elif pos < curr_node.rank:
                curr_node = curr_node.left

            else:
                return curr_node

        return None

    def insert(self, pos, val):
        def insert_recursively(node, pos, val):
            if node is None:
                return RankNode(value=val)

            elif pos > node.rank:
                pos -= node.rank
                node.right = insert_recursively(node=node.right, pos=pos, val=val)

            elif pos <= node.rank:
                node.rank += 1
                node.left = insert_recursively(node=node.left, pos=pos, val=val)

            node = self._rebalance_node(node)
            return node

        self.root = insert_recursively(self.root, pos, val)

    def show(self):
        if not self.root:
            print("Tree is empty")
            return
        v_root = self._visualize_tree(self.root)
        print(v_root)

    def _rebalance_node(self, node):
        node.height = (
            max(self._get_node_height(node.left), self._get_node_height(node.right)) + 1
        )
        balance = self._get_node_height(node.left) - self._get_node_height(node.right)

        # Left-side is heavier - do right-rotation
        if balance > 1:
            # Check left subnode for zig-zag
            if self._get_node_height(node.left.right) > self._get_node_height(
                node.left.left
            ):
                node.left = self._do_left_rotation(node.left)
            return self._do_right_rotation(node)

        # Right-side is heavier - do left-rotation
        if balance < -1:
            # Check right subnode for zig-zag
            if self._get_node_height(node.right.left) > self._get_node_height(
                node.right.right
            ):
                node.right = self._do_right_rotation(node.right)
            return self._do_left_rotation(node)

        return node

    def _get_node_height(self, node):
        return node.height if node else -1

    def _do_right_rotation(self, origin_node):
        # Pull-up son node
        pull_node = origin_node.left
        origin_node.left = pull_node.right
        pull_node.right = origin_node

        # Origin node will decrease its rank, bcs it doesn't have pull_node on its left now
        origin_node.rank -= pull_node.rank

        # Update heights
        origin_node.height = 1 + max(
            self._get_node_height(origin_node.left),
            self._get_node_height(origin_node.right),
        )

        pull_node.height = 1 + max(
            self._get_node_height(pull_node.left),
            self._get_node_height(pull_node.right),
        )

        # Replace origin node with pull
        return pull_node

    def _do_left_rotation(self, origin_node):
        # Pull-up son node
        pull_node = origin_node.right
        origin_node.right = pull_node.left
        pull_node.left = origin_node

        # Origin node will increase its rank, bcs it now have new nodes on the left
        pull_node.rank += origin_node.rank

        # Update heights
        origin_node.height = 1 + max(
            self._get_node_height(origin_node.left),
            self._get_node_height(origin_node.right),
        )

        pull_node.height = 1 + max(
            self._get_node_height(pull_node.left),
            self._get_node_height(pull_node.right),
        )

        # Replace origin node with pull
        return pull_node

    def _visualize_tree(self, node: RankNode):
        if node is None:
            return None

        v_node = VisualRankNode(f"{node.value}-r{node.rank}-h{node.height}")
        v_node.left = self._visualize_tree(node.left)
        v_node.right = self._visualize_tree(node.right)

        return v_node


tree = PositionalBalancedBinaryTree()
tree.insert(1, 42)
tree.insert(2, 312)
tree.insert(3, 122)
tree.insert(2, 234)
tree.insert(5, 235)
tree.insert(6, 236)
tree.insert(1, 10)
tree.show()
