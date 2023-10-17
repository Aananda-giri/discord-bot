import sqlite3
from datetime import datetime
import json, os

current_file_path = os.path.abspath(__file__)
parent_dir = os.path.dirname(current_file_path)

class QuizQuestions:
    def __init__(self, database_path, table_name='quiz_questions'):
        self.table_name = table_name

    @staticmethod
    def create_questions_table(table_name='quiz_questions', force=False):
        conn = sqlite3.connect(os.path.join(parent_dir,'quiz_sqlite_db.db'))
        c = conn.cursor()
        if force:
            c.execute(f"DROP TABLE IF EXISTS {table_name}")
        c.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (
            server_id INTEGER NOT NULL,
            channel_id INTEGER NOT NULL,
            question_id INTEGER NOT NULL,
            question TEXT NOT NULL,
            options TEXT NOT NULL,
            answer_index INTEGER NOT NULL,
            leaderboard_message_id INTEGER NOT NULL,
            created_datetime TEXT NOT NULL,
            expire_date_time TEXT NOT NULL,
            users_reacted TEXT NOT NULL,
            correctly_answered_users TEXT NOT NULL,
            active INTEGER NOT NULL
        )""")

        conn.commit()
        conn.close()

    @staticmethod
    def add_question(server_id, channel_id, question_id, question, options, answer_index, leaderboard_message_id, created_datetime, expire_date_time, users_reacted, correctly_answered_users, active):
        
            print('adding question')
            conn = sqlite3.connect(os.path.join(parent_dir,'quiz_sqlite_db.db'))
            c = conn.cursor()

            # Convert the datetime to a string in ISO 8601 format
            created_datetime = created_datetime.strftime('%Y-%m-%dT%H:%M:%S')
            expire_date_time = expire_date_time.strftime('%Y-%m-%dT%H:%M:%S')

            # Serialize the lists to JSON strings
            options = json.dumps(options)
            users_reacted = json.dumps(users_reacted)
            correctly_answered_users = json.dumps(correctly_answered_users)

            c.execute(f"""INSERT INTO quiz_questions (
                server_id, channel_id, question_id, question, options, answer_index, leaderboard_message_id,
                created_datetime, expire_date_time, users_reacted, correctly_answered_users, active
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (
                server_id, channel_id, question_id, question, options, answer_index,
                leaderboard_message_id, created_datetime, expire_date_time,
                users_reacted, correctly_answered_users, active
            ))

            conn.commit()
            conn.close()

            print(QuizQuestions.get_question(question_id))

    @staticmethod
    def get_question(question_id=None):
            conn = sqlite3.connect(os.path.join(parent_dir,'quiz_sqlite_db.db'))
            c = conn.cursor()

            if question_id:
                c.execute("SELECT * FROM quiz_questions WHERE question_id = ?", (question_id,))
            
                result = c.fetchone()

                conn.close()
                # print(result[8])
                if result:
                    # result = list(result)
                    keys = ['server_id', 'channel_id', 'question_id', 'question', 'options', 'answer_index', 'leaderboard_message_id', 'created_datetime', 'expire_date_time', 'users_reacted', 'correctly_answered_users', 'active']
                    result = dict(zip(keys, result))
                    print(result)
                    # Convert the string back to a datetime object
                    print(f"\n\ndate{result['created_datetime']}\n\n")
                    result['created_datetime'] = datetime.strptime(result['created_datetime'], '%Y-%m-%dT%H:%M:%S')
                    result['expire_date_time'] = datetime.strptime(result['expire_date_time'], '%Y-%m-%dT%H:%M:%S')
                    
                    # Convert JSON strings back to lists
                    result['options'] = json.loads(result['options'])
                    result['users_reacted'] = json.loads(result['users_reacted'])
                    result['correctly_answered_users'] = json.loads(result['correctly_answered_users'])
                    
                    # result[5] = json.loads(result[4])  # options
                    # result[8] = json.loads(result[9])  # users_reacted
                    # result[9] = json.loads(result[10])  # correctly_answered_users
                    return result
            else:
                c.execute("SELECT * FROM quiz_questions")
                results = c.fetchall()
                conn.close()
                return results
        
    @staticmethod
    def update_question(question_id, correctly_answered_users, users_reacted):
        conn = sqlite3.connect(os.path.join(parent_dir,'quiz_sqlite_db.db'))
        c = conn.cursor()

        # Convert lists to JSON strings
        users_reacted = json.dumps(users_reacted)
        correctly_answered_users = json.dumps(correctly_answered_users)

        c.execute("UPDATE quiz_questions SET correctly_answered_users = ?, users_reacted = ? WHERE question_id = ?", (
            correctly_answered_users, users_reacted, question_id
        ))

        conn.commit()
        conn.close()
        print(QuizQuestions.get_question(question_id))


if __name__ == "__main__":
    # Usage example with dummy data
    QuizQuestions.create_questions_table()

    # Add a question
    question_data = {
        'server_id': 1,
        'channel_id': 2,
        'question_id': 3,
        'question': 'What is 2 + 2?',
        'options': ['3', '4', '5'],
        'answer_index': 1,
        'leaderboard_message_id': 4,
        'created_datetime': datetime.now(),
        'expire_date_time': datetime.now(),
        'users_reacted': [1, 2, 3],
        'correctly_answered_users': [1, 2],
        'active': 1
    }

    QuizQuestions.add_question(**question_data)

    # Get a question
    question_id = 3
    retrieved_question = QuizQuestions.get_question(question_id)
    if retrieved_question:
        print("Retrieved Question:", retrieved_question)
    else:
        print("Question not found.")

    # Update a question
    new_question = "What is 3 + 3?"
    new_options = ['6', '7', '8']
    new_answer = 0

    QuizQuestions.update_question(question_id, new_question, new_options, new_answer)
