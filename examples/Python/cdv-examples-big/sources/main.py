from classes import Sidekick
from protagonist import Protagonist


main = Protagonist("Hiro Protagonist")
sidekick = Sidekick(main)

main.doStuff()
sidekick.help()

main.get_shot()



# Doing some unrelated stuff.

string_to_split = "Hello, world!"
split_string = [char for char in string_to_split.split()]
split_string.sort()

for char in split_string():
    print(char)