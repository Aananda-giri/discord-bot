# Table: quiz_questions

- Columns:
  server_id | Channel_id | message_id | question | options | answer_index | leaderboard_message_id | created_datetime | expire_date_time | reacted_users <list> | correctly_answered_users <list>

# Table: quiz_scores

- Columns:
  server_id | user_id | score |

- Note:
  - user have score related to server_id only

# Scores Example:

- Format: {server_id: { user_id: ['score': score]}}

```
scores = {
    863298114491514891: {'anon': {'score':6},
        'bnon': {'score':3},
        'cnon': {'score':6},
        'dnon': {'score':2},
        'enon': {'score':3},
        'fnon': {'score':2},}
}
server_id = 863298114491514891

# Sort by scores
sorted_scores = sorted(scores[server_id].items(), key=lambda x: x[1]['score'], reverse=True)
```

- result: [('anon', {'score': 6}), ('cnon', {'score': 6}), ('bnon', {'score': 3}), ('enon', {'score': 3}), ('dnon', {'score': 2}), ('fnon', {'score': 2})]

# Quiz Example:

- Format: {Channel_id: [{message_id, question, options, answer, leaderboard_message_id, created_datetime, expire_date_time, reacted_users, correctly_answered_users}]}

```
questions = {
    111: {
            'message_id': 123,
            'channle_id': 123456,
            'question': 'What is the capital of India?',
            'options':['Delhi', 'Mumbai', 'Kolkata', 'Chennai'],
            'answer':'1️⃣',
            'leaderboard_message_id': 12345,
            'created_datetime': "2023-10-16T21:12:32",
            'expire_date_time': '2023-10-16T22:12:32',    # Expires after 60 minutes
            'reacted_users': [],
            'correctly_answered_users':[]
        },
    112: {
            'message_id': 123,
            'channle_id': 123456,
            'question': 'What is the capital of India?',
            'options':['Delhi', 'Mumbai', 'Kolkata', 'Chennai'],
            'answer':'1️⃣',
            'leaderboard_message_id': 12345,
            'created_datetime': "2023-10-16T21:12:32",
            'expire_date_time': '2023-10-16T22:12:32',    # Expires after 60 minutes
            'reacted_users': [],
            'correctly_answered_users':[]
        }
}
```

# Storing datetime

```
from datetime import datetime

# Get the current datetime
current_datetime = datetime.now()

# Convert the datetime to a string in ISO 8601 format
datetime_str = current_datetime.strftime('%Y-%m-%dT%H:%M:%S')

# Now you can save `datetime_str` to your database

```

# loading datetime

```

from datetime import datetime

# Retrieve the datetime string from the database
datetime_str = '2023-10-16T15:30:00'  # Replace this with the value from your database

# Convert the string back to a datetime object
loaded_datetime = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S')

# Now, `loaded_datetime` is a datetime object that you can work with in your Python code

```
