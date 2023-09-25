import socket, threading, os, json, binascii, rsa
from Crypto.PublicKey import RSA

HOST_A = '127.0.0.1'
PORT_A = 443
serverSocketA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def logo():
    with open('server/logoServer.txt', 'r') as file:
        fileLogo = file.read()
    os.system('cls')
    print(fileLogo)
    Connection()

def receiveMessages(client_socket):
    while True:
        data = client_socket.recv(4096)
        if not data:
            client_socket.close()
            print('Conexão encerrada com a sonda.')
            break
        probeKeyReceive(data)
        dataReceive(data, client_socket)
        

def fileOpen(file):
    keyFile = open(file, 'rb')
    keyData = keyFile.read()
    keyFile.close()
    publicKey = RSA.import_key(keyData)
    return publicKey

def dataReceive(data, client_socket):
    try:
        message = json.loads(data.decode('utf-8'))
        action = message.get('action')
        if action == 'sendData':
            probeName = message.get('probeName')
            cryptoData = binascii.unhexlify(message['cryptoData'])
            sigData = binascii.unhexlify(message['sigData'])
            print(f'Conexão estabelecida com a sonda: {probeName}')
            publicKeyPath = f'server/keys/{probeName.lower()}.public.pem'
            with open(publicKeyPath, 'rb') as file:
                file.read()
            publicKey = fileOpen(publicKeyPath)
            try:
                rsa.verify(cryptoData, sigData, publicKey)
                print('A assinatura está validada com sucesso!')
                validacao = 'A assinatura está validada com sucesso!'
            except:
                print('Essa assinatura é inválida')
                validacao = 'Essa assinatura é inválida'
            client_socket.send(validacao.encode('utf-8'))
    except Exception as e:
        print(f'Ocorreu um erro ao processar a mensagem recebida: {e}')

def probeKeyReceive(data):
    message = json.loads(data.decode('utf-8'))
    action = message.get('action')
    if action == 'probeKey':
        probeName = message.get('probeName')
        publicKey = message.get('publicKey')
        print(f'Conexão estabelecida com a sonda: {probeName}')
        try:   
            if not os.path.exists('server/keys'):
                os.makedirs('server/keys')               
            with open(f'server/keys/{probeName.lower()}.public.pem', 'wb') as file:
                file.write(publicKey.encode())
                print(f'Chave Pública da sonda {probeName} recebida e salva com sucesso!')
                print('Aguardando conexão da Sonda...')
        except Exception as e:
            print(f'Ocorreu um erro ao receber os dados: {e}')
            print('Aguardando conexão da Sonda...')

def Connection():
    try:
        serverSocketA.bind((HOST_A, PORT_A))
        serverSocketA.listen()  
        print('Aguardando conexão da Sonda...')
        while True:
            clientSocketA, clientAddressA = serverSocketA.accept()
            receiveThread = threading.Thread(target=receiveMessages, args=(clientSocketA,))
            receiveThread.start()
    except Exception as e:
        print(f'Ocorreu um erro ao se conectar com a Sonda! {e}')
        os.system('pause')

logo()