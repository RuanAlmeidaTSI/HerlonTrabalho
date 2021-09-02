import socket
import threading
import wave
import time

FORMATO = 'utf-8'
ServerIP = ''
PORTA = 12000
ENDR = (ServerIP, PORTA)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ENDR)

chunk = 128

listaconectados = []

M1 = "teste.wav"
M2 = "Yoko Takahashi - A Cruel Angel's Thesis.wav"
M3 = 'Mob Choir - 99.wav'
M4 = 'Yôsei Teikoku - Fantasia Mitológica.wav'
M5 = 'One Piece - Novo Mundo.wav'
M6 = 'Hironobu Kageyama - Soul VS Soul.wav'
M7 = "Daisuke Hasegawa -Traitor's Requiem.wav"
M8 = 'One Piece - Estamos A Navegar.wav'
M9 = "Daft Punk - Get Lucky.wav"
M10 = "Rick Astley Never Gonna Give You Up.wav"
M11 = "The Cranberries - Zombie.wav"
M12 = "Yes - Roundabout.wav"
M13 = "Boney M - Rasputin.wav"
M14 = "John Cafferty - Heart's on Fire.wav"
M15 = "Kansas - Carry on Wayward Son.wav"

Lista_musicas = [M1, M2, M3, M4,
                 M5, M6, M7, M8,
                 M9, M10, M11, M12,
                 M13, M14, M15]

controle = False


def enviar_musica(con):

    num_mus = str(len(Lista_musicas))
    con.send(num_mus.encode(FORMATO))
    time.sleep(0.5)
    for i in range(len(Lista_musicas)):
        nome_musica = Lista_musicas[i]
        con.send(nome_musica.encode(FORMATO))
        time.sleep(0.5)


def tocarmusica(e3, con):

    song = wave.open(e3, 'rb')
    dados = song.readframes(chunk)
    stop = '1'

    while dados:
        try:
            con.send(dados)
            dados = song.readframes(chunk)
            if len(dados) < 1:
                con.send(stop.encode(FORMATO))
        except:
            print('\n A música foi interrompida!!!')
            print('\n Cliente se desconectou!!!')
            break
    time.sleep(0.5)
    song.close()
    con.close()


def tocarplay(nomes, con):

    for i in range(len(nomes)):
        time.sleep(5)

        print(f'\n Próxima música > {nomes[i]} começando...')
        song = wave.open(nomes[i], 'rb')
        dados = song.readframes(chunk)
        stop = '1'

        while dados:
            try:
                con.send(dados)
                dados = song.readframes(chunk)
                if len(dados) < 1:
                    con.send(stop.encode(FORMATO))
            except:
                print(f'\n A música {nomes[i]} foi pulada!!!')
                song.close()

                break
        song.close()

    time.sleep(0.5)

    con.close()


def musplay(con):
    filanomes = ['', '', '', '', '']
    listaplay = [0, 0, 0, 0, 0]
    enviar_musica(con)
    e1 = con.recv(1024).decode(FORMATO)
    e2 = int(e1)

    for i in range(e2):
        aux = con.recv(1024).decode(FORMATO)
        time.sleep(0.5)
        listaplay[i] = int(aux)
        aux2 = Lista_musicas[int(aux)]
        filanomes[i] = aux2
        aux3 = aux2.split(".")
        print(f'A MÚSICA "{aux3[0]}" FOI ADICIONADA')

    tocarplay(filanomes, con)
    con.close()


def musun(con, adr):

    enviar_musica(con)
    e1 = con.recv(1024).decode(FORMATO)
    e2 = int(e1)
    aux = Lista_musicas[e2]
    aux2 = aux.split(".")
    print(f'A MÚSICA ESCOLHIDA FOI : "{aux2[0]}"')

    if e1 == 'exit':
        print('\n')
        print('Nenhuma música foi escolhida!!!')
        print('\n')
        print(f'O cliente {adr} irá ser desconectado')
        print('\n')
        con.close()
    else:
        for i in range(len(Lista_musicas)):
            if e2 == i:
                e3 = Lista_musicas[i]
                tocarmusica(e3, con)

        con.close()


def novocliente(con, adr):

    print('\n')
    print(f'[NOVA CONEXÃO] Cliente {adr} se conectou\n')
    print('\n')
    op = con.recv(1024).decode(FORMATO)
    if op == '1':
        print('\nAguarde...')
        print(f'Cliente {adr} está escolhendo sua música...')
        musun(con, adr)
        print('\n')
        print(f'[AVISO] Cliente {adr} terminou sua música e será desconectado')
        con.close()
    elif op == '2':
        print('\nAguarde...')
        print(f'Cliente {adr} está escolhendo sua playlist...')
        musplay(con)
        print('\n')
        print(f'[AVISO] Cliente {adr} terminou sua playlist e será desconectado')
        con.close()
    else:
        print('\n')
        print(f'[AVISO] Cliente {adr} se desconectou')
        con.close()


def start():
    print('\n')
    print('[INICIANDO O SERVIDOR ...]')
    time.sleep(2)
    print('[SERVIDOR INICIADO]')
    print('[SERVIDOR AGUARDANDO CONEXÕES]')
    print('\n')
    server.listen(10)
    while True:
        con, adr = server.accept()
        listaconectados.append(adr)
        t = threading.Thread(target=novocliente, args=(con, adr))
        t.start()

        print(f'\n[NÚMERO DE CONEXÕES ATIVAS] {threading.active_count() - 1} ')
        for i in range(threading.active_count() - 1):
            print(f'[CONEXÃO ATIVA N° {i}] {listaconectados[i]}\n')


start()
