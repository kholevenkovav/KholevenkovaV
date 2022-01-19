import create_db_struct as database
import datetime

acc_1 = database.Accounts(login="VK1580", e_mail="1580@yandex.ru", password="123", points=0, address="qwe",
                       date_of_registration=datetime.datetime.now())
acc_2 = database.Accounts(login="YLA", e_mail="proger@gmail.com", password="YALAU", points=0, address="asd",
                       date_of_registration=datetime.datetime.now())
acc_3 = database.Accounts(login="DL1375", e_mail="TT@mail.ru", password="flower", points=0, address="zxc",
                       date_of_registration=datetime.datetime.now())

database.database.session.add(acc_1)
database.database.session.add(acc_2)
database.database.session.add(acc_3)
database.database.session.commit()

print(database.Accounts.query.all())