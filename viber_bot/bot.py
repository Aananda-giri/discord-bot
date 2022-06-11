#!/usr/bin/python3.8
'''
# A very simple Flask Hello World app for you to get started with...

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from Flask!'
'''







#Source: https://www.youtube.com/watch?v=oAr6jLg1wiY


from flask import Flask, request, Response, render_template
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages.text_message import TextMessage
from viberbot.api.messages import RichMediaMessage, PictureMessage, KeyboardMessage

from viberbot.api.viber_requests import ViberMessageRequest, ViberFailedRequest, ViberConversationStartedRequest
from viberbot.api.viber_requests import ViberSubscribedRequest
import os, random, requests, json, time, youtube_dl, datetime

#from home.viberbot.mysite.discord_bot.db import run_discord_bot
#For Chatterbot implementation
#from chatterbot import ChatBot
'''from chatterbot.trainers import ChatterBotCorpusTrainer
bot = ChatBot("Aries", storage_adapter="chatterbot.storage.SQLStorageAdapter")
trainer = ChatterBotCorpusTrainer(bot)
trainer.train("chatterbot.corpus.english")'''


global trigger_words, encouragements, chat_activated
chat_activated = False

global viber
viber = None

global TMDB_API_KEY
TMDB_API_KEY = None



app = Flask(__name__)

@app.route('/')
def hello_world():
    #return 'Hello from Flask!'
    return render_template('index.html')

#to get quotes
def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return (quote)

def get_jokes(no_of_jokes=1):
    headers = {
        "Accept-Language" : "en-US,en;q=0.5",
        "User-Agent": "Defined",
    }
    #response = requests.get("https://imao.herokuapp.com/jokes/api/{}/".format(int(no_of_jokes)))
    response = requests.get("https://imao.herokuapp.com/api/jokes/random/")
    jokes = []
    #for joke in response.json():
    joke = response.json()
    jokes.append(str(joke['title']) + '  \n' + str(joke['body']) + ' - ' + '\n\t')
    return (str(jokes[0]))

def bot_reply(msg):
    reply = bot.get_response(msg)
    return(reply)

def activate_chat(boolean_for_activating_chat, msg):
    global chat_activated
    chat_activated = boolean_for_activating_chat

def save_conversation(message=None, reply=None, author=None):
    print('message:{} {} {}'.format(message, reply, author))
    if message==None:
        pass
    else:
        with open('/home/viberbot/mysite/messages.json','a') as file:
            json.dump({'message':message, 'reply':reply, 'author':author, 'datetime':str(datetime.datetime.now())}, file, indent = 4)
    return


'''
SAMPLE_RICH_MEDIA = {
  "BgColor": "#69C48A",
  "Buttons": [
    {
      "Columns": 6,
      "Rows": 1,
      "BgColor": "#454545",
      "BgMediaType": "gif",
      "BgMedia": "http://www.url.by/test.gif",
      "BgLoop": "true",
      "ActionType": "open-url",
      "Silent": "true",
      "ActionBody": "www.tut.by",
      "Image": "www.tut.by/img.jpg",
      "TextVAlign": "middle",
      "TextHAlign": "left",
      "Text": "<b>example</b> button",
      "TextOpacity": 10,
      "TextSize": "regular"
    }
  ]
}

SAMPLE_ALT_TEXT = "upgrade now!"

rich_message = RichMediaMessage(rich_media=SAMPLE_RICH_MEDIA, alt_text=SAMPLE_ALT_TEXT);'''

