# from sqlitedict import SqliteDict
#db = SqliteDict('./environ_vars.sqlite', autocommit=True)

from discord.ext import commands
from cogs.functions import get_embeded_message, db
import config



# from discord import Embed
# from discord.ext.commands import Bot, Cog
import random, string

from database import db
count_db = db('count')
chain_db = db('chain')


class Games(commands.Cog, name="games"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='count',
                 brief='`.count start` to start counting in a channel',
                 help='Plesae enter `.help` for help', aliases=[''])
    async def count(self, context, *args):
        print("\n Count Invoked \n")
        what = ' '.join(args)
        
        count_channel_exists_in_db = count_db.exists(str(context.channel.id))
        count_data = count_db.get_one(str(context.channel.id))
        
        if what == 'score' or what=='scores':
            # get count/chain status of a channel
            channel_id_index = config.count_ids.index(str(context.channel.id))
            embed = get_embeded_message(context, 'count_logs', f'current_count: {count_data["current_count"]}, last_counter: {count_data["last_counter"]}', author=True)
            await context.send(embed = embed)
            
        if what == 'start' or (not count_channel_exists_in_db and what==''):
            print("\nCount Starting\n");
            if count_channel_exists_in_db:#db.get('count_ids'):
                embed = get_embeded_message(context, 'count started', f'current_count: {count_data["current_count"]}')
                await context.send(embed = embed)
            else:
                # add new channel to count db
                count_db.add_one_chain_word(channel_id = str(context.channel.id), current_word='0', current_author='', current_score='0', highest_score='0')
                
                embed = get_embeded_message(context, 'count started', 'starting with: 1')
                await context.send(embed = embed)
        
        elif what == 'stop' or (count_channel_exists_in_db and what==''):
            print("\nCount stopping\n");
            if count_channel_exists_in_db:#db.get('count_ids'):
                print("trying to remove counts")
                #channel_id_index = db.get('count_ids').index(str(context.channel.id))
                count_db.remove_one_chain_word(str(context.channel.id))
                
                embed = get_embeded_message(context, 'count Stopped', f'description: \n channel_id: {context.channel.id} \n current_count: {count_data["current_count"]} \n last_counter: {count_data["last_counter"]} \n current_score: {count_data["current_score"]} \n highest_score: {count_data["highest_score"]}')
                
                await context.send(embed = embed)
            else:
                embed = get_embeded_message(context, 'count Stoppted', 'It was never started')
                await context.send(embed = embed)
    
    @commands.command(name='chain',
                 brief='`.chain start` to start word chain in a channel',
                 help='Plesae enter `.help` for help', aliases=['word_chain'])
    async def chain(self, context, *args):
        print("\n Chain Invoked \n")
        what = ' '.join(args)
        
        if what == '':
            channel_id_index = config.chain_ids.index(str(context.channel.id))
            embed = get_embeded_message(context, 'word_logs', 'current_word: {}, last_word_author: {}, score: {}'.format(config.chain_values[channel_id_index], config.last_chain_author[str(context.channel.id)], config.chain_length[channel_id_index]))
            await context.send(embed = embed)
        elif what == 'start':
            print("\nChain Starting\n");
            if str(context.channel.id) in config.chain_ids:#db.get('chain_ids'):
                index_of_channel_id = config.chain_ids.index(str(context.channel.id))
                embed = get_embeded_message(context, 'chain started', 'It was already there, **last_word:{}**'.format(config.last_chain_word[index_of_channel_id]))
                
                await context.send(embed = embed)
            else:
                
                '''db.append('chain_ids', str(context.channel.id))
                db.append('chain_length', 0)
                db.update('last_chain_author', str(context.channel.id), '')
                random_letter = db.get_random_letter()
                db.append('last_chain_word', random_letter)'''
               
                config.chain_ids.append(str(context.channel.id)) 
                config.chain_length.append(0)
                config.last_chain_word.append('')
                config.last_chain_author[str(context.channel.id)] = ''      # {}
                                
                embed = get_embeded_message(context, 'chain started', '**starting with \"{}\"**'.format('anything you want'))#random_letter))
                await context.send(embed = embed)

        elif what == 'stop':
            print("\nCount stopping\n");
            if str(context.channel.id) in config.chain_ids:#db.get('chain_ids'):
                index_of_channel_id = config.chain_ids.index(str(context.channel.id))
                print("trying to remove counts")
                
                '''db.pop_by_index('chain_length', index_of_channel_id) # []
                db.remove_by_value('chain_ids', str(context.channel.id)) #[]
                db.pop_by_index('last_chain_author', str(context.message.author))
                db.pop_by_index('last_chain_word', index_of_channel_id)# []'''
                
                config.chain_length.pop(index_of_channel_id) # []
                config.chain_ids.pop(index_of_channel_id) #[]
                config.last_chain_word.pop(index_of_channel_id)# []
                config.last_chain_author.pop(str(context.message.author))
                
                embed = get_embeded_message(context, 'count Stopped', 'description')
                await context.send(embed = embed)
            else:
                embed = get_embeded_message(context, 'count Stoppted', 'It was never started')
                await context.send(embed = embed)
        else:
                #db.append('chain_length', 0)
                #db.update('last_chain_author', str(context.channel.id), '')
                #db.append('last_chain_word', what.lower().strip())
                
                # updating last_chain_word by 'word' if entered .chain 'word'
                config.last_chain_author[str(context.channel.id)] = str(context.message.author)
                index_of_channel_id = config.chain_ids.index(str(context.channel.id))
                config.last_chain_word[index_of_channel_id] = what.lower().strip()
                
    @commands.command(name='logs',
                 brief='`.logs` to see game logs',
                 help='Plesae enter `.help` for help', aliases=['game_logs'])
    async def logs(self, context, *args):
        print('\n logs activated \n')
        chain_length = list(config.chain_length)  #db.get('chain_length')
        chain_ids = list(config.chain_ids)    #db.get('chain_ids')
        last_chain_author = dict(config.last_chain_author)    #db.get('last_chain_author')
        last_chain_word = list(config.last_chain_word)    #db.get('last_chain_word')
        await context.send(f"chain_length{chain_length}, chain_ids: {chain_ids}, last_chain_author:{last_chain_author}, last_chain_word:{last_chain_word}")
    
    @commands.command(name='score',
                 brief='`.scores` to see game logs',
                 help='Plesae enter `.help` for help', aliases=['scores'])
    async def score(self, context, *args):
        print("\nscores activated\n");
        channel_id_index = config.count_ids.index(str(context.channel.id))
        
        embed = get_embeded_message(context, 'Score:', f'chain_word:{chain_length[channel_id_index]} , \n numbers_count: {count_values[channel_id_index]}')
        await context.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Games(bot))
    #bot.add_cog(WordChain(bot))
    #bot.add_cog(Slash(bot))
