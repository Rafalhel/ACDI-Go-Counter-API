import sqlite3

class dataBaseGeral:
    def __init__(self):
        self.sqliteConnection = sqlite3.connect('impressoraDB.db', check_same_thread=False)
        self.cursor = self.sqliteConnection.cursor()
        self.createTable()

    def close(self):
        """close sqlite3 connection"""
        self.sqliteConnection.close()

    def execute(self, new_data):
        """execute a row of data to current cursor"""
        self.cursor.execute(new_data)

    def commit(self):
        """commit changes to database"""
        self.sqliteConnection.commit()

    def createTable(self):
        self.table = """CREATE TABLE IF NOT EXISTS OIDGERAL (
                    totalGeral VARCHAR(255) NOT NULL                            
                ); """
        self.cursor.execute(self.table)


    # def createTable(self):
    #     self.cursor.execute(self.table)

    def inserirTabela(self,item):
        x = f'''INSERT INTO OIDGERAL VALUES ('{item}')'''
        self.cursor.execute(x)
        self.commit()
        # self.close()

    def select(self):
        data = self.cursor.execute('''SELECT * FROM OIDGERAL''')
        listaDados = []
        for row in data:
            listaDados.append(row)
        return listaDados
    def selectTotalGeral(self):
        data = self.cursor.execute('''SELECT totalGeral FROM OIDGERAL''')
        listaDados = []
        for row in data:
            listaDados.append(row)
        return listaDados

    def selectEspecific(self, atributo):
        data = self.cursor.execute(f'SELECT {atributo} FROM OIDGERAL')
        listaDados = []
        for row in data:
            listaDados.append(row)
        return listaDados

    def selectEspecificWhere(self, atributo, coluna):
        execut = f'SELECT totalGeral FROM OIDGERAL WHERE {atributo} = "{coluna}"'
        data = self.cursor.execute(execut)
        listaDados = []
        for row in data:
            listaDados.append(row)
        return listaDados

    def delete(self,id):
        data = self.cursor.execute(f"DELETE from OIDGERAL where person_id={id}")
        self.commit()


