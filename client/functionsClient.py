import os, socket, datetime, rsa, json, binascii, sys
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

HOST_B = '127.0.0.1'
PORT_B = 443

def logo():
    with open ('client/logoClient.txt', 'r') as file:
        fileLogo = file.read()
    print(fileLogo)    

def mainMenu():
    os.system('cls')
    logo()
    try:
        option = int(input(
            'Selecione uma das opções e pressione ENTER:'
            '\n1. Cadastrar sonda e gerar par de chaves'
            '\n2. Enviar chave da sonda'
            '\n3. Coletar dados da sonda'
            '\n4. Gerar assinatura e coletar dados'
            '\n5. Enviar os dados para a Terra'
            '\n6. Sair da aplicação'
            '\n\nOpção escolhida: '))
        if option == 1:
            probeRegister()
        elif option == 2:
            sendProbeKey()
        elif option == 3:
            createFile()
        elif option == 4:
            manageData()
        elif option == 5:
            sendMessage()
        elif option == 6:
            sys.exit()
        else:
            raise ValueError(f'Valor inválido')
    except Exception as e:
        print(f'Ocorreu um erro, tente novamente: {e}')
        os.system('pause')
        mainMenu()
            
def keyGeneration(probeName):
    try:   
        if not os.path.exists('client/data/probes'):
            os.makedirs('client/data/probes')
        probePath = os.path.join('client/data/probes', probeName.lower())
        os.makedirs(probePath, exist_ok = True) 
        key = RSA.generate(2048)
        
        privateKey = key.export_key()
        with open(os.path.join(probePath, f'{probeName.lower()}.private.pem'), 'wb') as file:
            file.write(privateKey)

        publicKey = key.public_key().export_key()
        with open(os.path.join(probePath, f'{probeName.lower()}.public.pem'), 'wb') as file:
            file.write(publicKey)
        print(f'A sonda {probeName} foi cadastrada e suas chaves foram geradas com sucesso')
    except Exception as e:
        print(f"Ocorreu um erro ao gerar as chaves para a sonda {probeName}: {e}")
        os.system('pause')
        mainMenu()

def probeRegister():
    os.system('cls')
    logo()
    listProbes()
    probeName = input('Digite o nome da Sonda: ')
    try:
        keyGeneration(probeName)
        os.system('pause')
        mainMenu()
    except Exception as e:
        print(f'Ocorreu um erro, tente novamente: {e}')
        os.system('pause')
        probeRegister()

def sendProbeKey():
    os.system('cls')
    logo()
    listProbes()
    probeName = input('Digite o nome da sonda que deseja enviar a chave: ')
    probeKeyPublicPath = f'client/data/probes/{probeName}/{probeName}.public.pem'
    try:
        with open(os.path.join(probeKeyPublicPath), 'rb') as file:
            publicKey = file.read()
            try:
                clientSocketB = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                clientSocketB.connect((HOST_B, PORT_B))
                message = {
                    'action': 'probeKey',
                    'probeName': probeName,
                    'publicKey': publicKey.decode()
                }
                messageReady = json.dumps(message)
                clientSocketB.send(messageReady.encode('utf-8')) 
                response = clientSocketB.recv(4096).decode('utf-8')
                print('Resposta do servidor: ', response)               
                os.system('pause')
                mainMenu()
            except Exception as e:
                print(f'Ocorreu um erro ao conectar com o servidor, tente novamente: {e}')  
                os.system('pause')
                mainMenu()
    except Exception as e:
        print(f'Ocorreu um erro ao buscar a chave da Sonda {probeName}, tente novamente: {e}')
        os.system('pause')
        mainMenu()

