# sqlite case_sensitive: capital letters only
import sqlite3


# open database
conn =sqlite3.connect('database.db')
c = conn.cursor()   # create a cursor

# Execute commands
c.execute("""CREATE TABLE '%s' (
  		channel_id int NOT NULL PRIMARY KEY

  		)"""% table_name)

# rename table
c.execute("ALTER TABLE table_name RENAME TO new_table_name")

# rename column
c.execute("ALTER TABLE table_name RENAME COLUMN current_name TO new_name")

# commit and close table
conn.commit() # commit our command
conn.close()  # close our connection