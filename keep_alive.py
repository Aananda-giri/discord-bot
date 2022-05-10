#------------ TO keep alive -------------------------------
#source:https://stackoverflow.com/questions/54722596/keep-discord-bot-online-on-repl-it

from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def main():
  return "Your Bot Is Ready"
  
def home():
    return"Hello, I am alive!"
    
def main():
  return "Your Bot Is Ready"

def run():
  app.run(host="0.0.0.0", port=8000)

def keep_alive():
  server = Thread(target=run)
  server.start()

