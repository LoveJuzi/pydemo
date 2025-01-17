#!/usr/bin/python3


#########################################################################################
def evaluate(component, env):
    return Interpreter.evaluate(component, env)


def apply(func, args):
    return Interpreter.apply(func, args)


#########################################################################################
class Undefeind:
    pass


undefeind = Undefeind()


#########################################################################################
class ObjFactory:
    def __init__(self):
        self._make_funcs = {}

    def install_make_func(self, k, v):
        self._make_funcs[k] = v

    def make(self, tag, *args):
        if tag not in self._make_funcs:
            return None
        return self._make_funcs[tag](*args)


#########################################################################################
class EnvironmentOp:
    @staticmethod
    def lookup_symbol_value(name, env):
        if env is None:
            # TODO: should add error message
            return undefeind
        val = env.get_value(name)
        if not val == undefeind:
            return val
        return EnvironmentOp.lookup_symbol_value(name, env.get_parent_env())

    @staticmethod
    def list_of_values(args, env):
        return [evaluate(arg, env) for arg in args]

    @staticmethod
    def define_variable(var, val, env):
        env.def_var_val(var, val)

    @staticmethod
    def extend_enviroment(variables, values, env):
        L1 = len(variables)
        L2 = len(values)
        if not L1 == L2:
            # TODO: add ERROR message
            return
        nameTable = {}
        for i in range(0, L1):
            nameTable[variables[i]] = values[i]
        return Environment(nameTable, env)


class Environment:
    def __init__(self, nameTable, parent):
        self._nameTable = nameTable
        self._parent = parent

    def get_value(self, name):
        if name not in self._nameTable:
            return undefeind

        return self._nameTable[name]

    def get_parent_env(self):
        return self._parent

    def def_var_val(self, var, val):
        self._nameTable[var] = val


#########################################################################################
class Interpreter:
    @staticmethod
    def convert(component):
        if not isinstance(component, (str, bytes, int, float, complex)):
            return component
        return ComponentFactory.make("Literal", component)

    evaluate_funcs = {}

    @staticmethod
    def install_evaluate_func(k, v):
        Interpreter.evaluate_funcs[k] = v

    @staticmethod
    def evaluate(component, env):
        component = Interpreter.convert(component)
        if Interpreter.get_component_type(component) not in Interpreter.evaluate_funcs:
            # ERROR
            return None
        return Interpreter.evaluate_funcs[Interpreter.get_component_type(component)](
            component, env
        )

    @staticmethod
    def get_component_type(component):
        return component.type()

    apply_funcs = {}

    @staticmethod
    def install_apply_func(k, v):
        Interpreter.apply_funcs[k] = v

    @staticmethod
    def apply(func, args):
        if Interpreter.get_func_type(func) not in Interpreter.apply_funcs:
            # ERROR
            return None
        return Interpreter.apply_funcs[Interpreter.get_func_type(func)](func, args)

    @staticmethod
    def get_func_type(func):
        return func.type()


#########################################################################################
ComponentFactory = ObjFactory()


#########################################################################################
class LiteralOp:
    @staticmethod
    def evaluate(component, env):
        return component.literal()


Interpreter.install_evaluate_func("Literal", LiteralOp.evaluate)


class Literal:
    def __init__(self, literal):
        self._literal = literal

    def literal(self):
        return self._literal

    def type(self):
        return "Literal"


ComponentFactory.install_make_func("Literal", lambda literal: Literal(literal))


#########################################################################################
class NameOp:
    @staticmethod
    def evaluate(component, env):
        return EnvironmentOp.lookup_symbol_value(component.name(), env)


Interpreter.install_evaluate_func("Name", NameOp.evaluate)


class Name:
    def __init__(self, name):
        self._name = name

    def name(self):
        return self._name

    def type(self):
        return "Name"


ComponentFactory.install_make_func("Name", lambda name: Name(name))


#########################################################################################
class DefinitionOp:
    @staticmethod
    def evaluate(component, env):
        EnvironmentOp.define_variable(
            component.variable(), evaluate(component.value(), env), env
        )
        return "ok"


Interpreter.install_evaluate_func("Definition", DefinitionOp.evaluate)


class Definition:
    def __init__(self, variable, value):
        self._variable = variable
        self._value = value

    def variable(self):
        return self._variable

    def value(self):
        return self._value

    def type(self):
        return "Definition"


ComponentFactory.install_make_func(
    "Definition", lambda name, value: Definition(name, value)
)


