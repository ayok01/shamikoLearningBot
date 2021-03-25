import re
import MeCab
from collections import deque
import random
import sys
import time


def mk_getTL_list():
    text_list = []
    choice_model = []
    with open("./data/sample.txt", encoding='utf-8') as data:
        for line in data:
            if "病" in line:
                text = line.rstrip('\n')
                text_list.append(text)
    print(text_list)
    return text_list

def mk_word_list():
    text_list = []
    with open("./data/syamiko_words.txt", encoding='utf-8') as data:
        for line in data:
            char, text = line.rstrip('\n').split(" ")
            if char == "優子":
                text_list.append(text)
    return text_list

def mk_mecab_list(word_list):
    text_model = []
    for list_macab in word_list:
        t = MeCab.Tagger("-Owakati")
        parsed_text = t.parse(list_macab).replace("\n", "")
        parsed_text_list = [None] + parsed_text.split() + [None]
        for i in range(len(parsed_text_list) - 2):
            model_word = parsed_text_list[i:i+3]
            text_model.append(model_word)
    return text_model


def mk_sentence(mecab_list):
    none_model = []
    for i in mecab_list:
        if None in i:
            text_list = i
            if text_list[0] == None:
                none_model.append(text_list)
    random_word = random.choice(none_model)
    if random_word[2] == None:
        return random_word[1]
    fast_word = random_word[1], random_word[2]
    sentence = []
    sentence += random_word[1]
    tes = []
    while fast_word:
        for i in mecab_list:
            ju = i[0], i[1]
            if ju == fast_word:
                tes += [i]
        random_word = random.choice(tes)
        sentence += random_word[1]
        fast_word = random_word[1], random_word[2]
        end_word = random_word[2]
        tes = []
        if end_word == None:
            break
    return sentence

def mk_filter_word(serihu):
    text_list = []
    with open("./data/filter.txt", encoding='utf-8') as data:
        for line in data:
            line = line.replace('\n', "")
            serihu= serihu.replace(line, "not") 
    return serihu


def mk_new_sentence():
    word_list = mk_getTL_list() + mk_word_list()
    mecab_word_list = mk_mecab_list(word_list)
    serihu = "".join(map(str, mk_sentence(mecab_word_list)))
    while True:
        sarch = serihu in word_list
        filter_judg = serihu in mk_filter_word(serihu)
        if serihu == []:
            serihu = "".join(map(str, mk_sentence(mecab_word_list)))
        elif filter_judg == False:
            mastodon.status_post(serihu,visibility='private')
            serihu = "".join(map(str, mk_sentence(mecab_word_list)))
        elif sarch == False:
            serihu = serihu.replace('シャミ子', "私")
            return serihu
        else:
            serihu = "".join(map(str, mk_sentence(mecab_word_list)))


print (mk_new_sentence())



