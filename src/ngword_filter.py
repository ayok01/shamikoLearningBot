import MeCab

def judgement_sentence(sentence_word):
    text_list = []
    with open("../data/filter.txt", encoding='utf-8') as data:
        for line in data:
            text = line.replace('\n','')
            print(text)
            text_list.append(text)
    print(text_list)
    if sentence_word in text_list:
        return True
    else:
        return False

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
