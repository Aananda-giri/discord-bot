import discord, datetime
from quiz_db.quiz_scores import QuizScores
from quiz_db.quiz_questions import QuizQuestions

import random


def generate_response(question=None,
                      correct_answer=None,
                      is_correct=True,
                      current_score=None,
                      has_answered=False):
  if has_answered:
    reactions = [
        "You've already conquered this one!",
        "Whoa! Double trouble! You've already answered!",
        "Impressive memory! You got it right before!",
        "Nice déjà vu! You've answered this one already!",
    ]
    reaction = random.choice(reactions)
    message = f"{reaction} \n Your current score remains 20. 🔄"
  elif is_correct:
    reactions = [
        "Boom! Nailed the AI challenge!",
        "Holy neural networks! You're on a roll!",
        "Bingo! You've cracked the AI code!",
        "Great job, AI maestro! You got it right!",
        "Impressive! Your AI knowledge is next level!",
        "Fantastic! You're an AI genius in the making!",
        "Incredible! You're mastering AI like a pro!",
    ]
    reaction = random.choice(reactions)
    message = f"{reaction} Your new score is {current_score}. 🚀"
  else:
    reactions = [
        "Whoopsie daisy! The AI overlords remain mysterious!",
        "Oh snap! Don't worry, even AI experts stumble sometimes!",
        "Oopsie! The algorithms were tricky this time. Keep going!",
        "Nice try! The correct AI answer is {correct_answer}.",
        "Almost there! AI is a tough nut to crack, but you'll get it!",
        "No worries! AI is a labyrinth, and you're navigating it well!",
        "Oh no! The AI gremlins got you this time. Try again!",
    ]
    reaction = random.choice(reactions)
    message = f"{reaction} \n\n the correct answer to question: \"{question}\" \n is: \"{correct_answer}\" \n\n your current_score remains: {current_score}"
  return message


async def update_scores(question,
                        reaction=None,
                        user=None,
                        raw_reaction=False,
                        message=None,
                        payload=None):
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

  if raw_reaction:
    username = payload.member.global_name
    user = payload.member

    reaction_time = datetime.datetime.utcnow()

    emoji = payload.emoji
  else:
    # Get the username of the user who reacted
    username = user.display_name

    # question = questions[message.id]
    message = reaction.message

    # Get the time that the user reacted
    reaction_time = message.created_at.replace(tzinfo=None)

    # Get the emoji that the user reacted with
    emoji = reaction.emoji

  number_emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣']
  # print(
  #     f'\n\n ----- the emoji ------:\"{payload.emoji}\" \"{payload.emoji in number_emojis}\" \"{str(payload.emoji) in number_emojis}\" \"{number_emojis[question["answer_index"]]}\"'
  # )
  users_reacted = question['users_reacted'] + [username]
  correctly_answered_users = question['correctly_answered_users']
  if reaction_time < question[
      'expire_date_time'] or True:  # True means questions does not expire
    old_score = QuizScores.get_score(server_id=question['server_id'],
                                     user_name=username)
    if username not in question['users_reacted']:
      print('username not in users_reacted')

      print('time is ok')
      print(question['answer_index'])

      # add user to reacted users
      question['users_reacted'].append(username)

      if old_score == None:
        old_score = 0

      if str(emoji) == number_emojis[question['answer_index']]:
        # correct answer
        print('\n\ncorrect answer')
        # get scores
        if len(question['correctly_answered_users']) < 1:
          # first correct answer get three points
          print('first correct')
          new_score = old_score + 3
        else:
          # elif len(question['correctly_answered_users']) == 1:
          # Everyone else with correct answer gets 2 points
          new_score = old_score + 2
          print('two points')
        # elif len(question['correctly_answered_users']) == 2:
        #     new_score = old_score + 5
        # else:
        #     new_score = old_score + 2   # give 2 points for every correct answer after the first 3
        print(f'\n user:{username} \n new_score:{new_score}')
        # # add user to scores if not already there
        # if username not in scores[server_id]:
        #     scores[server_id][username] = {'score':0}

        # update score of user in db
        # scores[server_id][username]['score'] += 1
        QuizScores.update_scores(server_id=question['server_id'],
                                 user_name=username,
                                 new_score=new_score)
        await user.send(
            generate_response(is_correct=True, current_score=new_score))
        # await user.send(f"Correct answer! yout new score is {new_score}")
        # update correctly_answered_users
        correctly_answered_users += [username]
      else:
        # wrong answer
        try:
          await user.send(
              generate_response(
                  is_correct=False,
                  current_score=old_score,
                  question=question['question'],
                  correct_answer=question['options'][question['answer_index']])
          )
          # await user.send(
          #     f"Sorry! the correct answer to question: \"{question['question']}\" \n is: \"{question['options'][question['answer_index']]}\" \n\n your current_score is: {old_score}"
          # )
        except Exception as e:
          print(e)
      # update question in db
      QuizQuestions.update_question(
          question['question_id'],
          correctly_answered_users=correctly_answered_users,
          users_reacted=users_reacted)
    else:
      # user have already voted
      await user.send(generate_response(has_answered=True, current_score=10))
      # await user.send(
      #     f"You have already voted for question: \"{question['question']}\" \n correct_answer: \"{question['options'][question['answer_index']]}\" \n\n your current_score is: {old_score}"
      # )
    QuizQuestions.update_question(
        question['question_id'],
        correctly_answered_users=correctly_answered_users,
        users_reacted=users_reacted)

  else:
    # Question Expired
    print(
        '\n ---------------------- \n question expired \n -----------------------'
    )

    # send quiz question expired message
    await user.send(
        f"sorry! the quiz question has expired. \n\n question: {question['question']} \n\n correct_answer: {question['options'][question['answer_index']]}"
    )

    # deactivate question
    QuizQuestions.deactivate_question(question['question_id'])

    # update leaderboard message
    leaderboard_data = QuizScores.get_top_ten(server_id=question['server_id'])

    return {
        'leaderboard_data': leaderboard_data,
        'question_expired': True
    }  # top 10

  leaderboard_data = QuizScores.get_top_ten(server_id=question['server_id'],
                                            how_many=15)
  print(
      f'\n\n -------------- server_id: {question["server_id"]} \n leaderboard_data:{leaderboard_data}  -------------- \n\n'
  )
  return {
      'leaderboard_data': leaderboard_data,
      'question_expired': False
  }  # top 10


