#!/usr/bin/python3


#########################################################################################
def evaluate(component, env):
    return JavaScriptInterpreter.evaluate(component, env)


def apply(func, args):
    pass


#########################################################################################
class JavaScriptInterpreter:
    @staticmethod
    def evaluate(component, env):
        return ComponentOp(component, env)


#########################################################################################
class ComponentOp:
    evaluate_funcs = {}

    @staticmethod
    def install_evaluate_funcs(k, v):
        ComponentOp.evaluate_funcs[k] = v

    @staticmethod
    def evaluate(component, env):
        if ComponentOp.get_type() not in ComponentOp.evaluate_funcs:
            # ERROR
            return None
        return ComponentOp.evaluate_funcs[ComponentOp.get_type(component)](
            component, env
        )

    @staticmethod
    def get_type(component):
        return component.type()


class LiteralOp:
    @staticmethod
    def evaluate(literal, env):
        pass


ComponentOp.install_evaluate_funcs("Literal", LiteralOp.evaluate)


class Literal:
    def __init__(self, literal):
        self._literal = literal
