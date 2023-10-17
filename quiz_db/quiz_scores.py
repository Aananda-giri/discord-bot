import sqlite3
import os

current_file_path = os.path.abspath(__file__)
parent_dir = os.path.dirname(current_file_path)

class QuizScores:
    def __init__(self, database_path, table_name='quiz_scores'):
        self.database_path = database_path
        self.table_name = table_name

    @staticmethod
    def create_scores_table(table_name='quiz_scores', force=False):
        '''
        - Columns:
        - server_id | user_name | score |
        '''
        conn = sqlite3.connect(os.path.join(parent_dir,'quiz_sqlite_db.db'))
        c = conn.cursor()
        if force:
            c.execute(f"DROP TABLE IF EXISTS {table_name}")
        c.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (
            server_id INTEGER NOT NULL,
            user_name TEXT NOT NULL,
            score INTEGER NOT NULL
        )""")

        conn.commit()
        conn.close()
    
    def database_path(self):
        print(self.database_path)
    @staticmethod
    def add_score(server_id, user_name, score):
        conn = sqlite3.connect(os.path.join(parent_dir,'quiz_sqlite_db.db'))
        c = conn.cursor()
        c.execute(f"""INSERT INTO quiz_scores (
            server_id, user_name, score
        ) VALUES (?, ?, ?)""", (
            server_id, user_name, score
        ))

        conn.commit()
        conn.close()
    @staticmethod
    def get_score(server_id=None, user_name=None):
        conn = sqlite3.connect(os.path.join(parent_dir,'quiz_sqlite_db.db'))
        c = conn.cursor()

        if server_id == None or user_name == None:
            # return all records
            c.execute("SELECT * FROM quiz_scores")
            result = c.fetchall()
            return result
        c.execute("SELECT score FROM quiz_scores WHERE server_id = ? AND user_name = ?", (server_id, user_name))
        result = c.fetchone()

        conn.close()

        if result:
            return result[0]
        else:
            return None
    @staticmethod
    def get_top_ten(server_id):
        conn = sqlite3.connect(os.path.join(parent_dir,'quiz_sqlite_db.db'))
        c = conn.cursor()
        c.execute("SELECT * FROM quiz_scores WHERE server_id = ? ORDER BY score DESC LIMIT 10", (server_id,))
        result = c.fetchall()

        conn.close()

        if result:
            return result
        else:
            return None

    @staticmethod
    def exists(server_id, user_name, check_server_only=False):
        conn = sqlite3.connect(os.path.join(parent_dir,'quiz_sqlite_db.db'))
        c = conn.cursor()
        if check_server_only:
            c.execute("SELECT COUNT(*) FROM quiz_scores WHERE server_id = ?", (server_id,))
            result = c.fetchone()
            conn.close()
        else:

            c.execute("SELECT COUNT(*) FROM quiz_scores WHERE server_id = ? AND user_name = ?", (server_id, user_name))
            result = c.fetchone()

            conn.close()

        if result[0] > 0:
            return True
        else:
            return False

    @staticmethod
    def update_scores(server_id, user_name, new_score):
        conn = sqlite3.connect(os.path.join(parent_dir,'quiz_sqlite_db.db'))
        c = conn.cursor()

        if QuizScores.exists(server_id, user_name):
            c.execute("UPDATE quiz_scores SET score = ? WHERE server_id = ? AND user_name = ?", (new_score, server_id, user_name))
        else:
            c.execute("INSERT INTO quiz_scores (server_id, user_name, score) VALUES (?, ?, ?)", (server_id, user_name, new_score))

        conn.commit()
        conn.close()
        print(new_score)

if __name__ == "__main__":
    # Usage example
    QuizScores.create_score_table()
    QuizScores.update_scores(server_id=123, user_name=456, new_score=100)
    score = QuizScores.get_score(server_id=123, user_name=456)


    print(f'score: {score}')

    QuizScores.exists(server_id=123, user_name=456, check_server_only=True)
