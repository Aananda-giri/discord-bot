from discord.ext import commands


from database import SocialDb
import instaloader
from .functions import get_embeded_message


class SocialMedia:

  def __init__(self, url):
    self.url = url

  def __str__(self):
    return self.url

  @staticmethod
  def get_username(url):
    if url.startswith('https://www.instagram.com/'):
      username = url.split('/')[-2]
      return username, 'instagram'
    else:
      return None, None
    # elif url.startswith('https://www.linkedin.com/'):
    #     username = url.split('/')[-2]
    #     return username, 'linkedin'

  @staticmethod
  def subscribe(channel_id, user_id, url):
    print(f'channel_id: {channel_id}, user_id:{user_id}, url:{url}')
    social_username, platform = SocialMedia.get_username(url)
    print(f'social_username: {social_username}, platform:{platform}')
    if social_username and platform:
      db = SocialDb(table_name=platform)

      if db.exists(str(channel_id), social_username):
        # get posts
        posts = db.get_posts(channel_id,
                             social_username)  # list of posts or empty list
      else:
        posts = []
      print(f'old_posts : {posts}')
      new_posts = SocialMedia.get_new_posts(social_username, channel_id, posts,
                                            db)  # list of posts or empty list
      print(f'\n new_posts: {new_posts}')

      # Save in database if it doesn't exist
      posts.extend(new_posts)
      db.add(channel_id, social_username, url, platform, posts)

      return 'subscribed to ' + platform + ' user: \`' + social_username + '\`'
    else:
      return 'invalid url'

  @staticmethod
  def get_new_posts(username, channel_id, old_posts, db=None):
    if not db:
      db = SocialDb(table_name=platform)

    # Create an Instaloader object
    L = instaloader.Instaloader()

    # Load the profile of the user you want to get the latest post from
    profile = instaloader.Profile.from_username(L.context, username)

    # Get the posts from the profile
    posts = profile.get_posts()
    new_posts = []

    try:
      # Print the caption of the latest post
      next_post = next(posts)
    except StopIteration:
      pass

    post_url = "https://www.instagram.com/p/" + next_post.shortcode
    while post_url not in old_posts:
      new_posts.append(post_url)

      try:
        # Print the caption of the latest post
        next_post = next(posts)
      except StopIteration:
        break

      post_url = "https://www.instagram.com/p/" + next_post.shortcode
      print(f'next_post: {post_url}')

      # post_text = next_post.caption
      # print(post_text)

    return new_posts

  @staticmethod
  def unleash(url):
    # Save in database if it doesn't exist
    # values: username, platform, channel_id, user_id, posts
    return 'subscribed'


class Social(commands.Cog, name="social"):

  def __init__(self, bot):
    self.bot = bot

  @commands.hybrid_command(name='subscribe',
                          description='subscribe to insta or linkedin user')
  async def subscribe(self, ctx, url):
    # await ctx.send(embed= get_embeded_message(ctx, 'ping-pong', f'this is body, what:{what}', author=False))
    # show typing status
    print(f'\n\nsubscribe: {url}\n\n')
    async with ctx.channel.typing():

      
      response = SocialMedia.subscribe(channel_id=ctx.channel.id,
                                       user_id=ctx.author.id,
                                       url=url)
      print(str(response))
      await ctx.channel.send(embed=get_embeded_message(
          ctx, 'Subscription:', str(response), author=True))
      # await ctx.send(embed = get_embeded_message(ctx, , response, author=False)
      # if url.startswith('https://www.instagram.com/'):
      #   username = url.split('/')[-2]

      #   await ctx.send(f'You have subscribed to insta {url} \n user:{username}')
      # elif url.startswith('https://www.linkedin.com/'):

      #     await ctx.send(f'You have subscribed to linkedin {url}')

  @commands.hybrid_command(name='unsubscribe',
                          description='unsubscribe to insta or linkedin user')
  async def unsubscribe(self, ctx, url):
    # await ctx.send(embed= get_embeded_message(ctx, 'ping-pong', f'this is body, what:{what}', author=False))
    SocialMedia.subscribe(user_id=ctx.author.id,
                          channel_id=ctx.channel.id,
                          url=url)
    if url.startswith('https://www.instagram.com/'):
      username = url.split('/')[-2]

      await ctx.send(f'You have subscribed to insta {url} \n user:{username}')
    elif url.startswith('https://www.linkedin.com/'):

      await ctx.send(f'You have subscribed to linkedin {url}')


async def setup(bot):
  await bot.add_cog(Social(bot))
