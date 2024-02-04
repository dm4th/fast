import graphviz as gv

def DrawGraphFromString(directed_string: str, format: str = 'png', size: str = '8,5') -> gv.Digraph:
    graph = gv.Digraph(
        format=format,
        engine='dot',
        strict=True,
        graph_attr={
            'rankdir': 'LR',
            'size': size,
            }
    )

    edges = []
    lines = directed_string.split('\n')
    for line in lines:
        line = line.strip()

        if len(line) == 0:
            continue

        nodes = line.split('->')
        for n in range(len(nodes)-1):
            node1 = nodes[n].strip()
            node2 = nodes[n+1].strip()
            label = None
            if '[' in node2 and ']' in node2:
                node2, label = node2.split('[')
                label = label.split(']')[0]
                label = label.split('=')[1]
            edges.append((node1, node2, label))

    for edge in edges:
        if edge[2] is not None:
            graph.edge(edge[0], edge[1], label=edge[2])
        else:
            graph.edge(edge[0], edge[1])

    return graph