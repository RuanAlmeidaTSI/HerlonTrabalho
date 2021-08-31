import socket
import time
import pyaudio
import keyboard
import os


FORMATO = 'utf-8'
ServerIP = '192.168.56.1'
PORTA = 12000
ENDR = (ServerIP, PORTA)

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


frm = 8
chn = 2
rt = 44100
chunk = 128


p = pyaudio.PyAudio()
stream = p.open(format=frm,
                channels=chn,
                rate=rt,
                output=True
                )

controle = False
nome_musica = []
def lista_mus():
    global nome_musica
    num_mus = int(cliente.recv(1024).decode('utf-8'))
    for i in range(num_mus):
        aux = cliente.recv(1024).decode('utf-8')
        nome_musica.append(aux)
    for j in range(len(nome_musica)):
        print(f'{j} - {nome_musica[j - 1]}')

def escolha():
    print(' ')
    escolha = input("Escreva o número da musica:")

    if escolha == '':
        print('\n')
        print('Nenhuma música foi escolhida!!!')
        print('O programa será fechado')
        print('\n')
        escolha = 'exit'

    elif escolha.isalpha() == True:
        print('\n')
        print('Nenhuma música foi escolhida!!!')
        print('O programa será fechado')
        print('\n')
        escolha = 'exit'

    elif int(escolha) > 7 or int(escolha) < 0:
        print('\n')
        print('Nenhuma música foi escolhida!!!')
        print('O programa será fechado')
        print('\n')
        escolha = 'exit'

    else:

        aux = int(escolha)
        print('')
        print('')
        print(f'A musica {nome_musica[aux - 1]} será tocada')
        print('')
        print('')
    return escolha

def recebermusica():
        global controle
        conteudo = cliente.recv(chunk)
        print('Iniciando a música...')
        print(' ')
        print('Pressione espaço para pausar a música')
        print('Pressione control para retomar a música')
        print('Pressione ESC para parar a música')
        while controle == False:
            while conteudo:

                    stream.write(conteudo)

                    conteudo = cliente.recv(chunk)
                    try:
                        if ((conteudo[(len(conteudo) - 5)]).decode() == 'Pare'):
                            controle = True
                            break
                    except:
                        pass
                    if keyboard.is_pressed('space'):
                        print('Músíca pausada')
                        print('')
                        print('')
                        print('Pressione control para continuar')
                        keyboard.wait('ctrl')
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print('Pressione espaço para pausar a música')
                        print('Pressione control para retomar a música')
                        print('Pressione ESC para parar a música')
                    if keyboard.is_pressed('esc'):

                            controle = True

                            print('')
                            print('A reprodução da música foi cancelada')
                            print('')
                            print('A conexão será fechada em alguns instantes...')
                            time.sleep(5)
                            p.terminate()
                            stream.close()
                            cliente.close()

        print('')

def MusicaUn():

    lista_mus()

    e1 = escolha()
    if e1 == 'exit':
        time.sleep(5)
        p.terminate()
        stream.close()
        cliente.close()

    cliente.send(e1.encode(FORMATO))

    recebermusica()

def menu():
    print('\n')
    print('SEJA BEM-VINDO')
    print('\n')
    print('Este é o player de música de socket')
    print('\n')
    print('====================================')
    print('Escolha qual operação deseja realizar:')
    print('\n')
    print('1- Música Única')
    print('2- Sair')
    print('\n')
    controle = 0
    while controle == 0:
        op = input("> ")
        if op == '1':
            cliente.connect(ENDR)
            cliente.send(op.encode(FORMATO))
            print('Executando função Música Única ... !!!' + '\n')
            MusicaUn()
            break
        elif op == '2':
            print('Finalizando o programa ... !!!')
            time.sleep(3)
            break
        else:
            print('Não foi fornecida uma opção válida!!!')
            print('Insira sua opção novamente')
            continue


def iniciar():

        menu()

iniciar()
