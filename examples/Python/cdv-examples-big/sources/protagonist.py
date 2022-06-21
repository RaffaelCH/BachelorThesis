from classes import Hero

import random


class Protagonist(Hero):
    
    class PlotArmor:

        def save(self, plot_armor=True):
            """Calculating if hero gets saved."""
            if (plot_armor):
                print("Plot armor saves the day (again)!")
            else:
                dice_throw_outcome = random.randint(1, 20)
                if dice_throw_outcome > 18:
                    print("Save!")
                else:
                    print("The hero died :(")
    
    def __init__(self, name):
        super().__init__(name)
        self.protagonist_power = Protagonist.PlotArmor()

    def get_shot(self):
        self.protagonist_power.save()