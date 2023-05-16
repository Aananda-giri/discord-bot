### run bots:
- installing requirements

pip install -r requirements.txt

- running bots in background
bash ./bots_startup_scripts.sh

- stopping bots

ps -Af | grep -v grep | grep  main.py   # list processes
ps -Af | grep -v grep | grep  __init__.py   # list processes <process_id>
sudo kill -9 p_id  #  repeat for each process process listed by above command

### python packages:<br>
replit
scrapy
* asyncpraw
* ffmpeg
* pynacl  : for voice functions
* scrapy
* qrcode
flask
youtube_dl
qrcode
config
python-dotenv
twisted
asyncpraw

ffmpeg
prawcore
discord.py
aio.http



##debugged_cogs:
- reddit
- general
- help
- games
- music


##debug:
commands.qr, commands.riddles ⬇️

##databases:
from replit import db
- db['unleash_ioe_notifi'] = [channels_id_list]
- db['unleash'] = {'channel_id':['subreddits']}

- esay search, complicateed update/retrive
- db['count_ids'] = [id1, id2, id3, ...]
- db['count_values'] = [val1, val2, val3, ...]

easy update, difficult search
db['count_ids']    = [[]]
db['last_counter'] = [[]]
db['count_values'] = [[]]

def append(value):
    

    

    
word_chain_game (count_modification):
db['count_ids']    -> db['chain_ids'] = []
db['last_counter'] -> db['last_chain_author'] = {}  #make it list
db['count_values'] -> db['chain_length'] = []   # length of chain
db['last_chain_word'] = []

## resources:
sharing global variables across models
* https://docs.python.org/3/faq/programming.html#how-do-i-share-global-variables-across-modules

## todo
- [ ] update reddit help
- unleash redit -> enable/disable   -> via abstraction
- replit.py: store to db/backup
time=35 # replit.py basics

# Done
- [X] Game: Count
- [X] Debug unleash reddit
- [X] .vent: echo message attachments