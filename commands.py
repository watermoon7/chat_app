import random


lengths = list(range(12))
distribution = [
    0.06, 0.07, 0.09, 0.11,
    0.13, 0.14, 0.10, 0.07,
    0.10, 0.06, 0.03, 0.04
    ]

def pp():
    choice = random.choices(lengths, distribution)[0]
    return f"8{choice*'='}D~"

def height():
    return f'{random.randint(2, 6)}\'{random.randint(1, 11)}\"'

fortunes = open('commands_data/fortunes.txt', 'r').read().splitlines()

def fortune():
    return random.choice(fortunes)

ball_8_responses = open('commands_data/8ball.txt', 'r').read().splitlines()

def ball_8(null=None):
    if null == None:
        return 'Add a question at the end you idiot. Try /8ball Am I an idiot?'
    return random.choice(ball_8_responses)

def dice():
    return random.randint(1, 6)

def math(expression):
    try:
        return eval(expression)
    except:
        return 'Invalid syntax for mathematical expression'
    
cat_breeds = open('commands_data/cats.txt', 'r').read().splitlines()
def cat():
    return random.choice(cat_breeds)

dog_breeds = open('commands_data/dogs.txt', 'r').read().splitlines()
def dog():
    return random.choice(dog_breeds)

def list_commands():
    global commands
    return ', '.join([str(i) for i in commands]) 

commands = {
    '/cat': cat,
    '/commands': list_commands,
    '/dice': dice,
    '/dog': dog,
    '/fortune': fortune,
    '/height': height,
    '/pp': pp,
    '/8ball': ball_8
    }

def command(msg):
    msg = msg.split(None, 1)
    if len(msg) == 1:
        return commands[msg[0]]()
    else:
        try:
            return commands[msg[0]](msg[1])
        except:
            return 'Invalid command'

""" while True:
    inp = input('Command: ')
    print(command(inp)) """
