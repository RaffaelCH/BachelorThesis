class SimpleClass:

    def __init__(self):
        pass

    def test(self):
        print("simple test")


simple = SimpleClass()
simple.test()



def foo(var):
    print(var)

def bar():
    return "bar"


foo("test")
foo(bar())