import sqlite3
import json

class SocialDb:

  def __init__(self,
               table_name="instagram",
               database_name='database.db') -> None:
    self.table_name = table_name
    self.database_name = database_name

  def create(self):
    conn = sqlite3.connect(self.database_name)
    c = conn.cursor()
    c.execute(f"""CREATE TABLE IF NOT EXISTS {self.table_name} (
                      channel_id TEXT NOT NULL,
                      social_username TEXT NOT NULL,
                      social_url TEXT NOT NULL,
                      platform TEXT NOT NULL,
                      posts TEXT
                   )""")
    conn.commit()
    conn.close()

  def add(self, channel_id, social_username, social_url, platform, posts):
    # create table if not exists

    if type(posts) == list:
      posts = json.dumps(posts)
    if type(channel_id) == int:
      channel_id = str(channel_id)

    conn = sqlite3.connect(self.database_name)
    c = conn.cursor()
    # Check if channel_id already exists
    c.execute(
        f"SELECT * FROM {self.table_name} WHERE channel_id = ? AND social_username = ?",
        (channel_id, social_username))

    result = c.fetchone()
    if result:
      # Update posts existing entry
      c.execute(f"UPDATE {self.table_name} SET posts = ? WHERE channel_id = ?",
                (posts, channel_id))
    else:
      # Insert new entry
      c.execute(
          f"INSERT INTO {self.table_name} (channel_id, social_username, social_url, platform, posts) VALUES (?, ?, ?, ?, ?)",
          (channel_id, social_username, social_url, platform, posts))
    conn.commit()
    conn.close()

  def remove_one(self, channel_id, social_username):
    print(f'removing post: {social_username} from channel: {channel_id}')
    conn = sqlite3.connect(self.database_name)
    c = conn.cursor()
    c.execute(
        f"DELETE FROM {self.table_name} WHERE channel_id = ? AND social_username = ?",
        (channel_id, social_username))
    conn.commit()
    conn.close()

  def exists(self, channel_id, social_username):
    self.create()

    conn = sqlite3.connect(self.database_name)
    c = conn.cursor()
    # Check if channel_id already exists
    c.execute(
        f"SELECT * FROM {self.table_name} WHERE channel_id = ? AND social_username = ?",
        (channel_id, social_username))
    result = c.fetchone()
    return True if result else False

  def get_posts(self, channel_id, social_username):
    conn = sqlite3.connect(self.database_name)
    c = conn.cursor()
    c.execute(
        f"SELECT posts FROM {self.table_name} WHERE channel_id = ? AND social_username = ?",
        (channel_id, social_username))
    posts = c.fetchone()
    conn.close()
    return json.loads(posts[0]) if posts else []

  def get_all(self):
    self.create()
    conn = sqlite3.connect(self.database_name)
    c = conn.cursor()
    c.execute(f"SELECT * FROM {self.table_name}")
    result = c.fetchall()
    conn.close()

    result_ordered = []
    for res in result:
      result_ordered.append({
          'channel_id': res[0],
          'social_username': res[1],
          'social_url': res[2],
          'platform': res[3],
          'posts': json.loads(res[4])
      })
    return result_ordered