rich_message="wtf are rich messages !"
#To reply the messages
encouragements = ['you are the best coder in the world', 'way to go!', 'you are the best programmer in the world', 'you are the best', 'now or never', "100 years from now you won't be here, make it worth", 'inspirational_message', 'inspirational_message']
trigger_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing", "hurt","pain"]
def get_reply(viber_request):
    text = True
    message = str(viber_request.message.text).lower().strip()

    if any(word in message for word in trigger_words):
            reply = random.choice(encouragements)

    elif message.split(' ')[0]=='activate':
        activate_chat(True, message)
        reply = 'Chat activated'

    elif message.split(' ')[0] == 'deactivate':
        activate_chat(False)
        reply = 'Chat deactivated'

    elif not chat_activated:
        if str(message).lower()=='joke':
            reply = get_jokes()
        elif message.strip() == 'meme':
            text = False
            sub_reddit = random.choice(['dankmemes', 'memes'])
            while True:
                url = requests.get("https://meme-api.herokuapp.com/gimme/{}".format(sub_reddit)).json()['url']
                if url.split('.')[-1] != 'gif':
                    break
            reply = {'url':url, 'text':sub_reddit}
        elif message == 'nude':
            print('Fucn\n\nfuck')
            text = False
            sub_reddit = random.choice(['hentai', 'BustyPetite'])#, 'fuck',])
            print(sub_reddit)
            url = requests.get("https://meme-api.herokuapp.com/gimme/{}".format(sub_reddit)).json()['url']
            print(url)
            reply = {'url':url, 'text':sub_reddit}
            print(reply)
        elif message == 'random':
            text = False
            sub_reddit = random.choice(['random'])
            url = requests.get("https://meme-api.herokuapp.com/gimme/{}".format(sub_reddit)).json()
            reply = {'url':url['url'], 'text':url['subreddit']}

        elif message == 'creepy':
            text = False
            sub_reddit = random.choice(['creepy'])
            url = requests.get("https://meme-api.herokuapp.com/gimme/{}".format(sub_reddit)).json()
            reply = {'url':url['url'], 'text':url['subreddit']}
        elif message == 'rich':
            reply=rich_message
        elif message=='secret_features':
            #text = True
            #url = requests.get("https://meme-api.herokuapp.com/gimme/{}".format(sub_reddit)).json()['url']
            reply = """/* Donate to unlock */ \n\n esewa/khalti id:\n 9840445934 \n\n Paytreon:\nhttps://www.patreon.com/join/7095305? \n\n Coinbase:\n https://commerce.coinbase.com/checkout/63a4b635-8510-459f-b091-a4f0697993e6"""
        elif message.split(' ')[0] == 'movie':
            search_term = message.split(' ',1)[1:]
            tmdb_url = f'https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&gener&language=en-US&page=1&include_adult=true&query={search_term}'

            result = requests.get(tmdb_url).json()

            movie_url = "https://www.2embed.ru/embed/tmdb/movie?id={}".format(result['results'][0]['id'])
            reply= "Movie: " + str(result['results'][0]['original_title']) +'\n'+ movie_url + "\n\nplease enter: \n`movie movie name`\nto get links of movies"
        elif message.split(' ')[0] == 'tv':
                #try:
                season = int(message.lower().split(' ')[1].replace('s',''))
                episode = int(message.lower().split(' ')[2].replace('e',''))
                search_term = message.lower().split(' ',3)[3]
                tmdb_url = f"https://api.themoviedb.org/3/search/tv?api_key={TMDB_API_KEY}&gener&language=en-US&page=1&include_adult=true&query={search_term}"
                #tmdb_url = f'https://api.themoviedb.org/3/search/tv?api_key={TMDB_API_KEY}&gener&language=en-US&page=1&include_adult=true&query={}'.format(search_term)

                result = requests.get(tmdb_url).json()
                tv_id = result['results'][0]['id']

                episode_url = f"https://www.2embed.ru/embed/tmdb/tv?id={tv_id}&s={season}&e={episode}/"

                # e.g. https://www.2embed.ru/embed/tmdb/tv?id=84958&s=1&e=1

                reply= "Tv_series: " + str(search_term) +'\n'+ episode_url + "\n\nplease enter: \n`tv tv_series_name s1 e1 loki`\nto see specific epicode e.g. season 1 episode 1"
                #except:
                #reply = "Invalid tv series or format: \n\nplease enter: \n`tv s1 e1 series_name`\nto see specific epicode e.g. season 1 episode 1"
        else:
            reply = str(get_quote())
            #text = "Your id is: " + str(viber_request.sender.id)

    else:
        # Chat is activated and have to get reply
        bot_reply(message)
    #viber_request.sender
    #UserProfile[name=Aananda Giri, avatar=None, id=GgTpnxng91MeuVMk/f04Bg==, country=NP, language=en-GB, api_version=10
    author = {'name':viber_request.sender.name, 'id':viber_request.sender.id}
    save_conversation(message, reply, author)
    #reply = str(reply) + str(str(viber_request.get_user)) + 'id' + str(viber_request.get_user.id)
    return(reply, text)


secret_keyboard={
"Type": "keyboard",
"Buttons": [
	{
	"Columns": 2,
	"Rows": 1,
	"BgColor": "#FF0000",
	#"BgMedia": "https://media.istockphoto.com/photos/boudhanath-iconic-buddhist-stupa-and-pilgrims-at-sunset-kathmandu-picture-id639470672?b=1&k=20&m=639470672&s=170667a&w=0&h=6zP55p-pJDixV9fPIG-wiKoMtzYVKD6JX8k38UqzhAk=",
	"BgMediaType": "picture",
	"BgLoop": True,
	"ActionType": "reply",
	"ActionBody": "nude",#This will be sent to your bot in a callback
	"ReplyType": "message",
	"Text": "nude"
	},
]}

