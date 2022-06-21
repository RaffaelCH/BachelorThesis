from classes import Main, Sidekick
from utils import greet


main = Main("Hero")
sidekick = Sidekick(main)

main.doStuff()
sidekick.help()


greet("John")