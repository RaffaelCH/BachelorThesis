class SuperInheritance:

    def super_inheritance(self):
        print("super inheritance")


class InheritanceClass(SuperInheritance):

    def inherit(self):
        print("inherit")


inheritance = InheritanceClass()
inheritance.inherit()
inheritance.super_inheritance()