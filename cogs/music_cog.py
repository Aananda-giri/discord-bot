import os, discord, json, config
from discord.ext import commands
import datetime, config, nacl
from cogs.functions import *
from music import AudioYTDLP
global player, playing
import yt_dlp as youtube_dl

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False, download=False):
        SAVE_PATH = os.path.join(os.getcwd(), 'downloads')
        ydl_opts = {
              'format': 'bestaudio/best',
              'audio-format': 'mp3', 
              'restrictfilenames': True,
              'noplaylist': True,
              'nocheckcertificate': True,
              'ignoreerrors': False,
              'logtostderr': False,
              'quiet': True,
              'no_warnings': True,
              'default_search': 'auto',
              'source_address':
              '0.0.0.0',  # bind to ipv4 since ipv6 addresses  cause issues sometimes
              
              'preferredcodec': [{
                  'key': 'FFmpegExtractAudio',
                  'preferredcodec': 'webm',
                  'preferredquality': '192',
              }],
              
              'outtmpl':SAVE_PATH + '/%(title)s.%(ext)s',
        }
        #results = YoutubeSearch(url, max_results=3).to_dict()
        #vid_url = 'https://www.youtube.com' +  results[0]['url_suffix']
        #thumbnails = results[0]['thumbnails']
        #title = results[0]['title']
        #print('vid_url:{}, thumbnails:{}, title:{}, download:{},url:{}'.format(vid_url, thumbnails, title, download, url))
        
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            data = ydl.extract_info(f"ytsearch:{url}", download=download)['entries'][0]
        
        URL = data['url']
        thumbnails = data['thumbnails']
        title = data['title']
        vid_url = data['webpage_url']
        
        print(URL)
        #Renaming files if downloaded
        if download==True:
            files = os.listdir(os.path.join(os.getcwd(), 'downloads'))
            for file_name in files:
                if not file_name.endswith('.part'):
            
                    # To download files as .mp3
                    #mp3_format = os.path.join(os.getcwd(), 'downloads', file_name.replace(file_name.split('.')[-1], 'mp3'))
                    file_name = os.path.join(os.getcwd(), 'downloads', file_name)
                    os.rename(file_name, title + '.mp3')
        return(URL,thumbnails, title, vid_url)

#Downloads videb name/url and returns full filename
async def download_from_youtube(url):
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

    #return video
    #print('type_of'+str(type(video)))
    
    # Didnot work for filename we extracted did not match with actual file_name
    '''file_name=str(video['title'] + '-' +video['id'] + '.'  +video['formats'][3]['ext'])
    file_name = file_name.replace('/','_')
    '''

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







#To get current, next, previous streams
def get_stream(which=None, current=None):
        
        try:
            config.streams[0]
            print('Streams already defined')
        except:
            global streams
            with open('fm_list.json','r') as F:    
                config.streams = json.load(F)
            config.streams = config.streams['stream_links']
            print('stream: {}'.format(config.streams[0]))
            
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
                nxt = config.streams.index(current) + 1
                
                # Triggred to get next station at the end of stations list 
                if nxt >= len(config.streams):
                    nxt -= len(config.streams)
                
                current = config.streams[nxt]
                print(nxt)
            
            elif which=='prev':
                prev = config.streams.index(current) - 1
                print(prev)
                
                # Triggred to get previous station at the beginning of stations list
                if prev < 0:
                    prev += len(config.streams)
                
                
                print('current:{}, prev:{}'.format(config.streams.index(current),prev))
                
                current = config.streams[prev]
                
            return(current)

