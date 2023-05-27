import os, requests
from discord.ext import commands
from cogs.functions import get_embeded_message
# from replit import db
from database import db
import config

# import math, asyncpraw, asyncprawcore
# import config, discord
# from spiders import run_spider

async def send_news(channel, country="", how_many = 10, language='en', last_country=False):
  if country=='np':
    '''run_spider()  # saves /mainnews urls to  db['gorkhapatra_articles']
    urls = db['gorkhapatra_articles']
    for url in urls:
      await channel.send(url)'''
    feed = requests.get('https://www.onlinekhabar.com/feed')
    #links = []
    for line in feed.content.decode('utf-8').split('<link>'):
      if '</link>' in line:
        link = line.split('</link>')[0]
        if link.strip().lower() != 'https://www.onlinekhabar.com':
          #links.append(link)
          await channel.send(link)
  else:
    if country=="" or country=="world":
        api_link = f"https://newsapi.org/v2/top-headlines?country=&category=business&apiKey={config.NEWS_API_KEY}&language={language}"
        # api_link = f"https://newsapi.org/v2/top-headlines?country=&category=business&apiKey={os.environ['NEWS_API_KEY']}&language={language}"
    else:
      api_link = f"https://newsapi.org/v2/top-headlines?country={country}&category=business&apiKey={config.NEWS_API_KEY}"
      # api_link = f"https://newsapi.org/v2/top-headlines?country={country}&category=business&apiKey={os.environ['NEWS_API_KEY']}" # replit native
      #api_link = "https://newsapi.org/v2/top-headlines?category=business&apiKey=19506b2fc6aa4bddb287495e65dd0cd0"
      news = requests.get(api_link).json()
      for new in news['articles'][:10]:
          url = new['url']
          title = new['title']
          description = new['description']
          image = new['publishedAt']
          await channel.send(url)
  
  if last_country:
    # send subscription list at the end of sending news
    # print(f'\n\nnews.send_news:  channel_id:{channel.id}\n\n')
    embed=get_embeded_message(channel, 'subscription List: [\'news\']\t', f"{db('news').get_one(str(channel.id))}", author=False)
    await channel.send(embed=embed)
    print('\n news.send_news: Unleashed news\n')
  

class News(commands.Cog, name="news_commands"):
  def __init(self, bot):
    self.bot=bot
  
  @commands.hybrid_group(name='subscribe', aliases=[],  brief='subscribe to news', help='e.g. `.subscribe news us 3` To subscribe to \'us\' daily news 3 at a time', fallback="subscribe")
  async def news(self, context, country='world', how_many=7):
      
      channel_id = str(context.channel.id)
      # print('country:{}'.format(country))

      news_db = db('news')   # {'np': {'ch1_id':3, 'ch2_id':3, }}
      # set and update country,how_many database
      news_db.add_one(channel_id = channel_id, gener=country, how_many=how_many)
      message = 'added daily news to channel: '
      print('\n news.subscribe: subscribed to news country:{country}\n')
          
      message = f'\n\nsubscribed:country: {country}, how_many:{how_many}, channel_id:{channel_id}'
      
      embed = get_embeded_message(context, message)
      await context.send(embed=embed) # send confirmation message
      await send_news(context.channel, country=country) # send news

  @news.command(name='unsubscribe', aliases=[],  brief='unsubscribe news from a channel', help='e.g. `.unsubscribe news us gb` To unsubscribe to \'us\' and \'gb\' daily news from a channel')
  async def unsubscribe(self, context, countries='all'):
    '''
      To unsubscribe one/list of countries from news in a channel
    
    '''
    # --------------
    # pseudocode
    # --------------
    news_db = db('news')
    if countries=='all':
      countries = news_db.get_all_countries(channel_id)
    countries=[countries]
    
    channel_id = str(context.channel.id)
    message = news_db.remove_many(channel_id, countries)
                        
    embed = get_embeded_message(context, message + str(countries))
    await context.send(embed=embed)
  
  @news.command(name='subscription', aliases=['subscriptions', 'subscribed'],  brief='unleahes the subreddit to the channel', help='e.g.To unleash r/jokes `.unleash jokes`')
  async def subscription(self, context):
    # get metadata of subscribed news
    news_db = db('news')
    channel_id = str(context.channel.id)
    channel_news_data = news_db.get_one(channel_id)
    
    # embed=get_embeded_message(context, 'subscription: `news:`\t', f'**subscriptions:** {subscriptions}\n **country:**{country}\n **time_peroid**: 6 hours')
    embed=get_embeded_message(context, f'subscription_data: {channel_news_data}')
    await context.send(embed=embed)
  
async def setup(bot):
    await bot.add_cog(News(bot))

# ----------------------- #
      # archives #
# ----------------------- #
'''
how_many = db['subscription'][str(context.channel.id)]['how_many']
db['subscription'][str(context.channel.id)]['how_many']=0


'''