class db:
    def __init__(self, table_name):
        self.table_name = table_name
        # ---------------------------------------------------
        # Table_names: 'subreddit' or 'news'
        # - channel_id
        # - gener: table_name:subreddit -> subredit_name
        # - gener: table_name:news -> country_prefix
        # - how_many: no. of posts per time
        # ---------------------------------------------------

    @staticmethod
    def create_subscription_table(table_name='subreddit'):

        conn = sqlite3.connect('database.db')
        c = conn.cursor()   # create a cursor
        c.execute("""CREATE TABLE '%s' (
  		channel_id int NOT NULL,
      gener text NOT NULL,
      how_many int NOT_NULL
  		)""" % table_name)
        conn.commit()  # commit our command
        conn.close()  # close our connection
    # create_reddit_table()
    
  

    def add_one(self, channel_id, gener=None, how_many=None):
        print('\n\n add_one: table_name: {}\n\n'.format(self.table_name))
        if self.table_name == 'ioe_notifications' or self.table_name == 'vent' or self.table_name == 'gemini_chat':
          # 'ioe_notification and vent' tables have same structure
            self.add_one_ioe_notificaiton(channel_id)
        elif self.table_name == 'subreddit' or self.table_name == 'news':
            print(f'\n table_name: {self.table_name}\n')
            self.add_one_subscription(channel_id, gener, how_many)
            return 'added one subreddit'
        else:
            print(f'\n table_name: \'{self.table_name}\' not found\n')
    
    def remove_one(self, channel_id, gener=None):
        if self.table_name == 'ioe_notifications' or self.table_name == 'vent' or self.table_name == 'gemini_chat':
            self.remove_one_ioe_notificaiton(channel_id)
        elif self.table_name == 'subreddit' or self.table_name == 'news':
            # print(f'genre is {gener} channel id:{channel_id}')
            self.remove_one_subscription(channel_id, gener)
        elif self.table_name == 'vent':
            self.remove_one_vent_channel(channel_id)
        return

    def remove_many(self, channel_id, gener=None):
        if self.table_name == 'news':
            # list of countries given in gener
            for country in gener:
                self.remove_one_subscription(channel_id, country)

    def add_one_subscription(self, channel_id, gener, how_many):
        '''
          adds/updates one news/subreddit that matches channel_id and gener.
          gener = 'subreddit' or 'news'
        '''

        conn = sqlite3.connect(('database.db'))
        c = conn.cursor()   # create a cursor
        c.execute("SELECT * FROM '%s' WHERE channel_id = (?) AND gener = (?)" %
                  self.table_name, (channel_id, gener))
        existing_data = c.fetchall()
        print('existing_data:', existing_data)
        if existing_data == []:
            # adding new data
            message = f'adding new data: channel_id:{channel_id}, gener:{gener}, how_many:{how_many}'
            c.execute("INSERT INTO '%s' VALUES (?, ?, ?)" %
                      self.table_name, ((str(channel_id)), gener, str(how_many)))
        else:
            # updating existing data
            message = f'updating existing data: channel_id:{channel_id}, gener:{gener}, how_many:{how_many}'
            c.execute("""UPDATE '%s' SET gener = (?), how_many=(?) WHERE channel_id = (?)""" %
                      self.table_name, (gener, str(how_many), channel_id,))
        # data = c.fetchall()
        conn.commit()  # commit our command
        conn.close()  # close our connection
        return message

    # add_one_reddit(123,'sub', 3)

    def remove_one_subscription(self, channel_id, gener=None):
        '''
          removes one from 'subreddit'/'news' table that matches channel_id and gener.
          gener = 'subreddit_name' for table_name='subreddit', 'country_prefix' for table_name= news
        '''

        conn = sqlite3.connect('database.db')
        c = conn.cursor()   # create a cursor
        if gener == None:
            # print(f'genre is {gener} channel id:{channel_id}')
            c.execute("DELETE FROM '%s' WHERE channel_id = (?)" %
                    self.table_name, (channel_id, ))
        else:
            c.execute("DELETE FROM '%s' WHERE channel_id = (?) AND gener = (?) " %
                    self.table_name, (channel_id, gener,))
        message = f"Delete: channel_id: {channel_id}, {self.table_name}: {gener}"

        conn.commit()  # commit our command
        conn.close()  # close our connection
        return message

    def get_one(self, channe_id):
        '''
           - common function for 'ioe_notifications' and news/reddit
           - Returns list of channel_ids if table_name == 'ioe_notifications'
           - else Return dictionary of format:
          # subreddit:    {'channel_id':['subreddit_name', how_many]}
          # news:  {'channel_id':['country_prefix', how_many]}
        # for table_name='chain_word': return {'channel_id': int(123), 'current_word' : 'rick', 'current_author' : 'me', data['current_score'] int(3), 'highest_score'] : int(5)
        # for table_name='count': return {'channel_id': int(123), 'current_count' : 'rick', 'current_author' : 'me', 'current_score', int(3), 'highest_score' : int(5)
        # for table_name='ioe_notifications': return ['1232453', '3443432524', ...] # channe_id_list
        '''

        conn = sqlite3.connect('database.db')
        c = conn.cursor()   # create a cursor

        if self.table_name == 'count' or self.table_name == 'chain_word':
            c.execute("SELECT * FROM '%s' WHERE channel_id = (?)" %
                      self.table_name, (channe_id,))
            data = {}
            for tup in c.fetchall():
                data['channel_id'] = str(tup[0])
                if self.table_name == 'count':
                    data['current_count'] = tup[1]
                else:
                    data['current_word'] = tup[1]
                data['current_author'] = tup[2]
                data['current_score'] = int(tup[3])
                data['highest_score'] = int(tup[4])
        elif self.table_name == 'ioe_notifications' or self.table_name == 'vent' or self.table_name == 'gemini_chat':
            # print('inside_vent_db')
            c.execute("SELECT * from '%s' WHERE channel_id = (?)" %
                      self.table_name, (channe_id,))
            data = [tup[0] for tup in c.fetchall()]
            # print(data)

        elif self.table_name == 'news' or self.table_name == 'subreddit':
            # for table: 'news' and table: 'subreddit'
            c.execute("SELECT * FROM '%s' WHERE channel_id = (?)" %
                      self.table_name, (channe_id,))
            data = {}
            for tup in c.fetchall():
                data[str(tup[0])] = [tup[1], tup[2]]

        conn.commit()  # commit our command
        conn.close()  # close our connection
        return data
    
    def exists(self, channel_id):
        if self.get_one(channel_id) == {} or self.get_one(channel_id) == []:
            return False
        else:
            return True

    # remove_one_reddit(123, 'sub2')
    def get_all(self):
        '''
           - common function for 'ioe_notifications' and news/reddit
           - Returns list of channel_ids if table_name == 'ioe_notifications'
           - else Return dictionary of format:
                {'channel_id':['subreddit_name', how_many]}   # for subreddit
                {'channel_id':['country_prefix', how_many]}   # for news
        # for table_name='chain_word': return {'channel_id': int(123), 'current_word' : 'rick', 'current_author' : 'me', data['current_score'] int(3), 'highest_score'] : int(5)
        # for table_name='count': return {'channel_id': int(123), 'current_count' : 'rick', 'current_author' : 'me', 'current_score', int(3), 'highest_score' : int(5)
        # for table_name='ioe_notifications': return ['1232453', '3443432524', ...] # channe_id_list
        '''
        conn = sqlite3.connect('database.db')
        c = conn.cursor()   # create a cursor
        if self.table_name == 'ioe_notifications' or self.table_name == 'vent' or self.table_name == 'gemini_chat':
            # print('inside_vent_db')
            c.execute("SELECT channel_id FROM '%s'" % self.table_name)
            data = [tup[0] for tup in c.fetchall()]
            # print(data)
        elif self.table_name == 'count' or self.table_name == 'chain_word':
            c.execute("SELECT * FROM '%s'" % self.table_name)
            data = []
            for tup in c.fetchall():
                
                # print(f'tup is :{tup[:]}') 
                # tuple: (12, '12', '12', 12, 12)  --> (channel_id, current_word, current_author, current_score, highest_score)
                
                # data[str(tup[0])] = tup[1:]
                
                d = {}
                d['channel_id'] = str(tup[0])
                if self.table_name == 'count':
                    d['current_count'] = tup[1]
                else:
                    d['current_word'] = tup[1]
                d['current_author'] = tup[2]
                d['current_score'] = int(tup[3])
                d['highest_score'] = int(tup[4])

                data.append(d)




                # fields = ['channel_id', 'current_word', 'current_author', 'current_score', 'highest_score']
                # for position, field in enumerate(fields):
                #   data['field'] = tup[position]

        else:
            # for table: 'news' and table: 'subreddit'
            c.execute("SELECT * FROM '%s'" % self.table_name)
            data = {}
            # Note:
            # tup[0] -> channe_id
            # tup[1] -> country
            # tup[2] -> how_many
            # required format: {channel_id: {country1:how_many, country2:how_many}}
            for tup in c.fetchall():
                try:
                    # when channel_id already contains some data
                    data[str(tup[0])][tup[1]] = tup[2]
                except:
                    # initially when channel_id of dictionary is not defined
                    data[str(tup[0])] = {tup[1]: tup[2]}
        conn.commit()  # commit our command
        conn.close()  # close our connection
        return data

    # ---------------------
    # news_db
    # - channel_id
    # - countries and how_many

    # ---------------------
        # Table_name: ioe_notifications
        # - channel_id
    # ---------------------
    @staticmethod
    def create_ioe_notification_table(table_name='ioe_notifications'):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()   # create a cursor
        # Check if table exists

        c.execute("""CREATE TABLE IF NOT EXISTS '%s' (
          channel_id int NOT NULL PRIMARY KEY
          )""" % table_name
        )
        conn.commit()  # commit our command
        conn.close()  # close our connection
    # create_ioe_notification_table()

    def add_one_ioe_notificaiton(self, channel_id):
        '''
          Adds one ioe_notification: to channel : {channel_id}
          overrides other add_one function of news/reddit if 'channel_id' argument is provided
        '''
        conn = sqlite3.connect(('database.db'))
        c = conn.cursor()   # create a cursor

        c.execute("INSERT INTO '%s' VALUES (?)" %
                  self.table_name, ((str(channel_id)),))
        data = c.fetchall()

        conn.commit()  # commit our command
        conn.close()  # close our connection
        return data

    def remove_one_ioe_notificaiton(self, channel_id):
        '''
          Removes one ioe_notification: from channel : {channel_id}
          overrides other remove_one function of news/reddit if only 'channel_id' argument is provided

        '''
        conn = sqlite3.connect('database.db')
        c = conn.cursor()   # create a cursor

        c.execute("DELETE FROM '%s' WHERE channel_id = (?) " %
                  self.table_name, (channel_id,))
        message = f"Delete ioe_notifications: channel_id:{channel_id}"

        conn.commit()  # commit our command
        conn.close()  # close our connection
        return message

    # ----------------------------------------
    # count and chain_word have seperate table but served with same functions of word_chain
    # - channel_id       -> channel_id
    # - current_count    -> current_word
    # - current_counter -> current_author
    # - highest_score    -> highest_score
    # - current_score    -> current_score
    # - gener: numbers_count                 ->
    # ----------------------------------------
    @staticmethod
    def create_word_chain_table_db(table_name='word_chain'):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()   # create a cursor
        c.execute("""CREATE TABLE '%s' (
  		channel_id int NOT NULL PRIMARY KEY,
      current_word TEXT,
      current_author TEXT,
      current_score INT,
      highest_score INT
  		)""" % table_name)
        conn.commit()  # commit our command
        conn.close()  # close our connection
    # create_word_chain_table_db()

    def add_one_chain_word(self, channel_id, current_word, current_author, current_score, highest_score):
        '''
          Adds one add_one_chain_word: to channel : {channel_id}, current_word: {current_word}, current_author:{current_author}, current_score:{current_score}, highest_score:{current_score}
          
        '''
        conn = sqlite3.connect(('database.db'))
        c = conn.cursor()   # create a cursor
        c.execute("SELECT * FROM '%s' WHERE channel_id = (?)" %
                  self.table_name, (channel_id,))
        existing_data = c.fetchall()
        print('existing:', existing_data)
        if existing_data == []:
            # adding new data
            message = f'starting word_chain: channel_id:{channel_id}, current_author:{current_author}, current_word:{current_word}, curret_score:{current_score}, highest_score:{highest_score}'
            c.execute("INSERT INTO '%s' VALUES (?, ?, ?, ?, ?)" % self.table_name, ((
                str(channel_id)), current_word, current_author, current_score, highest_score))
        else:
            # updating existing data
            message = f'updating word_chain: channel_id:{channel_id}, current_author:{current_author}'
            c.execute("""UPDATE '%s' SET current_author = (?), current_word=(?), current_score=(?), highest_score = (?) WHERE channel_id = (?)""" %
                      self.table_name, (current_author, current_word, current_score, highest_score, channel_id))
        conn.commit()  # commit our command
        conn.close()  # close our connection
        return message

    def remove_one_chain_word(self, channel_id):
        '''
          Removes one channel from game channels i.e. from databases : 'count' and 'chain_word':
          overrides other remove_one function of news/reddit if only 'channel_id' argument is provided

        '''
        conn = sqlite3.connect('database.db')
        c = conn.cursor()   # create a cursor

        c.execute("DELETE FROM '%s' WHERE channel_id = (?) " %
                  self.table_name, (channel_id,))
        message = f"Delete word_chain: channel_id:{channel_id}"

        conn.commit()  # commit our command
        conn.close()  # close our connection
        return message
    
    @staticmethod
    def create_score_table(table_name='quiz_scores'):
        '''
            - Columns:
            - server_id | user_id | score |
        '''
        
        conn = sqlite3.connect('database.db')
        c = conn.cursor()   # create a cursor
        
        c.execute("""CREATE TABLE '%s' (
            server_id int NOT NULL,
            user_id int NOT NULL
            score int NOT NULL
  		)""" % table_name)
        
        conn.commit()  # commit our command
        conn.close()  # close our connection
    
    def get_score(server_id):
        # return server scores
        pass
    
    def exists(server_id, user_id, search_server_only=False):
        # does user exist in server
        # does server exists
        pass
    
    def update_scores(server_id, scores):
        pass
'''
def get_one():
  pass
def add_one(channel_id, subreddit, how_many):
  # channelid not in db
  message = 'status'
  return message
def remove(channel_id, subreddit):
  # subreddit unleashed -> remove subreddit
  # subreddit not unleashed -> skip, send not unleashed message
  pass

def get_subreddits(channel_id):
  # returns list of subreddits unleashed in channed
  pass

def get_countries(channel_id):
  # returns list of countries news unleashed in channel
  pass

songs_db:
- channel_id
- queue: user_to_add_to_queuq, song_name, song_url


def update_count(channel_id, new_counter=None, new_count=0, new_highest_score=False):
  # to update count of channel_id with new_count, new_counter, new_highest_socre
  pass

word_chain
def update_word(channel_id, new_word, new_author=None, current_score = 0, new_highest_score=False):
  # to update data of channel_id with: new_word, new_author, current_score, highest_score
  pass
'''


if __name__ == "__main__":
  # from database import db
  gemini_chat_db = db('gemini_chat')
  
  # Crreate table: gemini_chat
  gemini_chat_db.create_ioe_notification_table('gemini_chat')