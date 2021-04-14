import MeCab
mecab = MeCab.Tagger ("-Ochasen")
testwords = "今日の天気は晴れです。"
print(mecab.parse(testwords))