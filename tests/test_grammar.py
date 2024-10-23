import grammar


def test_tree():
    t = grammar.Tree()
    root = t.add_node('root')
    assert t.nodes[root] == 'root'
    assert 'root' not in t.parents

    index = t.add_node('child1', root)
    assert t.nodes[index] == 'child1'
    assert t.parents[index] == root
    assert index in t.children[root]

    t.add_node('child2', root)
    index = t.get_next_child(index)
    assert t.nodes[index] == 'child2'
    assert t.get_next_child(index) is None


def test_grammar():
    g = grammar.Grammar()
    g.root = 'S'
    g.add_production('S', ('a', 'b'))
    assert g.terminals == {'a', 'b'}
    assert g.get_firsts() == {('a', 'b'): {'a'}}
    t = g.parse(('a', 'b'))
    assert t.nodes[t.root] == 'S'
    children = tuple(t.nodes[i] for i in t.children[t.root])
    assert children == ('a', 'b')


def test_number_grammar():
    g = grammar.NumberGrammar()
    t = g.parse('0')
    assert t.nodes[t.root] == 'number'
