from Constants import constants
from Graph import *
import random 

class Environment() :
    def __init__(self) :
        self.random_var_id = 65
        self.procedures_order = []
        self.procedures = {}
        self.constants = constants

    def assign_program(self, expression) :
        self.toplevel = Function("toplevel", [], expression)

    def run(self) :
        return self.toplevel.call(self, [])

    def compile(self) :
        return self.toplevel.compile(self, [])

    def __str__(self) :
        ret = ''
        for p in self.procedures_order :
            ret += self.procedures[p].__str__(0)
        ret += self.toplevel.__str__(0)
        return ret

    def get_new_var(self) :
        if self.random_var_id <= 90 :
            v = 'x_' + chr(self.random_var_id)
        else :
            v = 'x_' + str(self.random_var_id)
        self.random_var_id += 1
        return v
    
    def get_fresh_var_for_program(self) :
        hash = random.getrandbits(128)
        return 'foppl_x_' + str(hash)
        
        
class Context() :
    def __init__(self, env) :
        self.env = env
        self.variables = {}

class Expression() :
    def __init__(self) :
        pass

    def freevars(self) :
        pass

    def run(self, env) :
        pass

class Function() :
    def __init__(self, name, arguments, expression) :
        self.name = name
        self.arguments = arguments
        self.expression = expression

    def call(self, env, values) :
        assert len(values) == len(self.arguments)
        context = Context(env)
        context.variables = {k:v for k, v in zip(self.arguments, values)}
        return self.expression.run(context)

    def compile(self, env, values) :
        assert len(values) == len(self.arguments)
        context = Context(env)
        context.variables = {k:v for k, v in zip(self.arguments, values)}
        context.predicate = GraphNumber(True)
        return self.expression.compile(context)

    def __str__(self, level=0):
        ret = "\t"*level+"Function "+self.name+"(" + ','.join(self.arguments) + ")\n"
        ret += self.expression.__str__(level+1)
        return ret

class Number(Expression) :
    def __init__(self, num) :
        self.num = num
        super().__init__()

    def freevars(self) :
        return set([])

    def run(self, context) :
        return self.num

    def compile(self, context) :
        return Graph(), GraphNumber(self.num)

    def __str__(self, level=0):
        ret = "\t"*level+"Num "+str(self.num)+"\n"
        return ret

class Variable(Expression) :
    def __init__(self, name) :
        self.name = name
        super().__init__()

    def freevars(self) :
        return set([self.name])

    def run(self, context) :
        if self.name in context.variables :
            return context.variables[self.name]
        else :
            raise LookupError("Variable does not exists ..")

    def compile(self, context) :
        if self.name in context.variables :
            return Graph(), context.variables[self.name]
        else :
            raise LookupError("Variable does not exists ..")

    def __str__(self, level=0):
        ret = "\t"*level+"Var "+self.name+"\n"
        return ret

class LetExpression(Expression) :
    def __init__(self, name, argument, expression) :
        self.name = name
        self.argument = argument
        self.expression = expression
        super().__init__()

    def freevars(self) :
        return self.argument.freevars() | (set(self.expression.freevars()) - set([self.name]))

    def run(self, context) :
        if self.name in context.variables :
            raise LookupError("Already Exists ...")
        result = self.argument.run(context)
        if self.name != '_' : context.variables[self.name] = result
        result = self.expression.run(context)
        if self.name != '_' : del context.variables[self.name]

        return result

    def compile(self, context) :
        if self.name in context.variables :
            raise LookupError("Already Exists ...")
        G1, E1 = self.argument.compile(context)
        if self.name != '_' : context.variables[self.name] = E1
        G2, E2 = self.expression.compile(context)
        if self.name != '_' : del context.variables[self.name]

        return G1.disjoint_sum(G2), E2

    def __str__(self, level=0):
        ret = "\t"*level+"Let "+self.name + ' = ' +"\n"
        ret += self.argument.__str__(level+1)
        ret += "\t"*level+"In"+"\n"
        ret += self.expression.__str__(level+1)
        return ret

class IfExpression(Expression) :
    def __init__(self, condition, true_branch, false_branch) :
        self.condition = condition
        self.true_branch = true_branch
        self.false_branch = false_branch
        super().__init__()

    def freevars(self) :
        return self.condition.freevars() | self.true_branch.freevars() | self.false_branch.freevars()

    def run(self, context) :
        condition_result = self.condition.run(context)
        true_result = self.true_branch.run(context)
        false_result = self.false_branch.run(context)
        if condition_result :
            return true_result
        else :
            return false_result

    def compile(self, context) :
        G1, E1 = self.condition.compile(context)
        context.predicate = GraphConstantCall("and", [context.predicate, E1])
        G2, E2 = self.true_branch.compile(context)
        context.predicate = context.predicate.values[0]
        context.predicate = GraphConstantCall("and", [context.predicate, GraphConstantCall('not', [E1])])
        G3, E3 = self.false_branch.compile(context)
        context.predicate = context.predicate.values[0]
        return G1.disjoint_sum(G2.disjoint_sum(G3)), GraphIfExpression(E1, E2, E3)

    def __str__(self, level=0):
        ret = "\t"*level+"If"+"\n"
        ret += self.condition.__str__(level+1)
        ret += "\t"*level+"Then"+"\n"
        ret += self.true_branch.__str__(level+1)
        ret += "\t"*level+"Else"+"\n"
        ret += self.false_branch.__str__(level+1)
        return ret

