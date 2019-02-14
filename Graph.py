import networkx as nx
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
import matplotlib.pyplot as plt

class Graph() :
    def __init__(self) :
        self.V = set()
        self.A = set()
        self.P = {}
        self.Y = {}

    def disjoint_sum(self, G2) :
        g = Graph()
        g.V = self.V | G2.V
        g.A = self.A | G2.A
        g.P = {}
        g.P.update(self.P)
        g.P.update(G2.P)
        g.Y = {}
        g.Y.update(self.Y)
        g.Y.update(G2.Y)

        return g

    def draw(self) :
        ng = nx.DiGraph()
        for v in self.V :
            ng.add_node(str(v))

        for e in self.A :
            ng.add_edge(str(e[0]), str(e[1]))
            
        H = nx.relabel_nodes(ng, {str(v):str(self.P[v]).replace('(', '\n(') for v in self.V})
        plt.figure(figsize=(20,5))
        plt.gca().margins(0.2, 0.2)  
        pos = graphviz_layout(H, prog='dot')
        non_observe_nodes = [str(self.P[v]).replace('(', '\n(') for v in self.V if v not in self.Y]
        observe_nodes = [str(self.P[v]).replace('(', '\n(') for v in self.V if v in self.Y]
        nx.draw_networkx(H, pos=pos, nodelist=non_observe_nodes, alpha=0.3, node_color='#66c2a5', node_size=7000)
        nx.draw_networkx_labels(H, pos=pos, nodelist=non_observe_nodes)
        nx.draw_networkx(H, pos=pos, nodelist=observe_nodes, alpha=0.3, node_color='#fc8d62', node_size=7000)
        nx.draw_networkx_labels(H, pos=pos, nodelist=observe_nodes)
        plt.tight_layout()

class GraphExpression() :
    def __init__(self) :
        pass

class GraphVariable() :
    def __init__(self, var) :
        self.name = var

    def freevars(self) :
        return set([self])

    def __str__(self) :
        return self.name[:7]

class GraphNumber() :
    def __init__(self, num) :
        self.num = num

    def score(self, v, env) :
        return self

    def run(self, v) :
        return self.num

    def freevars(self) :
        return set([])

    def __str__(self) :
        return str(self.num)

class GraphIfExpression() :
    def __init__(self, condition, true_branch, false_branch) :
        self.condition = condition
        self.true_branch = true_branch
        self.false_branch = false_branch
        super().__init__()

    def score(self, v, env) :
        return GraphIfExpression(self.condition, self.true_branch.score(v), self.false_branch.score(v))

    def freevars(self) :
        return self.condition.freevars() | self.true_branch.freevars() | self.false_branch.freevars()

    def __str__(self) :
        return '(if ' + str(self.condition) + ' ' + str(self.true_branch) + ' ' + str(self.false_branch) + ')'

class GraphConstantCall() :
    def __init__(self, name, values) :
        self.name = name
        self.values = values

    def score(self, v, env) :
        if self.name in env.constants and hasattr(env.constants[self.name], "distribution") :
            return GraphConstantCall('p_' + self.name, [v] + self.values)  
        else :
            raise LookupError() 

    def freevars(self) :
        return set.union(*[x.freevars() for x in self.values])   

    def __str__(self) :
        return '(' + self.name + ' ' + ' '.join([str(v) for v in self.values]) + ')'   