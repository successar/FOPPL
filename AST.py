from Constants import constants

class Environment() :
    def __init__(self) :
        self.procedures_order = []
        self.procedures = {}
        self.constants = constants

    def assign_program(self, expression) :
        self.toplevel = Function("toplevel", [], expression)

    def run(self) :
        return self.toplevel.call(self, [])

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

class Number(Expression) :
    def __init__(self, num) :
        self.num = num
        super().__init__()

    def freevars(self) :
        return set([])

    def run(self, context) :
        return self.num

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
        context.variables[self.name] = result
        result = self.expression.run(context)
        del context.variables[self.name]

        return result

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