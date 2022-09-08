import sqlite3

import classes


class dataBase:
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
        self.table = """CREATE TABLE IF NOT EXISTS IMPRESSORAS (
                    person_id INTEGER PRIMARY KEY,
                    nomeFabricante VARCHAR(255) NOT NULL,
                    OIDFabricante VARCHAR(255),
                    nomeModelo VARCHAR(255),
                    modelo VARCHAR(255),
                    numeroDeSerie VARCHAR(255),
                    totalGeral VARCHAR(255),
                    totalCopiasCor VARCHAR(255),
                    totalCopiasMono VARCHAR(255),
                    totalCopias VARCHAR(255),
                    totalImpressaoCor VARCHAR(255),
                    totalImpressaoMono VARCHAR(255),
                    totalImpressao VARCHAR(255),
                    totalFax VARCHAR(255),
                    totalScanCor VARCHAR(255),
                    totalScanMono VARCHAR(255),
                    totalScan VARCHAR(255)                    
                ); """
        self.cursor.execute(self.table)


    # def createTable(self):
    #     self.cursor.execute(self.table)

    def inserirTabela(self,item):
        # self.conn()
        item = tuple(item.split(','))
        # x = f'''INSERT INTO IMPRESSORAS VALUES {item}'''
        x = f'''INSERT INTO IMPRESSORAS(
        nomeFabricante,OIDFabricante,nomeModelo,modelo,numeroDeSerie,totalGeral,totalCopiasCor,totalCopiasMono,totalCopias,
        totalImpressaoCor,totalImpressaoMono,totalImpressao,totalFax,totalScanCor,totalScanMono,totalScan
        ) VALUES {item}'''
        self.cursor.execute(x)
        self.commit()
        # self.close()

    def select(self):
        data = self.cursor.execute('''SELECT * FROM IMPRESSORAS''')
        listaDados = []
        for row in data:
            listaDados.append(row)
        return listaDados
    def selectTotalGeral(self):
        data = self.cursor.execute('''SELECT totalGeral FROM IMPRESSORAS''')
        listaDados = []
        for row in data:
            row = tuple([classes.unobscure(str(row)).decode()])
            listaDados.append(row)
        return listaDados

    def selectEspecific(self, atributo):
        data = self.cursor.execute(f'SELECT {atributo} FROM IMPRESSORAS')
        listaDados = []
        for row in data:
            listaDados.append(row)
        return listaDados

    def selectEspecificWhere(self, atributo, coluna):
        coluna = classes.obscure(str.encode(coluna)).decode()
        execut = f'SELECT * FROM IMPRESSORAS WHERE "{atributo}" = "{coluna}"'
        data = self.cursor.execute(execut)
        listaDados = []
        for row in data:
            row = list(row)
            for i in range (1,17):
                row[i] = classes.unobscure(row[i]).decode().upper()
            # row = tuple([classes.unobscure(str(row)).decode()])
            listaDados.append(row)
        return listaDados

    def delete(self,id):
        data = self.cursor.execute(f"DELETE from IMPRESSORAS where person_id={id}")
        self.commit()


