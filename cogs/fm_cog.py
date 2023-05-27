# -----------------------------------------------------
# ##################### FM Player #####################
# -----------------------------------------------------

import os, sys, discord, platform, random, aiohttp, json, youtube_dl
from discord.ext import commands
from multiprocessing import context
import time, asyncio, datetime

from cogs.functions import *
from cogs.voice_functions import *

global player


#To get current, next, previous streams
def get_stream(which=None, current=None):
        global streams
        try:
            streams[0]
            print('Streams already defined')
        except:
            with open('fm_list.json','r') as F:    
                streams = json.load(F)
            streams = streams['stream_links']
            print(streams)
            
            #global streams_url
            
            #streams=streams['stream_links']
            #streams_url = [i['url'] for i in streams]
            
        finally:
            if current==None:
                current={
                    "name": "Radio Nepal",
                    "city" : "kathmandu",
                    "url": "https://radionepal.news/live/audio/mp3",
                    "image": "https://radionepal.gov.np/wp-content/themes/rdnp/images/logo-en.png",
                    "desc": "am/sw/fm radio",
                    "longDesc": "Radio Nepal, oldest radio of nepal."
                }
            if which=='next':
                nxt = streams.index(current) + 1
                
                # Triggred to get next station at the end of stations list 
                if nxt >= len(streams):
                    nxt -= len(streams)
                
                current = streams[nxt]
                print(nxt)
            
            elif which=='prev':
                prev = streams.index(current) - 1
                print(prev)
                
                # Triggred to get previous station at the beginning of stations list
                if prev < 0:
                    prev += len(streams)
                
                
                print('current:{}, prev:{}'.format(streams.index(current),prev))
                
                current = streams[prev]
                
            return(current)



class FmRadio(commands.Cog, name="fmaradio"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command(aliases=['fm', 'radio'])
    async def playfm(self, ctx, url: str = 'http://stream.radioparadise.com/rock-128'):
        
        
        global playing
        playing = "fm"
        global currently_playing_message
        
        global stream
        stream = get_stream()
        #url = "https://radio-streaming-serv-1.hamropatro.com/radio/8050/radio.mp3"
        #url = 'https://radionepal.news/live/audio/mp3'
        #global channel
        if not ctx.message.author.voice:
            await ctx.send("{} is not connected to a voice channel".format(
                ctx.message.author.name))
            return
            
        else:
            channel = ctx.message.author.voice.channel
    
            try:
              global player
              player = await channel.connect()
            except:
              pass  
            #joined the channel
        player.play(FFmpegPCMAudio(stream['url']))
        #global message
        
        embed=discord.Embed(title=stream['name'],
        description=stream['longDesc'],
        color=0x00FFFF,
        url=stream['url'])
        embed.set_author(
            name=ctx.message.author,
            icon_url=ctx.message.author.avatar_url
            )
            #icon_url=ctx.message.author.avatar_url)
        embed.set_thumbnail(url=stream['image'])
        
        #embed.pfp = author.avatar_url
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text=f'Added by {ctx.author}', icon_url=ctx.author.avatar_url)
        
    
        currently_playing_message = await ctx.send(embed=embed)
        #emojis = [':track_previous:', ':pause_button:', ':stop_button:', ':track_next:', ':record_button:', ':arrow_down:']
        emos=['⏮️', '⏸️', '⏹️', '⏭️']#, '⏺️', '⬇️']
        for emoji in emos:
            await currently_playing_message.add_reaction(emoji)
    

            
    @commands.hybrid_command(aliases=['s', 'sto'])
    async def stopfm(ctx):
        player.stop()
    
async def setup(bot):
    await bot.add_cog(FmRadio(bot))
