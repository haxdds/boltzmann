from .treemixin import TreeMixin

__all__ = ['RBTree']

class Node(object):
    """ Internal object, represents a treenode """
    __slots__ = ['key', 'value', 'red', 'left', 'right']
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.red = True
        self.left = None
        self.right = None

    def free(self):
        self.left = None
        self.right = None
        self.key = None
        self.value = None

    def __getitem__(self, key):
        """ x.__getitem__(key) <==> x[key], where key is 0 (left) or 1 (right) """
        return self.left if key == 0 else self.right

    def __setitem__(self, key, value):
        """ x.__setitem__(key, value) <==> x[key]=value, where key is 0 (left) or 1 (right) """
        if key == 0:
            self.left = value
        else:
            self.right = value

def is_red(node):
    if (node is not None) and node.red:
        return True
    else:
        return False

def jsw_single (root, direction):
    other_side = 1 - direction
    save = root[other_side]
    root[other_side] = save[direction]
    save[direction] = root
    root.red = True
    save.red = False
    return save

def jsw_double (root, direction):
    other_side = 1 - direction
    root[other_side] = jsw_single(root[other_side], other_side)
    return jsw_single(root, direction)

class RBTree(TreeMixin):
    """ 
    RBTree implements a balanced binary tree with a dict-like interface.
    see: http://en.wikipedia.org/wiki/Red_black_tree
    A red-black tree is a type of self-balancing binary search tree, a data
    structure used in computing science, typically used to implement associative
    arrays. The original structure was invented in 1972 by Rudolf Bayer, who
    called them "symmetric binary B-trees", but acquired its modern name in a
    paper in 1978 by Leonidas J. Guibas and Robert Sedgewick. It is complex,
    but has good worst-case running time for its operations and is efficient in
    practice: it can search, insert, and delete in O(log n) time, where n is
    total number of elements in the tree. Put very simply, a red-black tree is a
    binary search tree which inserts and removes intelligently, to ensure the
    tree is reasonably balanced.
    RBTree() -> new empty tree.
    RBTree(mapping) -> new tree initialized from a mapping
    RBTree(seq) -> new tree initialized from seq [(k1, v1), (k2, v2), ... (kn, vn)]
    see also TreeMixin() class.
    """
    def __init__(self, items=None):
        """ x.__init__(...) initializes x; see x.__class__.__doc__ for signature """
        self._root = None
        self._count = 0
        if items is not None:
            self.update(items)

    def clear(self):
        """ T.clear() -> None.  Remove all items from T. """
        def _clear(node):
            if node is not None:
                _clear(node.left)
                _clear(node.right)
                node.free()
        _clear(self._root)
        self._count = 0
        self._root = None

    @property
    def count(self):
        """ count of items """
        return self._count

    @property
    def root(self):
        """ root node of T """
        return self._root

    def _new_node(self, key, value):
        """ Create a new treenode """
        self._count += 1
        return Node(key, value)

    def insert(self, key, value):
        """ T.insert(key, value) <==> T[key] = value, insert key, value into Tree """
        if self._root is None: # Empty tree case
            self._root = self._new_node(key, value)
            self._root.red = False # make root black
            return

        head = Node() # False tree root
        grand_parent = None
        grand_grand_parent = head
        parent = None # parent
        direction = 0
        last = 0

        # Set up helpers
        grand_grand_parent.right = self._root
        node = grand_grand_parent.right
        # Search down the tree
        while True:
            if node is None: # Insert new node at the bottom
                node = self._new_node(key, value)
                parent[direction] = node
            elif is_red(node.left) and is_red(node.right):# Color flip
                node.red = True
                node.left.red = False
                node.right.red = False

            # Fix red violation
            if is_red(node) and is_red(parent):
                direction2 = 1 if grand_grand_parent.right is grand_parent else 0
                if node is parent[last]:
                    grand_grand_parent[direction2] = jsw_single(grand_parent, 1-last)
                else:
                    grand_grand_parent[direction2] = jsw_double(grand_parent, 1-last)

            # Stop if found
            if key == node.key:
                node.value = value #set new value for key
                break

            last = direction
            direction = 0 if key < node.key else 1
            # Update helpers
            if grand_parent is not None:
                grand_grand_parent = grand_parent
            grand_parent = parent
            parent = node
            node = node[direction]

        self._root = head.right # Update root
        self._root.red = False # make root black

    def remove(self, key):
        """ T.remove(key) <==> del T[key], remove item <key> from tree """
        if self._root is None:
            raise KeyError(str(key))
        head = Node() # False tree root
        node = head
        node.right = self._root
        parent = None
        grand_parent = None
        found = None # Found item
        direction = 1

        # Search and push a red down
        while node[direction] is not None:
            last = direction

            # Update helpers
            grand_parent = parent
            parent = node
            node = node[direction]

            direction = 1 if key > node.key else 0

            # Save found node
            if key == node.key:
                found = node

            # Push the red node down
            if not is_red(node) and not is_red(node[direction]):
                if is_red(node[1-direction]):
                    parent[last] = jsw_single(node, direction)
                    parent = parent[last]
                elif not is_red(node[1-direction]):
                    sibling = parent[1-last]
                    if sibling is not None:
                        if (not is_red(sibling[1-last])) and (not is_red(sibling[last])):
                            # Color flip
                            parent.red = False
                            sibling.red = True
                            node.red = True
                        else:
                            direction2 = 1 if grand_parent.right is parent else 0
                            if is_red(sibling[last]):
                                grand_parent[direction2] = jsw_double(parent, last)
                            elif is_red(sibling[1-last]):
                                grand_parent[direction2] = jsw_single(parent, last)
                            # Ensure correct coloring
                            grand_parent[direction2].red = True
                            node.red = True
                            grand_parent[direction2].left.red = False
                            grand_parent[direction2].right.red = False

        # Replace and remove if found
        if found is not None:
            found.key = node.key
            found.value = node.value
            parent[int(parent.right is node)] = node[int(node.left is None)]
            node.free()
            self._count -= 1

        # Update root and make it black
        self._root = head.right
        if self._root is not None:
            self._root.red = False
        if not found:
            raise KeyError(str(key))