keyboard={
"Type": "keyboard",
"Buttons": [
	{
	"Columns": 3,
	"Rows": 2,
	"BgColor": "#97FF00",
	#"BgMedia": "https://media.istockphoto.com/photos/boudhanath-iconic-buddhist-stupa-and-pilgrims-at-sunset-kathmandu-picture-id639470672?b=1&k=20&m=639470672&s=170667a&w=0&h=6zP55p-pJDixV9fPIG-wiKoMtzYVKD6JX8k38UqzhAk=",
	"BgMediaType": "picture",
	"BgLoop": True,
	"ActionType": "reply",
	"ActionBody": "tv s1 e1 loki",#This will be sent to your bot in a callback
	"ReplyType": "message",
	"Text": "tv series"
	},{
	"Columns": 3,
	"Rows": 2,
	"BgColor": "#97FF00",
	#"BgMedia": "https://media.istockphoto.com/photos/boudhanath-iconic-buddhist-stupa-and-pilgrims-at-sunset-kathmandu-picture-id639470672?b=1&k=20&m=639470672&s=170667a&w=0&h=6zP55p-pJDixV9fPIG-wiKoMtzYVKD6JX8k38UqzhAk=",
	"BgMediaType": "picture",
	"BgLoop": True,
	"ActionType": "reply",
	"ActionBody": "movie iron man",#This will be sent to your bot in a callback
	"ReplyType": "message",
	"Text": "movie iron man"
	},{
	"Columns": 3,
	"Rows": 2,
	"BgColor": "#e6f5ff",
	#"BgMedia": "https://media.istockphoto.com/photos/boudhanath-iconic-buddhist-stupa-and-pilgrims-at-sunset-kathmandu-picture-id639470672?b=1&k=20&m=639470672&s=170667a&w=0&h=6zP55p-pJDixV9fPIG-wiKoMtzYVKD6JX8k38UqzhAk=",
	"BgMediaType": "picture",
	"BgLoop": True,
	"ActionType": "reply",
	"ActionBody": "meme",#This will be sent to your bot in a callback
	"ReplyType": "message",
	"Text": "meme"
	},{
	"Columns": 3,
	"Rows": 2,
	"BgColor": "#e6f5ff",
	#"BgMedia": "https://media.istockphoto.com/photos/boudhanath-iconic-buddhist-stupa-and-pilgrims-at-sunset-kathmandu-picture-id639470672?b=1&k=20&m=639470672&s=170667a&w=0&h=6zP55p-pJDixV9fPIG-wiKoMtzYVKD6JX8k38UqzhAk=",
	"BgMediaType": "picture",
	"BgLoop": True,
	"ActionType": "reply",
	"ActionBody": "quote",#This will be sent to your bot in a callback
	"ReplyType": "message",
	"Text": "quote"
	},{
	"Columns": 3,
	"Rows": 2,
	"BgColor": "#e6f5ff",
	#"BgMedia": "https://media.istockphoto.com/photos/boudhanath-iconic-buddhist-stupa-and-pilgrims-at-sunset-kathmandu-picture-id639470672?b=1&k=20&m=639470672&s=170667a&w=0&h=6zP55p-pJDixV9fPIG-wiKoMtzYVKD6JX8k38UqzhAk=",
	"BgMediaType": "picture",
	"BgLoop": True,
	"ActionType": "reply",
	"ActionBody": "random",#This will be sent to your bot in a callback
	"ReplyType": "message",
	"Text": "random"
	},{
	"Columns": 3,
	"Rows": 2,
	"BgColor": "#e6f5ff",
	#"BgMedia": "https://media.istockphoto.com/photos/boudhanath-iconic-buddhist-stupa-and-pilgrims-at-sunset-kathmandu-picture-id639470672?b=1&k=20&m=639470672&s=170667a&w=0&h=6zP55p-pJDixV9fPIG-wiKoMtzYVKD6JX8k38UqzhAk=",
	"BgMediaType": "picture",
	"BgLoop": True,
	"ActionType": "reply",
	"ActionBody": "creepy",#This will be sent to your bot in a callback
	"ReplyType": "message",
	"Text": "creepy"
	},{
	"Columns": 3,
	"Rows": 2,
	"BgColor": "#e6f5ff",
	#"BgMedia": "https://media.istockphoto.com/photos/boudhanath-iconic-buddhist-stupa-and-pilgrims-at-sunset-kathmandu-picture-id639470672?b=1&k=20&m=639470672&s=170667a&w=0&h=6zP55p-pJDixV9fPIG-wiKoMtzYVKD6JX8k38UqzhAk=",
	"BgMediaType": "picture",
	"BgLoop": True,
	"ActionType": "reply",
	"ActionBody": "joke",#This will be sent to your bot in a callback
	"ReplyType": "message",
	"Text": "joke"
	},{
	"Columns": 3,
	"Rows": 2,
	"BgColor": "#e6f5ff",
	#"BgMedia": "https://media.istockphoto.com/photos/boudhanath-iconic-buddhist-stupa-and-pilgrims-at-sunset-kathmandu-picture-id639470672?b=1&k=20&m=639470672&s=170667a&w=0&h=6zP55p-pJDixV9fPIG-wiKoMtzYVKD6JX8k38UqzhAk=",
	"BgMediaType": "picture",
	"BgLoop": True,
	"ActionType": "reply",
	"ActionBody": "secret_features",#This will be sent to your bot in a callback
	"ReplyType": "message",
	"Text": "secret_features"
	}
    ]
}
message = KeyboardMessage(tracking_data='tracking_data', keyboard=keyboard)
@app.route('/', methods=['POST'])
def incoming():
    # this library supplies a simple way to receive a request object
    viber_request = viber.parse_request(request.get_data())

    if isinstance(viber_request, ViberMessageRequest):
        if str(viber_request.message.text).lower()=='key':
            viber.send_messages(viber_request.sender.id, [
                TextMessage(text='secreet_keyboard', keyboard=secret_keyboard)
            ])
        else:
            reply, text = get_reply(viber_request)
            if text:
                viber.send_messages(viber_request.sender.id, [
                    TextMessage(text=reply, keyboard=keyboard)
                ])
            else:

                viber.send_messages(viber_request.sender.id, [
                    PictureMessage(media=reply['url'], text=reply['text'], keyboard=keyboard)
                ])
    elif isinstance(viber_request, ViberSubscribedRequest):
        viber.send_messages(viber_request.get_user.id, [
            TextMessage(text="thanks for subscribing!")#"Hvala što ste se prijavili na ovu uslugu!"
        ])
    elif isinstance(viber_request, ViberConversationStartedRequest) :
	    viber.send_messages(viber_request.get_user().get_id(), [
			TextMessage(text="Welcome!")
		])
    #elif isinstance(viber_request, ViberFailedRequest):
    #    logger.warn("client failed receiving message. failure: {0}".format(viber_request))

    return Response(status=200)


