from make_sentences import make_sentences
from ngword_filter import judgement_sentence
import numpy as np
from misskey import Misskey
import json


with open('../data/config.json', 'r') as json_file:
    config = json.load(json_file)
misskey = Misskey(config['token']['server'], i= config['token']['i'])



def note():
    if np.random.randint(1,91) == 1:
        nyanpass_status = misskey.notes_create("これで勝ったと思うなよー！")
    sentence_1= make_sentences()
    if judgement_sentence(sentence_1) != True:
        misskey.notes_create(sentence_1)