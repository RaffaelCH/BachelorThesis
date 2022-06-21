class TestClass:

    def __init__(self):
        pass

    def test(self):
        pass

    def test_caller(self):
        self.test()


def foo():   
    def bar():
        pass

def foo_caller():
    foo()


tc = TestClass()
tc.test_caller()

foo_caller()