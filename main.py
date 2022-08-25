import os
import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Shop, Book, Stock, Sale


if __name__ == '__main__':

    with open('DSN.txt', 'r') as file:
        i = 0
        for line in file:
            a = line.strip()
            if i == 0:
                driver = a
            if i == 1:
                login = a
            if i == 2:
                password = a
            if i == 3:
                name_db = a
            i += 1

    DSN = f"{driver}://{login}:{password}@localhost:5432/{name_db}"

    engine = sqlalchemy.create_engine(DSN)
    create_tables(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    file_name = "tests_data.json"
    base_path = os.getcwd()
    full_path = os.path.join(base_path, file_name)

    with open('tests_data.json', 'r') as fd:
        data = json.load(fd)

    for record in data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[record.get('model')]
        session.add(model(id=record.get('pk'), **record.get('fields')))
    session.commit()

    id_publish = input("Введите идентификатор издателя (либо нажмите ENTER для ввода имени издателя): ")

    if id_publish != "":
        for pub in session.query(Publisher).filter(Publisher.id == id_publish).all():
            print(pub)
    elif id_publish == "":
        name_publish = input("Введите имя издателя: ")
        for pub in session.query(Publisher).filter(Publisher.name.like(f'%{name_publish}%')).all():
            print(pub)


    session.close()