class ConstantCall(Expression) :
    def __init__(self, name, params) :
        self.name = name
        self.params = params
        super().__init__()

    def freevars(self) :
        return set.union(*[x.freevars() for x in self.params])

    def run(self, context) :
        results = [x.run(context) for x in self.params]
        if self.name in context.env.constants :
            obj = context.env.constants[self.name]
            return obj(*results)
        else :
            raise LookupError("%s does not exist "%(self.name,))

    def compile(self, context) :
        results = [x.compile(context) for x in self.params]
        G = Graph()
        for r in results :
            G = G.disjoint_sum(r[0])

        return G, GraphConstantCall(self.name, [r[1] for r in results])

    def __str__(self, level=0):
        ret = "\t"*level+"Call "+ self.name +"\n"
        for p in self.params :
            ret += p.__str__(level+1)
        return ret

class FunctionCall(Expression) :
    def __init__(self, name, params) :
        self.name = name
        self.params = params
        super().__init__()

    def freevars(self) :
        return set.union(*[x.freevars() for x in self.params])

    def run(self, context) :
        results = [x.run(context) for x in self.params]
        if self.name in context.env.procedures :
            obj = context.env.procedures[self.name]
            return obj.call(context.env, results)
        else :
            raise LookupError("%s does not exist "%(self.name,))

    def compile(self, context) :
        results = [x.compile(context) for x in self.params]
        G = Graph()
        for r in results :
            G = G.disjoint_sum(r[0])

        if self.name in context.env.procedures :
            obj = context.env.procedures[self.name]
            G1, E = obj.compile(context.env, [r[1] for r in results])  
            return G.disjoint_sum(G1), E
        else :
            raise LookupError("%s does not exist "%(self.name,)) 

    def __str__(self, level=0):
        ret = "\t"*level+"Call "+ self.name +"\n"
        for p in self.params :
            ret += p.__str__(level+1)
        return ret

class Sample(Expression) :
    def __init__(self, expression) :
        self.expression = expression
        super().__init__()

    def freevars(self) :
        return self.expression.freevars()

    def run(self, context) :
        result = self.expression.run(context)
        if hasattr(result, 'distribution') :
            return result.sample()
        else :
            raise LookupError("Not A Distribution ...")

    def compile(self, context) :
        G1, E1 = self.expression.compile(context)
        v = GraphVariable(context.env.get_new_var())
        try :
            Z = E1.freevars()
        except :
            breakpoint()
        F = E1.score(v, context.env)

        G = Graph()
        G.V |= (G1.V | set([v]))
        G.A |= (G1.A | set([(z, v) for z in Z]))
        G.P.update(G1.P)
        G.P[v] = F
        G.Y.update(G1.Y)
        return G, v

    def __str__(self, level=0):
        ret = "\t"*level+"sample"+"\n"
        ret += self.expression.__str__(level+1)
        return ret

class Observe(Expression) :
    def __init__(self, expression_1, expression_2) :
        self.expression_1 = expression_1
        self.expression_2 = expression_2
        super().__init__()

    def freevars(self) :
        return self.expression_1.freevars() | self.expression_2.freevars()

    def run(self, context) :
        result = self.expression_2.run(context)
        return result

    def compile(self, context) :
        G1, E1 = self.expression_1.compile(context)
        G2, E2 = self.expression_2.compile(context)
        G1 = G1.disjoint_sum(G2)
        v = GraphVariable(context.env.get_new_var())
        F1 = E1.score(v, context.env)
        F = GraphIfExpression(context.predicate, F1, GraphNumber(1))
        Z = F1.freevars() - set([v])
        B = set([(z, v) for z in Z])

        G = Graph()
        G.V |= (G1.V | set([v]))
        G.A |= (G1.A | B)
        G.P.update(G1.P)
        G.P[v] = F
        G.Y.update(G1.Y)
        G.Y[v] = E2

        return G, E2

    def __str__(self, level=0):
        ret = "\t"*level+"observe"+"\n"
        ret += self.expression_1.__str__(level+1)
        ret += self.expression_2.__str__(level+1)
        return ret