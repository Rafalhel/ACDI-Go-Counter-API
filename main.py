from flask import Flask, jsonify, request

import classes
from db import dataBase
from dbGeral import dataBaseGeral

oids = dataBase().select()
print(oids)
retornarJson = []
nomes = ['person_id','nomeFabricante','OIDFabricante','nomeModelo','modelo','numeroDeSerie','totalGeral','totalCopiasCor','totalCopiasMono','totalCopias',
        'totalImpressaoCor','totalImpressaoMono','totalImpressao','totalFax','totalScanCor','totalScanMono','totalScan']
reteste2 = dict(zip(nomes,oids[0]))
for i in oids:
    retornarJson.append(dict(zip(nomes,i)))

oidsGeral = dataBaseGeral().select()
print(oidsGeral)
retornarJsonGeral = []
nomeGeral = ['totalGeral']
novoGeral = dict(zip(nomeGeral,oidsGeral))
for i in oidsGeral:
    retornarJsonGeral.append(dict(zip(nomeGeral,i)))

app = Flask(__name__)

@app.route('/')
def home():
    return 'Home Page Route'

@app.route('/oid')
def oid():
    return jsonify(retornarJson)

@app.route('/oid', methods=['POST'])
def addOid():
    atributo = request.json
    inserir = []
    print(atributo)
    for i in atributo:
        inserir.append(classes.obscure(str.encode(atributo[i].upper())).decode())
        # print(atributo[i])
    inserir = ','.join(inserir)
    dataBase().inserirTabela(inserir)
    # oids = dataBase().select()
    # print(oids)
    # dataBase().inserirTabela(atributo)
    return jsonify({'message': 'oid adicionado com sucesso'})

@app.route('/RemoveOid', methods=['POST'])
def removeOid():
    atributo = request.json
    print(atributo)
    dataBase().delete(atributo['person_id'])
    return jsonify({'message': 'oid removido com sucesso'})

@app.route('/oidGeral')
def oidGeral():
    return jsonify(retornarJsonGeral)

@app.route('/oidGeral', methods=['POST'])
def addOidGeral():
    atributo = request.json
    inserir = []
    print(atributo)
    for i in atributo:
        inserir.append(atributo[i])
        # print(atributo[i])
    inserir = ','.join(inserir)
    dataBaseGeral().inserirTabela(inserir)
    # oids = dataBase().select()
    # print(oids)
    # dataBase().inserirTabela(atributo)
    return jsonify({'message': 'oid adicionado com sucesso'})

@app.route('/RemoveOidGeral', methods=['POST'])
def removeOidGeral():
    atributo = request.json
    print(atributo)
    dataBaseGeral().delete(atributo['totalGeral'])
    return jsonify({'message': 'oid removido com sucesso'})


app.run()