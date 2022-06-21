class TestClass:

    def __init__(self):
        pass

    def test(self):
        pass

    class Inner:
        def inner(self):
            pass


def foo():   
    def bar():
        pass
    bar()

def foo_caller():
    foo()