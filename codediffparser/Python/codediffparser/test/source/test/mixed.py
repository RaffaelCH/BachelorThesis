import nested_class
from simple_function import foo as foo_alias


class Sub(nested_class.Outer.Inner):

    def __init__(self):
        super().inner()
    
    def foo_caller(self):
        foo_alias("foo_caller")
    
    def static():
        print("static")


Sub().foo_caller()
Sub.static()