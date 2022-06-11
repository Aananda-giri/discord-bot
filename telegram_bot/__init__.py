from bot import start_bot

# to make config importable
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath("config") ) ) )
import config

if __name__ == "__main__":
    start_bot(config.TELEGRAM_TOKEN)