#Downloads file and returns full filename
def download_from_youtube(url):
    SAVE_PATH = os.path.join(os.getcwd(), 'downloads')

    ydl_opts = {
        'format': 'bestaudio/best',
        'preferredcodec': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'webm',
        'preferredquality': '192',
        }],'outtmpl':SAVE_PATH + '/%(title)s.%(ext)s',
    }

    print(' downloading!!! ')
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
        except:
            video = ydl.extract_info(f"ytsearch:{url}", download=True)['entries'][0]
        else:
            video = ydl.extract_info(url, download=False)
    files = os.listdir(os.path.join(os.getcwd(), 'downloads'))
    for file_name in files:
        if not file_name.endswith('.part'):
            # To download files as .mp3
            mp3_format = os.path.join(os.getcwd(), 'downloads', file_name.replace(file_name.split('.')[-1], 'mp3'))
            file_name = os.path.join(os.getcwd(), 'downloads', file_name)
            os.rename(file_name, mp3_format)
            print('file_name: {}'.format(file_name))
            print('mp3_format: {}'.format(mp3_format))
            return(mp3_format)

def start_bot(VIBER_AUTH_TOKEN, TMDB_KEY):
    # initializes viber
    global viber
    viber = Api(BotConfiguration(
    name='pizzabox',
    avatar='https://media.newyorker.com/photos/593581e785bd115baccba6d2/',
    auth_token=VIBER_AUTH_TOKEN
    ))

    global TMDB_API_KEY
    TMDB_API_KEY = TMDB_KEY

    # runs the flask app
    app.run(debug=True)

if __name__ == "__main__":
    start_bot(config.VIBER_AUTH_TOKEN, config.TMDB_API_KEY)

  # viber_thread = threading.Thread(target = start_viber_bot, args=(config.VIBER_AUTH_TOKEN, config.TMDB_API_KEY))
  # viber_thread.setDaemon(True)
  # viber_thread.start()    # starts twitter thread
  
  
#     app.run(host='https://viberbot.pythonanywhere.com/', port=8080, debug=True)
#     #run_discord_bot()
#     '''print('Hrlolo Woslld')
#     scheduler = BackgroundScheduler()
#     job = scheduler.add_job(start_scrapping, 'interval', minutes=1)
#     scheduler.start()'''


'''import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install('chatterbot')'''

'''
#SCRIPT TO SET A WEBHOOK: (run only once in python locally)
rom viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration

viber = Api(BotConfiguration(
 name ='Kupujem Prodajem Notifikator',
 avatar='',
    auth_token='asdasdasdasdas'
))
viber.set_webhook('https://viberbot.pythonanywhere.com')
'''
