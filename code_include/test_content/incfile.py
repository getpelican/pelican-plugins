# These two comment lines will not
# be included in the output
import random

insults = ['I fart in your general direction',
           'your mother was a hampster',
           'your father smelt of elderberries']

def insult():
    print random.choice(insults)
# This comment line will be included
# ...but this one won't
