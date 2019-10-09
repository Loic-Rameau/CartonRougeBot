import sqlite3


ROUGE = 629594572720177152
JAUNE = 629606962044207115


def _update(user, carton, nb):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE cartons SET nb = :nb where user=:user and type=:type',
                   {"user": user.id, "nb": nb, "type": carton})
    conn.commit()
    conn.close()


def _insert(user, carton):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO cartons(user,nb,type) VALUES (:user, :nb,:type)',
                   {"user": user.id, "nb": 1, "type": carton})
    conn.commit()
    conn.close()


class Carton:
    def __init__(self, user, carton, nb=0):
        self.user = user
        self.carton = carton
        self.nb = nb


def fethAllCartons():
    cartons = []
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cartons ORDER BY user, type")
    conn.close()
    for row in cursor.fetchall():
        cartons.append(Carton(row[0], row[2], row[1]))
    return cartons


def getCartons(user, carton):
    cartons = Carton(user, carton)
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT nb FROM cartons WHERE user = ?", (user.id,))
    fetch = cursor.fetchone()
    if fetch is None:
        conn.close()
        return cartons
    conn.commit()
    conn.close()
    print(f'select where user {user.name} donne {fetch[0]} carton {carton}')
    if fetch:
        cartons.nb = fetch[0]

    return cartons


async def addCarton(user, carton, channel):
    print(f'Add carton {carton}')
    current_cartons = getCartons(user, carton)
    if current_cartons.nb == 0:
        return _insert(user, carton)

    if carton == JAUNE:
        if current_cartons.nb >= 1:
            _update(user, JAUNE, 0)
            rouges = getCartons(user, ROUGE)
            await channel.send(
                f'2iem <:jaune:629606962044207115> pour {user.name} ... il se rammase donc un <:rouge:629594572720177152> !'
            )
            nb = rouges.nb + 1
            if rouges.nb == 0:
                _insert(user, ROUGE)
            else:
                _update(user, ROUGE, nb)
            await channel.send(f'{user.name} est désormait à {nb} <:rouge:629594572720177152> !')
        else:
            _update(user, carton, current_cartons.nb + 1)
    else:
        _update(user, carton, current_cartons.nb + 1)
        await channel.send(f'{user.name} est désormait à {current_cartons.nb + 1} <:rouge:629594572720177152> !')