def createFile():
    os.system('cls')
    logo()
    listProbes()
    print('Insira os dados que você deseja criptografar:')
    try:
        probeName = input('Nome da Sonda: ')
        local = input('Local: ').replace(' ', '-')
        temp = str(int(input('Temperatura: '))) + 'ºC'
        radA = int(input('Radiação Alfa: '))
        radB = int(input('Radiação Beta: '))
        radG = int(input('Radiação Gama: '))
        date = datetime.datetime.now().strftime('%d.%m')
        data = {
            'Sonda': probeName,
            'Local': local,
            'Data': date,
            'Temperatura': temp,
            'Radiação Alfa': radA,
            'Radiação Beta': radB,
            'Radiação Gama' : radG
        }
        fileName = f'client/data/probes/{data["Sonda"]}/{data["Local"]}.{data["Data"]}.txt'

        with open(fileName, 'w') as file:
            file.write(f"Local: {data['Local']}\n")
            file.write(f"Temperatura: {data['Temperatura']}\n")
            file.write(f"Radiação Alfa: {data['Radiação Alfa']}\n")
            file.write(f"Radiação Beta: {data['Radiação Beta']}\n")
            file.write(f"Radiação Gama: {data['Radiação Gama']}\n")
        os.system('pause')
        mainMenu()
    except Exception as e:
        print(f'Ocorreu um erro ao cadastrar os valores, tente novamente: {e}')
        os.system('pause')
        createFile()


def encryptText(data, fileName):
    publicKeyPem = open(f'client/data/probes/{data["Sonda"]}/{data["Sonda"]}.public.pem').read()
    publicKey = RSA.import_key(publicKeyPem)
    cipher = PKCS1_OAEP.new(publicKey)
    plainText = open(fileName, 'rb').read()
    cipherText = cipher.encrypt(plainText)
    return cipherText
        
def listProbes():
    probePath = 'client/data/probes'
    if os.path.exists(probePath):
        probeFolder = [folder for folder in os.listdir(probePath) if os.path.isdir(os.path.join(probePath, folder))]
        if probeFolder:
            print("Sondas disponíveis:")
            for folder in probeFolder:
                print(folder)
        else:
            print("Não há sondas cadastradas.")

def manageData():
    os.system('cls')
    logo()
    listProbes()
    probeName = input('Digite o nome da sonda: ')
    probePath = f'client/data/probes/{probeName}'
    privateKeyPath = probePath + f'/{probeName}.private.pem'
    if os.path.exists(probePath):
        dataFiles = [file for file in os.listdir(probePath) if file.lower().endswith('.txt') and os.path.isfile(os.path.join(probePath, file))]
        if dataFiles:
            print(f"Dados disponíveis para gerar assinatura na sonda {probeName}:")
            for i, file in enumerate(dataFiles, start=1):
                print(f"{i}. {file}")
            chosenNumber = input('Digite o número correspondente ao arquivo que deseja gerar assinatura: ')
            try:
                chosenNumber = int(chosenNumber)
                chosenFile = dataFiles[chosenNumber - 1]
                confirm = input(f"Você confirma a escolha do arquivo '{chosenFile}'? (s/n): ")
                if confirm.lower() != 's':
                    print('Operação cancelada. Escolha novamente.')
                    manageData()
                else:
                    print(f"Iniciando a assinatura do arquivo '{chosenFile}'...")
                    try:
                        chosenFilePath = f'{probePath}' + f'/{chosenFile}'
                        signFile(privateKeyPath, chosenFilePath, probePath, chosenFile)
                        print(f'Assinatura dos dados {chosenFile} foram um sucesso!')
                        os.system('pause')
                        mainMenu()
                    except Exception as e:
                        print(f'Ocorreu um erro ao assinar os dados: {e}')
                        os.system('pause')
                        manageData()
            except:
                print("Por favor, digite um número válido.")
                os.system('pause')
                mainMenu()
        else:
            print(f"Não há dados disponíveis para gerar assinatura na sonda {probeName}.")
            os.system('pause')
            mainMenu()            
    else:
        print(f"A sonda {probeName} não existe ou não possui dados disponíveis para criptografar.")
        os.system('pause')
        mainMenu()

