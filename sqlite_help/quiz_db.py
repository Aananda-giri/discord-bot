import sqlite3

class QuizDatabase:
    def __init__(self, table_name):
        self.table_name = table_name

    @staticmethod
    def create_score_table(table_name='quiz_scores'):
        '''
        - Columns:
        - server_id | user_id | score |
        - one server has multiple users
        '''
        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        c.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (
            server_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            score INTEGER NOT NULL
        )""")

        conn.commit()
        conn.close()

    @staticmethod
    def get_score(server_id, user_id):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        c.execute("SELECT score FROM quiz_scores WHERE server_id = ? AND user_id = ?", (server_id, user_id))
        result = c.fetchone()

        conn.close()

        if result:
            return result[0]
        else:
            return None

    @staticmethod
    def exists(server_id, user_id, check_server_only=False):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        if check_server_only:
            c.execute("SELECT COUNT(*) FROM quiz_scores WHERE server_id = ?", (server_id,))
            result = c.fetchone()
            return result[0] > 0
        c.execute("SELECT COUNT(*) FROM quiz_scores WHERE server_id = ? AND user_id = ?", (server_id, user_id))
        result = c.fetchone()

        conn.close()

        if result[0] > 0:
            return True
        else:
            return False

    @staticmethod
    def update_scores(server_id, user_id, new_score):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        if Database.exists(server_id, user_id):
            c.execute("UPDATE quiz_scores SET score = ? WHERE server_id = ? AND user_id = ?", (new_score, server_id, user_id))
        else:
            c.execute("INSERT INTO quiz_scores (server_id, user_id, score) VALUES (?, ?, ?)", (server_id, user_id, new_score))

        conn.commit()
        conn.close()

# Usage example
Database.create_score_table()
Database.update_scores(server_id=123, user_id=456, score=100)
score = Database.get_score(server_id=123, user_id=456)
print(score)
