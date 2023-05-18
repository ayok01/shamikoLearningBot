from make_sentences import make_sentences
from ngword_filter import judgement_sentence
import json
import websockets
from misskey import Misskey


with open('../data/config.json', 'r') as json_file:
    config = json.load(json_file)

TOKEN= config['token']['i']
msk = Misskey(config['token']['server'], i=TOKEN)
MY_ID = msk.i()['id']
WS_URL='wss://misskey.io/streaming?i='+TOKEN

async def on_note(note):
 if note.get('mentions'):
  if MY_ID in note['mentions']:
   print("this リプライid =>", note['id'])
   sentence_1= make_sentences()
   if judgement_sentence(sentence_1) != True:
    msk.notes_create(sentence_1, reply_id=note['id'])

async def runner():
 async with websockets.connect(WS_URL) as ws:
  await ws.send(json.dumps({
   "type": "connect",
   "body": {
     "channel": "homeTimeline",
     "id": "test"
   }
  }))

  while True:
   data = json.loads(await ws.recv())
   if data['type'] == 'channel':
    if data['body']['type'] == 'note':
     note = data['body']['body']
     await on_note(note)