def get_question_embed(context,
                       question_text,
                       options,
                       question_expired=False,
                       answer_index=None):
  # print(type(options))
  numbers = [
      ':one:', ':two:', ':three:', ':four:', ':five:', ':six:', ':seven:',
      ':eight:', ':nine:', ':keycap_ten:'
  ]

  if question_expired:
    embed = discord.Embed(title=f"{question_text}",
                          color=discord.Color.yellow())
    numbers[answer_index - 1] = ':white_check_mark:'
  else:
    embed = discord.Embed(title=f"{question_text}",
                          color=discord.Color.green())

  for index, option in enumerate(list(options)):
    embed.add_field(name=f"{numbers[index]} {option}", value=f"", inline=False)
  return embed


def create_stylish_leaderboard_embed(leaderboard_data,
                                     question_expired=False,
                                     is_most_active_leaderboard=False):
  # Create a new Discord embed
  if not is_most_active_leaderboard:
    if question_expired == True:
      embed = discord.Embed(title="Quiz Expired", color=discord.Color.yellow())
    else:
      embed = discord.Embed(title="Top 10 Leaderboard",
                            color=discord.Color.green())
  else:
    embed = discord.Embed(title="Most Active Members This Week!",
                          color=discord.Color.green())

  # Create the leaderboard text
  leaderboard_text = ""
  for rank, data in enumerate(leaderboard_data, start=1):
    # Destructure data tuple for readability
    if not is_most_active_leaderboard:
      username, score = data[1], data[2]
    else:
      username, score = data[0], data[1]

    # Decide the color and the emoji for the rank
    if rank == 1:
      rank_color = ":first_place:"
    elif rank == 2:
      rank_color = ":second_place:"
    elif rank == 3:
      rank_color = ":third_place:"
    else:
      rank_color = ""

    # Align the text
    if not rank in [1, 2, 3]:
      rank_str = f"`{str(rank).rjust(2)}`"
    else:
      rank_str = f"{rank_color} "
    user_str = f"**`{username.ljust(25)[:25]}`**"
    score_str = f"`{str(score).rjust(5)}`"

    # Combine the parts and append to the full leaderboard text
    leaderboard_text += f"{rank_str} {user_str} {score_str}\n"

    # Add a blank line after the top 3 for visual separation
    if rank == 3:
      leaderboard_text += "\n"

  # Add a field to the embed with the leaderboard text
  embed.add_field(
      name='Rank     User                                           Score',
      value=leaderboard_text,
      inline=False  # Set to False for better readability
  )
  return embed
