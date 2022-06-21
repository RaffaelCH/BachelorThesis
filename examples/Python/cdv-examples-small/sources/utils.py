def greet(name):
    """Greet the person."""

    def get_greeting():
        # TODO: Get greeting from somewhere else.
        return "Hello"
    
    try:
        greeting_to_use = get_greeting()
    except:
        print("Couldn't get greeting :(")
    greet_in_console(greeting_to_use, name)


def greet_in_console(greeting, name):
    print(f"{greeting}, {name}")