import time
from instabot import Bot
bot = Bot()
bot.login(username=INSTA_USERNAME, password=INSTA_PASSWORD)
print('sleeping 15s')
time.sleep(15)
######  upload a picture #######
bot.upload_photo("index.jpeg", caption="biscuit eating baby")

# ######  follow someone #######
# bot.follow("elonrmuskk")

# ######  send a message #######
# bot.send_message("Hello from Dhaval", ['user1','user2'])

# ######  get follower info #######
# my_followers = bot.get_user_followers("dhavalsays")
# for follower in my_followers:
#     print(follower)

# # Unfollow everyone
# bot.unfollow_everyone()
