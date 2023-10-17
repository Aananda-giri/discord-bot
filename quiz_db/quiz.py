from .quiz_questions import QuizQuestions
from .quiz_scores import QuizScores
from datetime import datetime

# Define the Quiz class that inherits from both QuizQuestions and QuizDatabase
class Quiz(QuizQuestions, QuizScores):
    def __init__(self, database_path="database_sqlite.db", *args, **kwargs):
        super().__init__(database_path, *args, **kwargs)
    
    @staticmethod
    def test1():
        # Usage example with dummy data
        Quiz.create_questions_table()

        # Add a question
        question_data = {
            'server_id': 1,
            'channel_id': 2,
            'question_id': 3,
            'question': 'What is 2 + 2?',
            'options': ['3', '4', '5'],
            'answer_index': 1,
            'leaderboard_question_id': 4,
            'created_datetime': datetime.now(),
            'expire_date_time': datetime.now(),
            'users_reacted': [1, 2, 3],
            'correctly_answered_users': [1, 2],
            'active': 1
        }

        Quiz.add_question(**question_data)

        # Get a question
        question_id = 3
        retrieved_question = Quiz.get_question(question_id)
        if retrieved_question:
            print("Retrieved Question:", retrieved_question)
        else:
            print("Question not found.")

        # Update a question
        new_question = "What is 3 + 3?"
        new_options = ['6', '7', '8']
        new_answer = 0

        Quiz.update_question(question_id, new_question, new_options, new_answer)

        # Usage example
        Quiz.create_score_table()
        Quiz.update_scores(server_id=123, user_id=456, new_score=100)
        score = Quiz.get_score(server_id=123, user_id=456)


        print(f'score: {score}')

        Quiz.exists(server_id=123, user_id=456, check_server_only=True)
    @staticmethod
    def test2():
         # Usage example
        Quiz.create_score_table()
        Quiz.update_scores(server_id=123, user_id=456, new_score=100)
        score = Quiz.get_score(server_id=123, user_id=456)


        print(f'score: {score}')

        Quiz.exists(server_id=123, user_id=456, check_server_only=True)

if __name__ == '__main__':
    # QuizQuestions.create_questions_table()
    # QuizScores.create_score_table()
    quiz = Quiz()
    quiz.test1()
    quiz.test2()