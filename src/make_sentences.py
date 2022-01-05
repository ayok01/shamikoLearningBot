import re
import MeCab
from collections import deque
import random
from misskey import Misskey
import json
import requests

with open('../data/config.json', 'r') as json_file:
    config = json.load(json_file)

#Misskey.py API
misskey = Misskey(config['token']['server'], i= config['token']['i'])

#Misskey API json request用
get_tl_url = "https://" + config['token']['server'] + "/api/notes/timeline"
limit = 30
get_tl_json_data = {
    "i" : config["token"]["i"],
    "limit": limit,
}

def mk_misskey_list():
    text_list = []
    with open("../data/getword.txt", encoding='utf-8') as data:
        for line in data:
            text = line.rstrip('\n')
            text_list.append(text)
    return text_list

def get_tl_misskey():
    text_list = []
    response = requests.post(
        get_tl_url,
        json.dumps(get_tl_json_data),
        headers={'Content-Type': 'application/json'})
    hash = response.json()
    for num in range(limit):
        line = str(hash[num]["text"])
        line = re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", line)
        line = re.sub(r'@.*', "", line)
        line = re.sub(r'#.*', "", line)
        line = re.sub(r':.*', "", line)
        line = re.sub(r"<[^>]*?>", "", line)
        line = re.sub(r"\(.*", "", line)
        line = line.replace('\\', "")
        line = line.replace('*', "")
        line = line.replace('\n', "")
        line = line.replace('\u3000', "")
        line = line.replace('俺', "私")
        line = line.replace('僕', "私")
        line = line.replace(' ', "")
        deq_list = line in text_list
        if line != "None" and line != "" and deq_list == False:
            with open('../data/getword.txt', 'a') as f:
                print(line, file=f)
            text_list.append(line)
    return text_list

def mk_word_list():
    text_list = []
    with open("../data/syamiko_words.txt", encoding='utf-8') as data:
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

def mk_new_sentence(word_list, mecab_word_list):
    serihu = "".join(map(str, mk_sentence(mecab_word_list)))
    while True:
        sarch = serihu in word_list
        if serihu == []:
            serihu = "".join(map(str, mk_sentence(mecab_word_list)))
        elif sarch == False:
            serihu = serihu.replace('シャミ子', "私")
            return serihu
        else:
            serihu = "".join(map(str, mk_sentence(mecab_word_list)))

def make_sentences():
    geted_word_list = mk_misskey_list()
    word_list = mk_word_list() + get_tl_misskey()+geted_word_list
    mecab_word_list = mk_mecab_list(word_list)
    sentence_1 = mk_new_sentence(word_list,mecab_word_list)
    return sentence_1

print(make_sentences())
