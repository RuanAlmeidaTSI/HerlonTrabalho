import socket
import threading
import wave
import time
import queue
import keyboard
fila = []


FORMATO = 'utf-8'
ServerIP = '192.168.56.1'
PORTA = 5050
ENDR = (ServerIP, PORTA)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ENDR)

chunk = 2048


M1 = 'Estamos A Navegar.wav'
M2 = 'A Cruel Angels Thesis.wav'
M3 = '99.wav'
M4 = 'Fantasia mitologica.wav'
M5 = 'Novo Mundo.wav'
M6 = 'Soul VS Soul.wav'
M7 = 'Traitor Requiem.wav'

Lista_musicas = [M1, M2,
                 M3, M4,
                 M5, M6,
                 M7]
playlista = [ ]









"""
    escolha = con.recv(1024).decode('utf-8')
    

    

    


"""
controle = False

def enviar_musica(con):
    num_mus = str(len(Lista_musicas))
    con.send(num_mus.encode(FORMATO))
    time.sleep(0.5)
    i = 0
    for i in range(len(Lista_musicas)):
        nome_musica = Lista_musicas[i]
        con.send(nome_musica.encode(FORMATO))
        time.sleep(0.5)



def tocarmusica(e1,con):
    global controle
    song = wave.open(e1, 'rb')
    dados = song.readframes(chunk)



    while dados:
        if controle == True:
            break
        try:
            con.send(dados)
            dados = song.readframes(chunk)
        except Exception:
            print('Cliente desconectou!!!')
            controle = True

            song.close()
            con.close()

def tocarmusicaplaylist(e5,con):


    global controle

    song = wave.open(e5, 'rb')
    dados = song.readframes(chunk)



    while dados:
        if controle == True:
            break
        try:
            con.send(dados)
            dados = song.readframes(chunk)
        except Exception:
            print('Cliente desconectou!!!')
            controle = True

            song.close()
            break


def musun(con):
    enviar_musica(con)

    e1 = con.recv(1024).decode(FORMATO)

    print(f'A ESCOLHA FOI : {e1}')

    if e1 == 'exit':
        print('\n')
        print('Nenhuma música foi escolhida!!!')
        print('O programa será fechado')
        print('\n')
        con.close()
    else:
        i = 0
        for i in range(len(Lista_musicas)):
            if e1 == f'{i}':
                e1 = Lista_musicas[i - 1]

        t2 = threading.Thread(target=tocarmusica, args=(e1, con))
        t2.start()


def playlist(con):
    enviar_musica(con)

    for i in range(4):
        e1 = con.recv(1024).decode(FORMATO)

        aux = int(e1)
        print(f'A MÚSICA {Lista_musicas[aux-1]} FOI ADICIONADA')
        fila.append(Lista_musicas[aux-1])


    e5 = fila[0]

    t6 = threading.Thread(target=tocarmusicaplaylist, args=(e5, con))
    j=0
    for j in range(len(fila)):
            if t6.is_alive() == False:
                e5 = fila[j]

                t6.start()
            else:
                j -= 1
                continue



def novocliente(con, adr):

    print('\n')
    print(f'[NOVA CONEXÃO] Cliente {adr} se conectou')
    print('\n')
    op = con.recv(1024).decode(FORMATO)
    if op == '1':
        musun(con)
    else:
        playlist(con)





def start():
    print('\n')
    print('[INICIANDO O SERVIDOR ...]')
    print('\n')
    server.listen()
    while True:

        con, adr = server.accept()

        t = threading.Thread(target=novocliente, args=(con, adr))
        t.start()


        print('\n')
        print(f'[NÚMERO DE CONEXÕES ATIVAS] {threading.active_count() - 1} ')
        print('\n')


start()





