import itertools
import string
from db_manager import sess, AlloTips, get_or_create


def generator(symbols, count):
    yield from itertools.product(*([symbols] * count))


def create_tips():

    for count in range(1, 4):

        for tip in generator(string.ascii_lowercase + string.digits, count):
            sess.add(get_or_create(AlloTips, {"request": ''.join(tip)}))
            sess.commit()