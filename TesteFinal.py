import socket
import time
import pyaudio
'''
import keyboard
import os
'''

FORMATO = 'utf-8'
ServerIP = '127.0.0.1'
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
        aux2 = aux.split(".")
        nome_musica.append(aux2[0])
    for j in range(len(nome_musica)):
        print(f'{j} - {nome_musica[j]}')


def escolha():

    print(' ')
    es = input("Escreva o número da musica:")

    if es == '':
        print('\n')
        print('Nenhuma música foi escolhida!!!')
        print('O programa será fechado')
        print('\n')
        es = 'exit'

    elif es.isalpha() is True:
        print('\n')
        print('Nenhuma música foi escolhida!!!')
        print('O programa será fechado')
        print('\n')
        es = 'exit'

    elif int(es) > len(nome_musica) or int(es) < 0:
        print('\n')
        print('Nenhuma música foi escolhida!!!')
        print('O programa será fechado')
        print('\n')
        es = 'exit'

    else:

        aux = int(es)
        print('\n')
        print(f'A musica " {nome_musica[aux]} " será tocada')
        print('\n')
    return es


def recebermusica():

    conteudo = cliente.recv(chunk)
    print('Iniciando a música...')
    print(' ')
    print('Pressione espaço para pausar a música')
    print('Pressione control para retomar a música')
    print('Pressione ESC para parar a música')
    while conteudo:
        stream.write(conteudo)
        conteudo = cliente.recv(chunk)
        if conteudo == '1':
            print('\n A música acabou!')
            print('A conexão será fechada em alguns instantes...')
            time.sleep(5)
            p.terminate()
            stream.close()
            cliente.close()


'''     
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

                            print('')
                            print('A reprodução da música foi cancelada')
                            print('')
                            
'''


def musicaun():

    lista_mus()

    e1 = escolha()
    if e1 == 'exit':
        time.sleep(5)
        p.terminate()
        stream.close()
        cliente.close()
    else:
        cliente.send(e1.encode(FORMATO))

    recebermusica()


def menu():

    cliente.connect(ENDR)
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
    control = 0
    while control == 0:
        op = input("> ")
        if op == '1':
            cliente.send(op.encode(FORMATO))
            print('Executando função Música Única ... !!!' + '\n')
            musicaun()
            control = 1
        elif op == '2':
            print('Finalizando o programa ... !!!')
            time.sleep(3)
            control = 1
        else:
            print('Não foi fornecida uma opção válida!!!')
            print('Insira sua opção novamente')
            continue
    cliente.close()


def iniciar():

    menu()


iniciar()
