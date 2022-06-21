class Hero:

    def __init__(self, name):
         self.name = name
    
    def doStuff(self):
        """Added some documentation."""
        output_string = f"{self.name} is doing stuff."
        print(output_string)


class Sidekick:

    def __init__(self, main):
        self.main = main

    def help(self):
        print("Sidekick is helping " + self.main.name)