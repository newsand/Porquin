import sqlite3


class Filebase:
    """
    File storage Class for sqlite3
    :params conn — sqlite3Connection
    :params curr — cursor
    """

    def __init__(self):
        try:
            self.conn = sqlite3.connect("test.db")
            print("Successfully Opened User")
            self.curr = self.conn.cursor()
        except:
            print("Failed")

    def createTable(self):
        '''
        Method for Creating Table in Files
        '''
        create_table = '''
        CREATE TABLE IF NOT EXISTS files    (
        id          INTEGER  PRIMARY KEY AUTOINCREMENT,
        owner       INTEGER,
        filename    TEXT NOT NULL,
        file        BLOB NOT NULL,
        
        FOREIGN KEY(owner) REFERENCES cred(id)
        );
        '''
        self.curr.execute(create_table)
        names_index = "CREATE INDEX IF NOT EXISTS idx_owner ON files (owner);"
        self.curr.execute(names_index)
        self.conn.commit()

    def insertFile(self, data):
        '''
        Method for Insertig Data in Table in Files
        '''
        insert_data = """
        INSERT INTO files(owner, filename, file)
        VALUES(?, ?, ?);
        """
        self.curr.execute(insert_data, data)
        self.conn.commit()

    def search_files_from_user(self, data):
        '''
        Method for Searching Data in Table Files
        '''
        search_data = '''
        SELECT * FROM files WHERE owner = (?);
        '''
        self.curr.execute(search_data, data)
        rows = self.curr.fetchall()
        return rows

    def search_file(self, data):
        '''
        Method for Searching Data in Table  Files
        '''
        search_data = '''
        SELECT * FROM files WHERE owner = (?) and id  = (?);
        '''
        self.curr.execute(search_data, data)
        rows = self.curr.fetchall()
        return rows

    def delete_files(self, data):
        '''
        Method for Delete Data in Table Files
        '''
        query = "DELETE FROM files WHERE id IN ({})".format(", ".join("?" * len(data)))
        self.curr.execute(query, tuple(data))
        self.conn.commit()
        return

    def finish(self):
        try:
            self.conn.close()
            print("Successfully CLosed ")
        except:
            print("not closed")