#!/bin/sh
# command to run this file: 

nohup python main.py >> logs/nohup_discord.out &                # running discord bot
nohup python viber_bot/__init__.py  >> logs/nohup_viber.out &   # running viber_bot
nohup python telegram_bot/__init__.py  >> logsnohup_telegram.out &   # running telegram bot outputs_to_file: nohup_telegram.out

