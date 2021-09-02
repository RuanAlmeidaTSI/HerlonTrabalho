import socket
import time
import pyaudio
import os

FORMATO = 'utf-8'
ServerIP = '10.8.0.14'
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


def escolhaplay():

    listaplay = ['', '', '', '', '']
    print(' ')
    print('\n')
    print('Escolha 5 músicas, uma por vez, para serem tocadas em sequência')
    for i in range(5):
        es = input("Escreva o número da musica:")
        if es == '':
            print('\n')
            print('Opção inválida!!!')
            print('\n')
            print(f'A musica " {nome_musica[1]} " foi escolhida por padrão')
            print('\n')
            listaplay[i] = '0'

        elif es.isalpha() is True:
            print('\n')
            print('Opção inválida!!!')
            print('\n')
            print(f'A musica " {nome_musica[1]} " foi escolhida por padrão')
            print('\n')
            listaplay[i] = '0'

        elif int(es) > len(nome_musica) or int(es) < 0:
            print('\n')
            print('Opção inválida!!!')
            print('\n')
            print(f'A musica " {nome_musica[1]} " foi escolhida por padrão')
            print('\n')
            listaplay[i] = '0'

        else:
            aux = int(es)
            listaplay[i] = es
            print('\n')
            print(f'A musica " {nome_musica[aux]} " foi inserida na posição {i+1}')
            print('\n')

    return listaplay


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

    elif int(es) > 14 or int(es) < 0:
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
    print('Pressione Ctrl + C para parar a música')
    while conteudo:
        try:
            stream.write(conteudo)
            conteudo = cliente.recv(chunk)
            if conteudo == '1':
                print('\n A música acabou!')
                print('\nA conexão será fechada em alguns instantes...')
                break
        except KeyboardInterrupt:
            print('')
            os.system('cls' if os.name == 'nt' else 'clear')
            print('A reprodução da música foi cancelada')
            print('A conexão será fechada em alguns instantes...')
            print('')
            break

    time.sleep(5)
    p.terminate()
    stream.close()
    cliente.close()


def receberplay():

    for i in range(5):
        time.sleep(5)

        print('Iniciando a música...')
        print(' \n Aguarde alguns instantes\n')
        print('Pressione Ctrl + C para pular a música')
        conteudo = cliente.recv(chunk)
        while conteudo:
            try:
                stream.write(conteudo)
                conteudo = cliente.recv(chunk)
                if conteudo == '1':
                    print('\n A música acabou!')
                    print('\nA conexão será fechada em alguns instantes...')
                    break
            except KeyboardInterrupt:
                print('')
                os.system('cls' if os.name == 'nt' else 'clear')
                print('A música foi pulada!')
                print('')
                break

    time.sleep(5)
    p.terminate()
    stream.close()
    cliente.close()


def musicaplay():
    lista_mus()

    e1 = escolhaplay()
    aux = str(len(e1))
    cliente.send(aux.encode(FORMATO))

    for i in range(len(e1)):
        cliente.send(e1[i].encode(FORMATO))
        time.sleep(0.5)

    receberplay()


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
    print('====================================')
    print('SEJA BEM-VINDO')
    print('\n')
    print('====================================')
    print('Este é o player de música de socket')
    print('\n')
    print('====================================')
    print('Escolha qual operação deseja realizar:')
    print('\n')
    print('1- Música Única')
    print('2- Playlist')
    print('3- Sair')
    print('\n')
    control = 0
    while control == 0:
        op = input("> ")
        if op == '1':
            cliente.send(op.encode(FORMATO))
            os.system('cls' if os.name == 'nt' else 'clear')
            print('Executando função Música Única ... !!!' + '\n')
            musicaun()
            control = 1
        elif op == '2':
            cliente.send(op.encode(FORMATO))
            print('\n')
            os.system('cls' if os.name == 'nt' else 'clear')
            print('Executando função Playlist ... !!!' + '\n')
            musicaplay()
            control = 1
        elif op == '3':
            print('\n')
            print('Finalizando o programa ... !!!')
            time.sleep(3)
            control = 1
        else:
            print('\n')
            print('Não foi fornecida uma opção válida!!!')
            print('Insira sua opção novamente')
            continue


def iniciar():

    menu()


iniciar()
