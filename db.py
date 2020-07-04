import sqlite3

conn = sqlite3.connect('instagram.db')

c = conn.cursor()

c.execute("""
            CREATE TABLE IF NOT EXISTS Profiles (
                user text,
                username text,
                liked_href text,
                search text
            );
           """)

c.execute("""
            CREATE TABLE IF NOT EXISTS Following (
                username text,
                link text,
                datetime text
            );
           """)

# c.execute("INSERT INTO Profiles VALUES('test','testlink','sdf')")

c.execute("ALTER TABLE Profiles add user text")
# c.execute("INSERT INTO Profiles VALUES('{}','{}','{}')".format('k','k','k'))
# c.execute("SELECT * FROM Profiles")




print(c.fetchall())

conn.commit()

conn.close()
