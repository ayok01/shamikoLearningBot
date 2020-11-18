from websocket import create_connection
import time
from discord.ext import tasks
import discord
import re
import MeCab
from collections import deque
import random
import tweepy

import json
import codecs
import requests
import re


client = discord.Client()
TOKEN = "NzY4ODQxNDkxNDIxNDYyNTkw.X5GVbw.bgTA2UTSUr5hcFXVs_nvdY7xZeI"
channel_id = 768846161297276929
channel_sent = None

# CK = "hxIMXjJuFq1Sor3E6Ac7cw2pN"
# CS = "Z9Yg3Nc7A8cszoMDzgZQlr5oPjtWbd68N00GPXCNYO10jRbWAI"
# AT = "1168017285203648514-720aHEmyVNfKbtYdqhLjSMYXWAQeIb"
# AS = "0TlgCVPofm1o4pJOPGspmvRxNPIaXKCSQIN6ibD5pQt06"
# auth = tweepy.OAuthHandler(CK, CS)
# auth.set_access_token(AT, AS)
# api = tweepy.API(auth)

post_url = "https://misskey.io/api/notes/create"
get_tl_url = "https://misskey.io/api/notes/timeline"
limit = 30
get_tl_json_data = {
    "i": "qJ6pGhE0rqAm8nAxrpuzgAmY1hwOcvS5",
    "limit": limit,
}


# def get_tl():
#    text_list = []
#    for status in api.home_timeline():
#        line = re.sub(
#            r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", status.text)
#        line = re.sub("RT", "", line)
#        line = re.sub(r'@.*', "", line)
#        line = re.sub(r'#.*', "", line)
#        line = line.replace('\n', "")
#        text_list.append(line)
#    return(text_list)
#

def mk_misskey_list():
    text_list = []
    with open("./data/sample.txt", encoding='utf-8') as data:
        for line in data:
            text = line.rstrip('\n')
            text_list.append(text)
    return text_list


def get_tl_misskey(text_list):
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
            with open('./data/sample.txt', 'a') as f:
                print(line, file=f)
            text_list.append(line)
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


test = mk_misskey_list()
word_list = test + mk_word_list() + \
    get_tl_misskey(test)
mecab_word_list = mk_mecab_list(word_list)


def mk_new_sentence():
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


ws = create_connection(
    "wss://misskey.io/streaming?i=qJ6pGhE0rqAm8nAxrpuzgAmY1hwOcvS5")

json_data = {
    "type": "connect",
    "body": {
        "channel": "main",
        "id": "mention"
    }
}

ws.send(json.dumps(json_data))


while True:
    hash = ws.recv()
    test = json.loads(hash)
    if test["body"]["type"] == "mention":
        if test["body"]["body"]["user"]["username"] != "Syamikobot":

            serihu = mk_new_sentence().replace('None', '')
            print(serihu)
            if serihu != None:
                post_json_data = {
                    "i": "qJ6pGhE0rqAm8nAxrpuzgAmY1hwOcvS5",
                    "text": serihu,
                    "replyId": test["body"]["body"]["id"]
                }
                requests.post(
                    post_url,
                    json.dumps(post_json_data),
                    headers={'Content-Type': 'application/json'})