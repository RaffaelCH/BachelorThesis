class Outer:

    class Inner:
        def inner(self):
            print("inner")
    
    def outer(self):
        print("outer")


outer = Outer()
outer.outer()

inner = Outer.Inner()
inner.inner()