def signFile(privateKeyPath, filePath, signaturePath, fileName):
    try:
        with open(privateKeyPath, 'rb') as keyFile:
            privateKeyData = keyFile.read()
            privateKey = rsa.PrivateKey.load_pkcs1(privateKeyData)
        with open(filePath, 'rb') as file:
            data = file.read()
        signature = rsa.sign(data, privateKey, 'SHA-256')
        fileName = fileName.replace('.txt', '')
        with open(f'{signaturePath}/' + f'{fileName}assinatura' , 'wb') as sign:  
            sign.write(signature)
        
    except Exception as e:
        print(f'Houve uma falha ao assinar o arquivo: {e}')
        os.system('pause')
        mainMenu()

def sendMessage():
    os.system('cls')
    logo()
    listProbes()
    try:
        probeName = input('Digite o nome da sonda que deseja enviar a chave: ')
        chosenFile = readyFiles(probeName)  
        if chosenFile:
            try:
                clientSocketB = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                clientSocketB.connect((HOST_B, PORT_B))

                probePath = f'client/data/probes/{probeName}'
                txtFilePath = os.path.join(probePath, chosenFile)
                signatureFilePath = os.path.join(probePath, chosenFile.replace('.txt', 'assinatura'))

                with open(txtFilePath, 'rb') as txtFile:
                    cryptoData = binascii.hexlify(txtFile.read()).decode('utf-8')
                with open(signatureFilePath, 'rb') as sigFile:
                    sigData = binascii.hexlify(sigFile.read()).decode('utf-8')

                message = {
                    'action': 'sendData',
                    'probeName': probeName,
                    'cryptoData': cryptoData,
                    'sigData': sigData
                }
                clientSocketB.send(json.dumps(message).encode('utf-8'))
                response = clientSocketB.recv(4096).decode('utf-8')
                print('Resposta do servidor: ', response)
                os.system('pause')
                mainMenu()
            except Exception as e:
                print(f'Ocorreu um erro ao conectar com o servidor, tente novamente: {e}')  
                os.system('pause')
                sendMessage() 
        else:
            raise Exception('Sonda não localizada')
    except Exception as e: 
        print(f'Ocorreu um erro, tente novamente: {e}')
        os.system('pause')
        sendMessage()

def readyFiles(probeName):
    try:
        probePath = f'client/data/probes/{probeName}'
        readyFiles = []
        if os.path.exists(probePath):
            dataFiles = [file for file in os.listdir(probePath) if file.lower().endswith('.txt') and os.path.isfile(os.path.join(probePath, file))]
            for dataFile in dataFiles:
                signatureFile = dataFile.replace('.txt', 'assinatura')
                if os.path.isfile(os.path.join(probePath, signatureFile)):
                    readyFiles.append(dataFile)
            if readyFiles:
                print(f'Arquivos prontos da sonda {probeName}:')
                for i, file in enumerate(readyFiles, start=1):
                    print(f'{i}. {file}')
                try:
                    chosenNumber = int(input('Digite o número correspondente ao arquivo que deseja gerar assinatura: '))
                    chosenFile = readyFiles[chosenNumber - 1]
                    confirm = input(f"Você confirma a escolha do arquivo '{chosenFile}'? (s/n): ")
                    if confirm.lower() != 's':
                        print('Operação cancelada. Escolha novamente.')
                        os.system('pause')
                        sendMessage()
                    else:
                        print(f'Fazendo envio do arquivo: {chosenFile}')
                        return chosenFile
                except ValueError:
                    print("Por favor, digite um número válido.")
                    os.system('pause')
                    sendMessage()
                except IndexError:
                    print("Por favor, escolha um número dentro da lista.")
                    os.system('pause')
                    sendMessage()
            else:
                raise Exception(f'Não há arquivos prontos para a sonda {probeName}.')
        else:
            raise Exception(f'O caminho da sonda {probeName} não existe.')
    except Exception as e:
        print(f'Ocorreu um erro ao buscar os arquivos prontos: {e}')
        os.system('pause')
        sendMessage()