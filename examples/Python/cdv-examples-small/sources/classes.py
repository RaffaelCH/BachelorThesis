class Main:

    def __init__(self, name):
         self.name = name
    
    def doStuff(self):
        print(self.name + " is doing stuff.")


class Sidekick:

    def __init__(self, main):
        self.main = main

    def help(self):
        print("Sidekick is helping " + self.main.name)