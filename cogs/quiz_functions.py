import discord
from quiz_db.quiz_scores import QuizScores
from quiz_db.quiz_questions import QuizQuestions
def update_scores(question, reaction, user):
    '''
    - check:
        - has not already reacted
        - reacted within the time limit
        - reacted to the correct answer
        
        
    - update scores
    - sort scores on server = server[server_id] by scores
    - return top 10
    '''

    # emoji, reaction_time, username, server_id, message
    '''
    {'server_id': 863298114491514891,
        'channel_id': 1163003138018639973,
        'question_id': 1163569335328055296,
        'question': 'test',
        'options': ['a', 'b', 'c', 'd'],
        'answer_index': 1,
        'leaderboard_message_id': 1163569353153843200,
        'created_datetime': '2023-10-16 20:09:07',
        'expire_date_time': '2023-10-16 23:09:07',
        'users_reacted': [],
        'correctly_answered_users': [],
        'active': 1}
    '''
    # question = questions[message.id]
    message = reaction.message

    # Get the username of the user who reacted
    username = user.display_name

    # Get the time that the user reacted
    reaction_time = reaction.message.created_at.replace(tzinfo=None)

    # Get the emoji that the user reacted with
    emoji = reaction.emoji

    number_emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣']
    users_reacted = question['users_reacted'] + [username]
    correctly_answered_users = question['correctly_answered_users']
    
    if username not in question['users_reacted']:
        print('username not in users_reacted')
        if reaction_time < question['expire_date_time']:
            print('\n\nvalid reaction time')
            print(question['answer_index'])
            if emoji == number_emojis[question['answer_index']]:
                print('\n\ncorrect answer')    
                
                # add user to reacted users
                question['users_reacted'].append(username)
                
                old_score = QuizScores.get_score(server_id = question['server_id'], user_name=username)
                
                if old_score == None:
                    old_score = 0
                # get scores
                if len(question['correctly_answered_users']) == 0:
                    new_score = old_score +  15
                elif len(question['correctly_answered_users']) == 1:
                    new_score = old_score +  10
                elif len(question['correctly_answered_users']) == 2:
                    new_score = old_score + 5
                else:
                    new_score = old_score + 2   # give 2 points for every correct answer after the first 3
                
                
                print(f'\nscore:{new_score}')
                # # add user to scores if not already there
                # if username not in scores[server_id]:
                #     scores[server_id][username] = {'score':0}
                
                # update score of user in db
                # scores[server_id][username]['score'] += 1
                QuizScores.update_scores(server_id = question['server_id'], user_name=username, new_score = new_score)
                
                # update correctly_answered_users
                correctly_answered_users += [username]

                # update question in db
                QuizQuestions.update_question(question['question_id'], correctly_answered_users=correctly_answered_users, users_reacted=users_reacted)
                
                # sorted scores
                # sorted_scores = sorted(scores[server_id].items(), key=lambda x: x[1]['score'], reverse=True)

                # print(f'\n\n sorted_scores: {sorted_scores} \n\n')
        # update reacted users
        
        QuizQuestions.update_question(question['question_id'], correctly_answered_users=correctly_answered_users, users_reacted=users_reacted)
    return QuizScores.get_top_ten(server_id=question['server_id'])   # top 10


def get_question_embed(context, question, options):
    # print(type(options))
    embed = discord.Embed(
        title=f"{question}",
        color=discord.Color.green()
    )
    numbers = [':one:', ':two:', ':three:', ':four:', ':five:', ':six:', ':seven:', ':eight:', ':nine:', ':keycap_ten:']
    
    for index, option in enumerate(list(options)):
        embed.add_field(
            name=f"{numbers[index]} {option}",
            value=f"",
            inline=False
        )
    return embed


def create_stylish_leaderboard_embed(leaderboard_data):
    # Create a new Discord embed
    embed = discord.Embed(
        title="Top 10 Leaderboard",
        color=discord.Color.green()
    )

    # Create the leaderboard text
    leaderboard_text = ""
    for rank, data in enumerate(leaderboard_data):
        username = data[1]
        score = data[2]
        leaderboard_text += f"`{str(rank+1).rjust(4)}`      `{username.center(10)}`      `{str(score).center(5)}`\n\n"

        # print(leaderboard_text)
    # Add a field to the embed with the leaderboard text
    embed.add_field(
        name='Rank          User            Score',
        value=leaderboard_text,
        inline=True
    )
    return embed