class Audio(commands.Cog, name="audio"):
    queue = {}

    def __init__(self, bot):
        self.bot = bot
        
    # _______________________________________________________________________
    # ---------------------------- For Music Bot : https://medium.com/pythonland/build-a-discord-bot-in-python-that-plays-music-and-send-gifs-856385e605a1
    # _______________________________________________________________________
    
    
    @commands.hybrid_command(
        name='join',
        help='Tells the bot to join the voice channel before playing music ')
    async def join(self, context):
        if not context.message.author.voice:
            await context.send("{} is not connected to a voice channel".format(
                context.message.author.name))
            return
        else:
            channel = context.message.author.voice.channel
            print('\nchannel:',channel)
            await channel.connect()
            await context.send("joined")

    
    
    @commands.hybrid_command(name='leave', help='To make the bot leave the voice channel')
    async def leave(self, context):
        voice_client = context.message.guild.voice_client
        if voice_client.is_connected():
            await voice_client.disconnect()
        else:
            await context.send("The bot is not connected to a voice channel.")
    
    
    @commands.hybrid_command(name='p',
                 brief='To play song note: Please enter: `.join` first',
                 help="example: `.play gangnam style`",
                 aliases=["play"])
    async def play(self, context, url):
        
        config.playing = url
        
        config.queue_by_user.put(config.playing) #put to queue
        
        if not context.message.author.voice.channel:
            await context.send("{} is not connected to a voice channel".format(
                context.message.author.name))
            return
            
        else:
            channel = context.message.author.voice.channel
        try:
          #####################################################
          ############################################################# improve with if not connected
          #####################################################
          config.player = await channel.connect()
        except:
            pass  
        # joined the channel
        try:
            server = context.message.guild
    
            voice_channel = server.voice_client
            #print('voice_channel : ' + str(voice_channel))
    
            async with context.typing():
                ytdl_data = await YTDLSource.from_url(url, loop=context.bot.loop)
                
                config.player.stop() #to stop playing if already playing another
                if len(self.queue)==0:
                    URL, thumbnails, title, vid_url = ytdl_data
                    
                    #####################################################
                    ##################################################### config.player?
                    #####################################################
                    config.player.play(discord.FFmpegPCMAudio(URL))
                else:
                    self.queue[len(self.queue)] = player
                    await context.send(f':mag_right: **Searching for** ``' + url + '``\n<:youtube:763374159567781890> **Added to queue:** ``{}'.format(player.title) + "``")
                
                
            print('vid_url:{}, thumbnails:{}, title:{}, URL:{},url:{}'.format(vid_url, thumbnails, title, URL, url))
            embed=discord.Embed(title=title,
            #description=stream['longDesc'],
            color=0x00FFFF,
            url=vid_url)
            embed.set_author(name=context.message.author)
            embed.set_thumbnail(url=thumbnails[0]['url'])
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_footer(text=f'Added by {context.author}',icon_url=context.author.avatar_url)#, url = context.message.author.avatar_url)
            
            
            message = await context.send(embed=embed)
            emos=['⏮️', '⏸️', '⏹️', '⏭️', '⬇️']
            for emoji in emos:
              await message.add_reaction(emoji)
        except Exception as ex:
            error_message = "error while playing song: {}".format(ex)
            print(error_message)
            db['errors'].append(ex)
            await context.send(error_message)
    
    
    
    
    
    
    
    
    
    
    @commands.hybrid_command(name='download',
                 brief='To download song note: Please enter: `.d song name` ',
                 help="example: `.d gangnam style`",
                 aliases=["audio", "download_audio, download_one"])
    async def d(self, context, url:str):
        print('Try download')

        async with context.typing():
            message = await context.channel.send('Downloading... \n Extracting audio... \n Please wait...')
            url, thumbnail, title, description, duration, full_download_path = await AudioYTDLP.download_audio(url, yesplaylist=False)
            await message.delete()

            try:
                await context.send(file=discord.File(full_download_path))
            except Exception as e:
                message = await context.channel.send('File size too large for server! \n Creating Download Link ...')
                s3_url = AudioYTDLP.upload_to_s3(full_download_path)
                await message.delete()
                context.send('audio download link: ' + s3_url)
            os.remove(full_download_path)
            print(' downloaded!!! ')
    
    @commands.hybrid_command(name='dall',
                 brief='To download song note: Please enter: `.d song name` ',
                 help="example: `.dall gangnam style`",
                 aliases=["audio_playlist", "download_audio_playlist, download_playlist"])
    async def dall(self, context, url:str):
        print('Try download')
        
        async with context.typing():
            message = await context.channel.send('Downloading... \n Extracting audio... \n Please wait...')
            url, thumbnail, title, description, duration, full_download_path = await AudioYTDLP.download_audio(url, yesplaylist=True)
            
            await message.delete()
            message = await context.channel.send('Creating Download Link...')
            s3_url = AudioYTDLP.upload_to_s3(full_download_path, is_folder=True)
            await message.delete()
            context.send('Playlist download link: ' + s3_url)
            
            os.remove(full_download_path)
            print(' downloaded!!! ')
    
    @commands.hybrid_command(name='pause',brief='To To pause the song currently beieng played: `.p`, To play: `.p song_name` ', help='This command pauses the song. e.g. while song is being played, press: `.p` ')
    async def pause(self, context):
        voice_client = context.message.guild.voice_client
        if voice_client.is_playing():
            await voice_client.pause()
        else:
            await context.send("The bot is not playing anything at the moment.")
    
    
    @commands.hybrid_command(name='resume', help='Resumes the song')
    async def resume(self, context):
        voice_client = context.message.guild.voice_client
        if voice_client.is_paused():
            await voice_client.resume()
        else:
            await context.send(
                "The bot was not playing anything before this. Use play_song command"
            )
    
    
    @commands.hybrid_command(name='stop', help='Stops the song')
    async def stop(self, context):
        await context.message.add_reaction('🛑')
        voice_client = context.message.guild.voice_client
        if voice_client.is_playing():
            await voice_client.stop()
            voice_client
        #os.remove(
        else:
            await context.send("The bot is not playing anything at the moment.")
    
    #_______________________________________________________________________
    # ----------------------------- ---------------------------------------
    # _______________________________________________________________________
    # ----------------------------- FM Player -----------------------------
    
    
    
    from discord import FFmpegPCMAudio
    from discord.ext.commands import Bot
    from dotenv import load_dotenv
    
    load_dotenv()
    
    #To be implemented
    global streams
    config.streams = None
    def start_load_streams():
        global streams
        try:
            config.streams[0]
        except:
            with open('test_fm_list.json','r') as F:    
                config.streams = json.load(F)
    
    
    @commands.hybrid_command(aliases=['fm', 'radio'])
    async def playfm(self, context, url: str = 'https://radionepal.news/live/audio/mp3'):

        config.playing = "fm"
        
        config.stream = get_stream()
        #url = "https://radio-streaming-serv-1.hamropatro.com/radio/8050/radio.mp3"
        #url = 'https://radionepal.news/live/audio/mp3'
        #global channel
        if not context.message.author.voice:
            await context.send("{} is not connected to a voice channel".format(
                context.message.author.name))
            return
            
        else:
            channel = context.message.author.voice.channel
    
            try:
              config.player = await channel.connect()
            except Exception as ex:
              await context.send("Exception (music.py_playfm): {}".format(ex))
              
            #joined the channel
        print('\n Playing: {}\n'.format(config.stream['url']))
        config.player.play(discord.FFmpegPCMAudio(config.stream['url']))
        #config.player.play(FFmpegPCMAudio(config.stream['url']))
        #global message
        
        embed=discord.Embed(title=config.stream['name'],
        description=config.stream['longDesc'],
        color=0x00FFFF,
        url=config.stream['url'])
        embed.set_author(
            name=context.message.author,
            icon_url=context.message.author.avatar_url
            )
            #icon_url=context.message.author.avatar_url)
        embed.set_thumbnail(url=config.stream['image'])
        
        #embed.pfp = author.avatar_url
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text=f'Added by {context.author}', icon_url=context.author.avatar_url)
        
    
        currently_playing_message = await context.send(embed=embed)
        #emojis = [':track_previous:', ':pause_button:', ':stop_button:', ':track_next:', ':record_button:', ':arrow_down:']
        emos=['⏮️', '⏸️', '⏹️', '⏭️']#, '⏺️', '⬇️']
        for emoji in emos:
            await currently_playing_message.add_reaction(emoji)
            
    @commands.hybrid_command(aliases=['s', 'sto'])
    async def stopfm(self, context):
        config.player.stop()
    
   
    
    
    
async def setup(bot):
    await bot.add_cog(Audio(bot))
