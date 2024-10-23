from collections import defaultdict


class Tree:
    def __init__(self):
        self.nodes = []
        self.children = defaultdict(list)
        self.parents = {}
        self.root = None

    def add_node(self, value, parent: int = None) -> int:
        self.nodes.append(value)
        index = len(self.nodes) - 1
        if parent is not None:
            self.add_child(parent, index)
        else:
            self.root = index
        return index

    def add_child(self, parent: int, child: int):
        self.children[parent].append(child)
        self.parents[child] = parent

    def get_next_child(self, node: int):
        while node in self.parents:
            parent = self.parents[node]
            siblings = self.children[parent]
            index = siblings.index(node) + 1
            if index >= len(siblings):
                # This was the last child, move up
                node = parent
                continue
            return siblings[index]
        # Top level node has no siblings
        return None

    def to_list(self) -> list:
        result = []
        q = [(result, self.root)]
        while q:
            output, index = q.pop(0)
            value = self.nodes[index]
            if index in self.children:
                children = []
                output.append({value: children})
                for n in self.children[index]:
                    q.append((children, n))
            else:
                output.append(value)
        return result


class Grammar:
    """"A generic context-free grammar."""
    def __init__(self):
        self.root = None
        self.terminals = set()
        self.productions = {}

    def add_production(self, head: str, body: tuple[str]):
        if head not in self.productions:
            self.productions[head] = []
            self.terminals.discard(head)
        self.productions[head].append(body)
        for symbol in body:
            if symbol not in self.productions:
                self.terminals.add(symbol)

    def get_first(self, body: tuple[str]) -> set[str]:
        if len(body) == 0:
            return {()}
        if body[0] in self.terminals:
            return {body[0]}

        productions = self.productions[body[0]]
        result = set()
        for production in productions:
            result |= self.get_first(production)
        return result

    def get_firsts(self) -> dict:
        """Get the set of possible first terminal symbols for each production.

        The result is a dict mapping a production (tuple of symbols) as the
        key, to the set of terminal symbols that can occur first in any
        derivation of that production.

        This method requires that the grammar is free from left-recursion.
        """
        result = defaultdict(set)
        for head, bodies in self.productions.items():
            for body in bodies:
                result[body] |= self.get_first(body)
        return dict(result)

    def parse(self, tokens: tuple[str]):
        tree = Tree()
        head = self.root
        node = tree.add_node(head)
        firsts = self.get_firsts()
        i = 0
        while True:
            while head is None and node is not None:
                # Skip past empty nodes
                node = tree.get_next_child(node)
                if node is not None:
                    head = tree.nodes[node]

            if node is None:
                if i < len(tokens):
                    raise ValueError(
                            "Ran out of tree nodes while there are still "
                            "tokens remaining to be parsed.")
                # Completed parsing successfully.
                return tree
            if i < len(tokens):
                symbol = tokens[i]
            else:
                symbol = None
            if symbol in self.terminals and symbol == head:
                # Terminal symbol matches, advance the current token and move
                # to the next leftmost child node.
                i += 1
                node = tree.get_next_child(node)
                if node is not None:
                    head = tree.nodes[node]
                continue

            productions = self.productions[head]
            candidates = {x for x in productions if symbol in firsts[x]}
            production = None
            if len(candidates) > 1:
                raise ValueError(
                        f"Multiple productions are valid for `{head}` with "
                        f"first token `{symbol}`: {candidates}")
            if len(candidates) == 1:
                production = next(iter(candidates))
            if len(candidates) == 0:
                if () in productions:
                    # No productions match the symbol, but an empty match is
                    # possible, so select it by adding a single node with value
                    # None to the tree and moving on.
                    node = tree.add_node(None, node)
                    head = None
                    continue
            if production is None:
                raise ValueError(
                        f"No valid productions for `{head}` with first "
                        f"token `{symbol}`.")
            # A particular non-empty production has been selected, populate
            # this node's children with the production and descend to the first
            # child.
            parent = node
            head = production[0]
            node = tree.add_node(head, parent)
            for item in production[1:]:
                tree.add_node(item, parent)


class NumberGrammar(Grammar):
    """An abstract base class grammar for simple integer arithmetic.

    A new NumberGrammar object will be initialised with rules to produce a
    'number' (a non-negative integer) from a sequence of digits. The rules for
    arithmetic operations (operators and parentheses) will need to be added by
    the caller or by a subclass.
    """
    def __init__(self):
        super().__init__()

        self.root = 'number'
        self.add_production('number', ('digit', 'number1'))
        self.add_production('number1', ('digit', 'number1'))
        self.add_production('number1', ())
        for digit in range(10):
            self.add_production('digit', tuple(str(digit)))