#########################################################################################
class IfOp:
    @staticmethod
    def evaluate(component, env):
        if IfOp.is_true(evaluate(component.predicate(), env)):
            return evaluate(component.consequent(), env)
        return evaluate(component.alternative(), env)

    @staticmethod
    def is_true(val):
        return val is True


Interpreter.install_evaluate_func("If", IfOp.evaluate)


class If:
    def __init__(self, predicate, consequent, alternative):
        self._predicate = predicate
        self._consequent = consequent
        self._alternative = alternative

    def predicate(self):
        return self._predicate

    def consequent(self):
        return self._consequent

    def alternative(self):
        return self._alternative

    def type(self):
        return "If"


ComponentFactory.install_make_func(
    "If",
    lambda predicate, consequent, alternative: If(predicate, consequent, alternative),
)


#########################################################################################
class SequenceOp:
    @staticmethod
    def evaluate(component, env):
        rt = None
        for action in component.actions():
            rt = evaluate(action, env)
        return rt


Interpreter.install_evaluate_func("Sequence", SequenceOp.evaluate)


class Sequence:
    def __init__(self, actions):
        self._actions = actions

    def actions(self):
        return self._actions

    def type(self):
        return "Sequence"


ComponentFactory.install_make_func("Sequence", lambda actions: Sequence(actions))


#########################################################################################
class LambdaOp:
    @staticmethod
    def evaluate(component, env):
        print(component.parameters())
        print(component.body())
        return FunctionFactory.make(
            "CoupoundFunc", component.body(), component.parameters(), env
        )


Interpreter.install_evaluate_func("Lambda", LambdaOp.evaluate)


class Lambda:
    def __init__(self, parameters, body):
        self._parameters = parameters
        self._body = body

    def parameters(self):
        return self._parameters

    def body(self):
        return self._body

    def type(self):
        return "Lambda"


ComponentFactory.install_make_func(
    "Lambda", lambda parameters, body: Lambda(parameters, body)
)


#########################################################################################
class ApplicationOp:
    @staticmethod
    def convert(func_name):
        if not isinstance(func_name, str):
            return func_name
        return ComponentFactory.make("Name", func_name)

    @staticmethod
    def evaluate(component, env):
        func = component.func_expression()
        func = ApplicationOp.convert(func)
        return apply(
            evaluate(func, env),
            EnvironmentOp.list_of_values(component.arg_expressions(), env),
        )


Interpreter.install_evaluate_func("Application", ApplicationOp.evaluate)


class Application:
    def __init__(self, func_expression, arg_expressions):
        self._func_expression = func_expression
        self._arg_expressions = arg_expressions

    def func_expression(self):
        return self._func_expression

    def arg_expressions(self):
        return self._arg_expressions

    def type(self):
        return "Application"


ComponentFactory.install_make_func(
    "Application", lambda func, args: Application(func, args)
)


#########################################################################################
FunctionFactory = ObjFactory()


#########################################################################################
class PrimitiveFuncOp:
    @staticmethod
    def apply(func, args):
        return func.apply(*args)


Interpreter.install_apply_func("PrimitiveFunc", PrimitiveFuncOp.apply)


class PrimitiveFunc:
    def __init__(self, func):
        self._func = func

    def apply(self, *args):
        return self._func(*args)

    def type(self):
        return "PrimitiveFunc"


FunctionFactory.install_make_func("PrimitiveFunc", lambda func: PrimitiveFunc(func))


#########################################################################################
class CoupoundFuncOp:
    @staticmethod
    def apply(func, args):
        return evaluate(
            ComponentFactory.make("Sequence", func.body()),
            EnvironmentOp.extend_enviroment(func.parameters(), args, func.env()),
        )


Interpreter.install_apply_func("CoupoundFunc", CoupoundFuncOp.apply)


class CoupoundFunc:
    def __init__(self, body, parameters, env):
        self._body = body
        self._parameters = parameters
        self._env = env

    def body(self):
        return self._body

    def parameters(self):
        return self._parameters

    def env(self):
        return self._env

    def type(self):
        return "CoupoundFunc"


FunctionFactory.install_make_func(
    "CoupoundFunc", lambda body, parameters, env: CoupoundFunc(body, parameters, env)
)


#########################################################################################
def build_top_env():
    def add(*args):
        L = len(args)
        if L < 2:
            return None
        rt = args[0]
        for i in range(1, L):
            rt = rt + args[i]
        return rt

    def equal(v1, v2):
        return v1 == v2

    nameTable = {}

    nameTable["+"] = FunctionFactory.make("PrimitiveFunc", add)
    nameTable["=="] = FunctionFactory.make("PrimitiveFunc", equal)

    return Environment(nameTable, None)


