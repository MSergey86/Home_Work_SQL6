import os
import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Shop, Book, Stock, Sale


if __name__ == '__main__':

    with open('DSN.json', 'r', encoding='utf-8') as file:
        data = file.read()
        js = json.loads(data)
        driver = js["driver"]
        login = js["login"]
        password = js["password"]
        name_db = js["name_db"]

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

    for book in session.query(Book).join(Stock.book).filter(Book.id_publisher == id_publish).all():
        for p in session.query(Stock).filter(Stock.id_book == book.id).all():
            for name_shop in session.query(Shop).filter(Shop.id == p.id_shop).all():
                print(name_shop.name)


    session.close()
