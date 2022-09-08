import csv
import os
import shutil
import subprocess
import traceback
from datetime import datetime
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d
import zlib
from pysnmp.hlapi import *

def diaAtual():
    from datetime import datetime
    diaAtual = datetime.now().strftime('%d-%m-%Y')
    return diaAtual

def diaAnterior():
    from datetime import datetime, timedelta
    diaAnterior = (datetime.now() - timedelta(1)).strftime('%d-%m-%Y')
    return diaAnterior
def ok(lugar , diretorio = 'GPLAp.txt'):
    try:
        with open(f'logs/{diretorio} - {diaAtual()}.txt', 'a') as f:
            writer = csv.writer(f, lineterminator='\r')
            writer.writerow([f'{datetime.today().strftime("[%Y-%m-%d %H:%M:%S]")} {lugar} Ok\n\n'])
            f.close()

        pathDiaAnterior = f'logs/{diretorio} - {diaAnterior()}.txt'
        if os.path.exists(pathDiaAnterior):
            shutil.move(pathDiaAnterior,f'old/{diretorio} - {diaAnterior()}.txt')
    except:
        ...



def erro(lugar , diretorio = 'GPLAp.txt', logErro = True):
    try:
        print(traceback.format_exc())
        with open(f'logs/{diretorio} - {diaAtual()}.txt', 'a') as f:
            writer = csv.writer(f, lineterminator='\r')
            writer.writerow([f'{datetime.today().strftime("[%Y-%m-%d %H:%M:%S]")} {lugar} Erro \n\n'])
            if logErro == True:
                writer.writerow([f'{traceback.format_exc()}'])
            f.close()

        pathDiaAnterior = f'logs/{diretorio} - {diaAnterior()}.txt'
        if os.path.exists(pathDiaAnterior):
            shutil.move(pathDiaAnterior,f'old/{diretorio} - {diaAnterior()}.txt')
    except:
        ...

def ip():
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
        local_ip_address = s.getsockname()[0]
        if not local_ip_address.startswith("127."):
            # print(local_ip_address)
            return local_ip_address
        else:
            local_ip_address = 'localhost'
            # print(local_ip_address)
            return local_ip_address
    except:
        local_ip_address = 'localhost'
        # print(local_ip_address)
        return local_ip_address

def getItemOID(ip,oid):
    oid = oid.split('.')
    z = []
    for i in oid:
        z.append(int(i))
        # 1, 3, 6, 1, 2, 1, 1, 1, 0
        # 1.3.6.1.2.1.1.1.0

    oid = tuple(z)



    iterator = getCmd(
        SnmpEngine(),
        CommunityData('public', mpModel=0),
        UdpTransportTarget((ip, 161)),
        ContextData(),
        # ObjectType(ObjectIdentity('IF-MIB', 'ifNumber', 0))
        # ObjectType(ObjectIdentity((1,3,6,1,2,1,1,1,0)))
        ObjectType(ObjectIdentity(oid))
    )

    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

    if errorIndication:
        # print(errorIndication)
        return 'Not a printer'
        # return errorIndication

    elif errorStatus:
        # print('%s at %s' % (errorStatus.prettyPrint(),
        #                     errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        return 'Not a printer'

    else:
        for varBind in varBinds:
            # print(varBind[1])
            # print(' = '.join([x.prettyPrint() for x in varBind]))
            return varBind[1]


def listaImpressorasPingadas(ip):
    # hostname = '.'.join(ip().split('.')[0:3])
    try:
        hostname = '.'.join(ip.split('.')[0:3])
        listaIpsImpressora = []
        for ips in range(1,255):
            hostname_aux = hostname+f'.{str(ips)}'
            ok(hostname_aux)

            try:
                try:
                    with open('dados/segundos.txt','r') as f:
                        TIMEOUT = float(f.readline())
                except:
                    TIMEOUT = 0.5


                # resultado = os.system("ping -c 1 " + hostname_aux)
                # resultado = subprocess.run(
                #     f"ping -n 1 {hostname_aux}",
                #     stdout=subprocess.DEVNULL,
                #     stderr=subprocess.DEVNULL,
                #     timeout=TIMEOUT,
                #     shell=True)
                import ping3
                ping3.DEBUG=True


                resultado = ping3.ping(hostname_aux,timeout=TIMEOUT)

                ok(f'Resultado: {resultado}\n\n')
                ok(f'ip: {ip}\n\n')
                ok(f'ips: {ips}\n\n')
                if hostname_aux == ip or ips == 1 or ips == 254 or ips == 255:
                    ok(f'{ip()} ON mas não é uma impressora')
                    ...
                # elif resultado.returncode == 1:
                # elif resultado == False:
                elif resultado == None or resultado == False:
                    ok(hostname_aux + ' off')
                    pass
                # elif resultado.returncode == 0:
                # elif resultado == True:
                else:
                    listaIpsImpressora.append(hostname_aux)
                    ok(hostname_aux + ' ON')


            except subprocess.TimeoutExpired:
                erro('')
                # print(hostname_aux + ' off')
            except:
                erro('')
                # print(traceback.format_exc())
        return listaIpsImpressora
    except:
        erro('')
        return []

def OIDcomLista():
    listaImps = listaImpressorasPingadas(ip())
    print(listaImps)
    for i in listaImps:
        try:
            print(i+': ')
            getItemOID(i,'1.3.1')
        except:
            print(traceback.format_exc())

def OIDsemLista(ip, oid):
    try:
        testOid = getItemOID(ip,oid)
        try:
            testOid = int(testOid)
            return 'Is a printer'
        except:
            return 'Not a printer'
    except:
        # print(traceback.format_exc())
        return 'Not a printer'
    # input('Press Enter')
def obscure(data: bytes) -> bytes:
    return b64e(zlib.compress(data, 9))

def unobscure(obscured: bytes) -> bytes:
    return zlib.decompress(b64d(obscured))