#########################################################################################
def test_literal_create():
    component = ComponentFactory.make("Literal", "Hello")
    assert component.literal() == "Hello"
    component = ComponentFactory.make("Literal", 2)
    assert component.literal() == 2
    component = ComponentFactory.make("Literal", 5.12)
    assert component.literal() == 5.12
    component = ComponentFactory.make("Literal", None)
    assert component.literal() is None


def test_literal_eval():
    component = ComponentFactory.make("Literal", "Hello")
    assert evaluate(component, None) == "Hello"


def test_name_create():
    component = ComponentFactory.make("Name", "v1")
    assert component.name() == "v1"
    env1 = Environment({"v1": 1, "v2": 2}, None)
    env2 = Environment({"v1": 0}, env1)
    assert evaluate(component, env2) == 0
    component2 = ComponentFactory.make("Name", "v2")
    assert evaluate(component2, env2) == 2


def test_top_env_add():
    top_env = build_top_env()
    add_func = EnvironmentOp.lookup_symbol_value("+", top_env)
    assert add_func.apply(1, 2, 3) == 6
    assert add_func.apply("A", "B", "C") == "ABC"


def test_apply_primitive_func():
    top_env = build_top_env()
    add_func = EnvironmentOp.lookup_symbol_value("+", top_env)
    PrimitiveFuncOp.apply(add_func, [1, 2, 3]) == 6


def test_application_v1():
    top_env = build_top_env()
    component = ComponentFactory.make("Application", "+", [5, 2])
    assert evaluate(component, top_env) == 7
    top_env = build_top_env()
    component = ComponentFactory.make("Application", "+", ["A", "B", "C"])
    assert evaluate(component, top_env) == "ABC"


def test_definition():
    top_env = build_top_env()
    component = ComponentFactory.make("Definition", "smh", "shengmh")
    assert evaluate(component, top_env) == "ok"
    name = ComponentFactory.make("Name", "smh")
    assert evaluate(name, top_env) == "shengmh"


def test_equal():
    top_env = build_top_env()
    component = ComponentFactory.make("Application", "==", [1, 1])
    assert evaluate(component, top_env)


def test_if():
    top_env = build_top_env()
    predicate = ComponentFactory.make("Application", "==", [1, 2])
    consequent = ComponentFactory.make("Literal", True)
    alternative = ComponentFactory.make("Literal", False)
    component = ComponentFactory.make("If", predicate, consequent, alternative)
    assert not evaluate(component, top_env)


def test_sequence():
    top_env = build_top_env()
    component = ComponentFactory.make(
        "Sequence",
        [
            1,
            2,
            3,
            ComponentFactory.make("Application", "+", [1, 2, 3]),
        ],
    )
    assert evaluate(component, top_env) == 6


def test_definition_v2():
    top_env = build_top_env()
    addition = ComponentFactory.make("Name", "+")
    evaluate(ComponentFactory.make("Definition", "add", addition), top_env)
    assert (
        evaluate(ComponentFactory.make("Application", "add", [1, 2, 3]), top_env) == 6
    )


def test_compound_func():
    top_env = build_top_env()
    func = FunctionFactory.make(
        "CoupoundFunc",
        [
            ComponentFactory.make(
                "Application",
                "+",
                [
                    ComponentFactory.make("Name", "a"),
                    ComponentFactory.make("Name", "b"),
                ],
            )
        ],
        ["a", "b"],
        top_env,
    )
    assert apply(func, [1, 2]) == 3


def test_lambda():
    top_env = build_top_env()
    lambda_add = ComponentFactory.make(
        "Lambda",
        ["a", "b"],
        [
            ComponentFactory.make(
                "Application",
                "+",
                [
                    ComponentFactory.make("Name", "a"),
                    ComponentFactory.make("Name", "b"),
                ],
            )
        ],
    )
    func = evaluate(lambda_add, top_env)
    assert apply(func, [1, 2]) == 3


def test_lambda_add():
    top_env = build_top_env()
    lambda_add = ComponentFactory.make(
        "Lambda",
        ["a", "b"],
        [
            ComponentFactory.make(
                "Application",
                "+",
                [
                    ComponentFactory.make("Name", "a"),
                    ComponentFactory.make("Name", "b"),
                ],
            )
        ],
    )
    def_add = ComponentFactory.make("Definition", "add", lambda_add)
    evaluate(def_add, top_env)
    call_add = ComponentFactory.make("Application", "add", [1, 2])
    assert evaluate(call_add, top_env) == 3
