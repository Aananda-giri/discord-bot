#!/bin/sh
# command to run this file: 

nohup python main.py >> nohup_discord.out &                # running discord bot
nohup python viber_bot/__init__.py  >> nohup_viber.out &   # running viber_bot
nohup python telegram_bot/__init__.py  >> nohup_telegram.out &   # running telegram bot outputs_to_file: nohup_telegram.out

