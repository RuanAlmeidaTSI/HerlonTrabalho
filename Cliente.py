import socket
import threading
import time

import pyaudio
import queue
import keyboard
import os
import sys

FORMATO = 'utf-8'
ServerIP = '192.168.56.1'
PORTA = 5050
ENDR = (ServerIP, PORTA)

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


playlista = []


frm = 8
chn = 2
rt = 44100
chunk = 2048
flagM = 0


nome_musica = []

p = pyaudio.PyAudio()
stream = p.open(format=frm,
                channels=chn,
                rate=rt,
                output=True
                )

'''
def escolher_musica():
    

   if keyboard.is_pressed('p'):
            print('Músíca Interrompida')
            break

        if keyboard.is_pressed('v'):
            print('Músíca Interrompida')
            break

def Playlist():
    pass
'''''

'''




    
'''

'''
def musicaUnica():


 
    lista_mus()
    while True:

        

        


       

           
            



           
        break
'''









"""
escolher_opcao()
FlagT = 'A'

if flagM == 1:
    musicaUnica()
    stream.close()
    p.terminate()



    cliente.close()
else:
    sys.exit()
     print('Iniciando a música...')
    print(' ')
    print('Pressione espaço para pausar a música')
    print('Pressione control para retomar a música')
    print('Pressione ESC para parar a música')
    print('Pressione P para pular a música atual (APENAS PARA PLAYLISTS!!!)')
    print('Pressione V para voltar à música anterior(APENAS PARA PLAYLISTS!!!)')
"""

controle = False

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
        content = cliente.recv(chunk)

        while controle == False:
            while content:

                    stream.write(content)

                    content = cliente.recv(chunk)

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

def playlist():
    lista_mus()
    print('Escolha quais musicas quer adicionar à playlist:')
    print('Escolha apenas uma por vez!!!')
    print('Tamanho limite = 4 músicas')

    for i in range(4):
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
            print(f'A musica {nome_musica[aux - 1]} foi adicionada')
            print('')
            print('')
            cliente.send(escolha.encode(FORMATO))

        """        
        muz = input('> ')
        if muz == ' ':
            print('Opção inválida!!!')
            i -= 1
        elif muz.isalpha() == True:
            print('Opção inválida!!!')
            i -= 1
        elif int(escolha) > 7 or int(escolha) < 0:
            print('Opção inválida!!!')
            i -= 1
        else:
            cliente.send(muz.encode(FORMATO))
        """

    for i in range(4):

        t3 = threading.Thread(target=recebermusica, args=())

        if t3.is_alive() == False:
                t3.start()
        else:
            i -= 1
            continue

def MusicaUn():

    lista_mus()

    e1 = escolha()
    cliente.send(e1.encode(FORMATO))

    if e1 == 'exit':
        time.sleep(5)
        p.terminate()
        stream.close()
        cliente.close()

    t = threading.Thread(target=recebermusica, args=())

    t.start()

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
    print('2- Playlist')
    print('3- Sair')
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
            cliente.connect(ENDR)
            cliente.send(op.encode(FORMATO))
            print('Executando função playlist ... !!!' + '\n')
            playlist()
            break
        elif op == '3':
            print('Finalizando o programa ... !!!')
            time.sleep(3)
            break
        else:
            print('Não foi fornecida uma opção válida!!!')
            print('Insira sua opção novamente')
            pass


def iniciar():

    menu()



iniciar()

