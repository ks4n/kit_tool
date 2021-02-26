import sqlite3
import requests
import re
import os.path
from datetime import date


class DataBase:
    def __init__(self, sala_poker, data_torneio, time, prize_pool, name_tournament, id_tournament, buy_in, password,
                 id_unique):
        self.id_unique = id_unique
        self.sala_poker = sala_poker
        self.data_torneio = data_torneio
        self.time = time
        self.prize_pool = prize_pool
        self.name_tournament = name_tournament
        self.id_tournament = id_tournament
        self.buy_in = buy_in
        self.password = password
        self.conexao = sqlite3.connect('db.sqlite3')
        self.cursor = self.conexao.cursor()

    def ler(self):
        """


        :return: retorna uma lista com os  para exibir no front
        """
        get_data = date.today()
        data = f'{get_data.strftime("%B")} {get_data.strftime("%d")}, {get_data.strftime("%Y")}'
        db = []
        self.cursor.execute("""
        SELECT * FROM torneios ORDER BY data_torneio DESC;
        """)
        for linha in self.cursor.fetchall():
            if data in linha:
                print(linha)
                db.append(linha)
        self.conexao.close()

        return db

    def inserir(self):
        self.cursor.execute("""
            INSERT or IGNORE INTO torneios (sala_poker, data_torneio, time, prize_pool, name_tournament, id_tournament, buy_in, password, id_unique)
            VALUES (?,?,?,?,?,?,?,?,?)
            """, (self.sala_poker, self.data_torneio, self.time, self.prize_pool, self.name_tournament,
                  self.id_tournament, self.buy_in, self.password, self.id_unique))
        self.conexao.commit()
        self.conexao.close()

    def criar_db_e_tabela(self):
        self.cursor.execute("""
        CREATE TABLE torneios (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                sala_poker NOT NULL,
                data_torneio NOT NULL,
                time NOT NULL,
                prize_pool NOT NULL, 
                name_tournament NOT NULL, 
                id_tournament NOT NULL, 
                buy_in NOT NULL,
                password NOT NULL, 
                id_unique NOT NULL UNIQUE

        );
        """)

        print('Tabela criada com sucesso.')
        # desconectando...
        self.conexao.close()


def checklogs(url):
    r = requests.get(url)
    result = r.text
    torneio_localizado = result.split('<span class="exroom">Poker Room:')
    reg_get_id = ''
    for torneio in torneio_localizado:
        if not '!DOCTYPE' in torneio:
            sala_poker = torneio.split('rel="noopener">')[1].split('</a>')[0]
            id_unique = torneio.split('id="')[1].split('">')[0]
            try:
                reg_get_id = re.findall('post+-[0-9][0-9][0-9][0-9][0-9]', torneio)[0]
            except IndexError:
                print('error value')
            if 'post-' in reg_get_id:
                data_torneio = torneio.split('display-single">')[1].split('</span>')[0]
                time = torneio.split('Time:</span>')[1].split('<br')[0]
                prize_pool = torneio.split('Prize Pool:</span>')[1].split('<br')[0]
                name_tournament = torneio.split('Name:</span>')[1].split('<br')[0]
                id = torneio.split('ID:</span>')[1].split('<br')[0]
                buy_in = torneio.split('Buy-in:</span>')[1].split('<br')[0]
                password = torneio.split('"expass2">')[1].split('</span>')[0]
                postar_blog = DataBase(sala_poker, data_torneio, time, prize_pool, name_tournament, id, buy_in,
                                       password, id_unique)
                postar_blog.inserir()


if not os.path.exists('db.sqlite3'):
    postar_blog = DataBase('', '', '', '', '', '', '', '', '')
    postar_blog.criar_db_e_tabela()

"""
checklogs('https://freerollpasswords.com/poker/pokerstars/')
checklogs('https://freerollpasswords.com/poker/888poker/')
postar_blog = DataBase('', '', '', '', '', '', '', '', '')
"""
