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

fortunes = [
    "Your social media rants will be ignored by everyone except your grandmother.",
    "Your tweets will only be retweeted by your mom.",
    "Your political beliefs are more contradictory than a puzzle with the wrong pieces.",
    "You will serendipitously discover a panacea for a problem that has long vexed you.",
    "You will experience an ineffable sense of contentment and bliss.",
    "You will encounter a perspicacious mentor who will guide you towards success.",
    "You will have a revelatory epiphany that will change your perspective on life.",
    "You will be granted a propitious opportunity to advance your career.",
    "You will meet a gregarious individual who will introduce you to new social circles.",
    "You will have an erudite conversation with a renowned scholar.",
    "You will be struck by a prodigious inspiration that will lead to great achievements.",
    "You will experience a transcendent moment of clarity and understanding.",
    "You will encounter an enigmatic figure who will challenge your assumptions and beliefs.",
    "You will receive a prestigious award for your exceptional talents.",
    "You will have a superlative performance that will impress your colleagues and superiors.",
    "You will have an auspicious meeting that will lead to exciting opportunities.",
    "You will experience a profound sense of equanimity and inner peace.",
    "You will encounter a charismatic leader who will inspire you to greatness.",
    "You will undergo a transformative experience that will redefine your sense of purpose.",
    "You will have a magnanimous gesture of kindness reciprocated in unexpected ways.",
    "You will encounter an uncommon obstacle that will test your ingenuity and perseverance.",
    "You will have a felicitous encounter with an old friend.",
    "You will be emboldened by a fortuitous turn of events.",
    "You will be struck by a poignant realization that will bring you to tears.",
    "You will have a fleeting moment of lucidity that will reveal the truth about a difficult situation.",
    "You will be granted a rarefied opportunity to showcase your talents.",
    "You will experience a moment of sublime beauty that will take your breath away.",
    "You will have a bittersweet moment of nostalgia for a time long past.",
    "You will have an unanticipated encounter that will change your life forever.",
    "You will encounter an arcane mystery that will test your intellect and curiosity.",
    "You will experience a pensive moment of reflection that will lead to self-discovery.",
    "You will receive an unexpected gift that will bring you great joy.",
    "You will have a fortuitous stroke of luck that will change your fortune.",
    "You will encounter a daunting challenge that will require all of your courage and determination.",
    "You will have a profound realization about the interconnectedness of all things.",
    "You will accidentally swallow a harmonica every time you breathe",
    "You will step on a piece of Lego :(",
    "You will develop a phobia of your own reflection",
    "You will wake up with an extra eye in the middle of your forehead",
    "You will be followed around by a flock of seagulls wherever you go",
    "You will develop a sudden fear of doors and windows",
    "You will always feel like you are drowning",
    "You will be cursed to always smell like your arse",
    "You will accidentally turn your hands into feet and your feet into hands",
    "You will always feel like you are being suffocated by a pillow",
    "You will always feel like you are being followed by a pair of disembodied hands"
        ]
def fortune():
    return random.choice(fortunes)

responses = [
    "Absolutely",
    "Utterly",
    "Completely",
    "Totally",
    "Entirely",
    "Thoroughly",
    "Partially",
    "Incompletely",
    "Somewhat",
    "Moderately",
    "Halfway",
    "Partly",
    "By no means",
    "In no way",
    "Absolutely not",
    "Not in the slightest",
    "Not even a little bit",
    "Not even close"
    ]

def ball_8(null=None):
    if null == None:
        return 'Add a question at the end you idiot. Try /8ball Am I an idiot?'
    return random.choice(responses)

def dice():
    return random.randint(1, 6)

def math(expression):
    try:
        return eval(expression)
    except:
        return 'Invalid syntax for mathematical expression'
cat_breeds = [
    "Abyssinian",
    "American Bobtail",
    "American Curl",
    "American Shorthair",
    "Balinese",
    "Bengal",
    "Birman",
    "Bombay",
    "British Shorthair",
    "Burmese",
    "Chartreux",
    "Cornish Rex",
    "Devon Rex",
    "Egyptian Mau",
    "Exotic Shorthair",
    "Havana Brown",
    "Himalayan",
    "Japanese Bobtail",
    "Javanese",
    "Korat",
    "LaPerm",
    "Maine Coon",
    "Manx",
    "Munchkin",
    "Nebelung",
    "Norwegian Forest Cat",
    "Ocicat",
    "Oriental",
    "Persian",
    "Pixiebob",
    "Ragamuffin",
    "Russian Blue",
    "Savannah",
    "Scottish Fold",
    "Selkirk Rex",
    "Siamese",
    "Siberian",
    "Singapura",
    "Snowshoe",
    "Somali",
    "Sphynx",
    "Tonkinese",
    "Turkish Angora",
    "Turkish Van",
    "York Chocolate",
    "Bambino",
    "Burmilla",
    "Chantilly-Tiffany",
    "Cymric",
    "Peterbald"
    ]
def cat():
    return random.choice(cat_breeds)

dog_breeds = [
    "Airedale Terrier",
    "Akita",
    "Alaskan Malamute",
    "American Bulldog",
    "Australian Cattle Dog",
    "Australian Shepherd",
    "Basset Hound",
    "Beagle",
    "Bernese Mountain Dog",
    "Bichon Frise",
    "Bloodhound",
    "Border Collie",
    "Boston Terrier",
    "Boxer",
    "Bulldog",
    "Cane Corso",
    "Cavalier King Charles Spaniel",
    "Chihuahua",
    "Chow Chow",
    "Cocker Spaniel",
    "Dalmatian",
    "Doberman Pinscher",
    "English Springer Spaniel",
    "French Bulldog",
    "German Shepherd",
    "Golden Retriever",
    "Great Dane",
    "Greyhound",
    "Havanese",
    "Irish Setter",
    "Jack Russell Terrier",
    "Labrador Retriever",
    "Lhasa Apso",
    "Maltese",
    "Miniature Pinscher",
    "Newfoundland",
    "Old English Sheepdog",
    "Papillon",
    "Pekingese",
    "Pomeranian",
    "Poodle",
    "Pug",
    "Rottweiler",
    "Saint Bernard",
    "Schnauzer",
    "Shetland Sheepdog",
    "Shih Tzu",
    "Siberian Husky",
    "Vizsla",
    "Weimaraner"
    ]
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
    '/math': math,
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
'''
while True:
    inp = input('Command: ')
    print(command(inp))
'''