import unittest

from database import Database


class TestDatabase(unittest.TestCase):
    database = None

    @classmethod
    def setUpClass(cls):
        cls.database = Database(":memory:")
        cls.database.cursor.executescript("""
        BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Accounts" (
	"User_ID"	INTEGER,
	"Login"	TEXT NOT NULL UNIQUE,
	"E_mail"	TEXT NOT NULL UNIQUE,
	"Password"	TEXT NOT NULL,
	"Points"	INTEGER,
	"Address"	TEXT NOT NULL,
	"Date_of_registration"	TEXT,
	"Date_of_birth"	TEXT,
	PRIMARY KEY("User_ID" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Items" (
	"Item_ID"	INTEGER,
	"Category"	TEXT,
	"Name"	TEXT NOT NULL UNIQUE,
	"Price"	INTEGER NOT NULL,
	"Description"	TEXT,
	"Rating"	INTEGER,
	PRIMARY KEY("Item_ID" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Shopping_cart" (
	"Shopping_cart_ID"	INTEGER,
	"User_ID"	INTEGER NOT NULL,
	"Item_ID"	INTEGER NOT NULL,
	"Count_of_items"	INTEGER NOT NULL,
	"Status_of_item"	TEXT NOT NULL,
	PRIMARY KEY("Shopping_cart_ID" AUTOINCREMENT),
	FOREIGN KEY("Item_ID") REFERENCES "Items"("Item_ID"),
	FOREIGN KEY("User_ID") REFERENCES "Accounts"("User_ID")
);
INSERT INTO "Accounts" VALUES (1,'VK1580','1580@yandex.ru','123',0,'qwe','21.11.2021','2005-02-19');
INSERT INTO "Accounts" VALUES (2,'YLA','proger@gmail.com','YALAU',0,'asd','20.10.2021','2004-08-22');
INSERT INTO "Accounts" VALUES (3,'DL1375','TT@mail.ru','flower',0,'zxc','04.07.2021','2005-08-10');
INSERT INTO "Items" VALUES (1,'Basket','BWB',1500,NULL,NULL);
INSERT INTO "Items" VALUES (2,'Digit','BWD',3000,NULL,NULL);
INSERT INTO "Items" VALUES (3,'Animal','VOA',2500,NULL,NULL);
INSERT INTO "Items" VALUES (4,'Digit','For GR',1000,NULL,NULL);
INSERT INTO "Shopping_cart" VALUES (1,1,1,3,'In the shopping cart');
INSERT INTO "Shopping_cart" VALUES (2,2,2,3,'Ordered');
INSERT INTO "Shopping_cart" VALUES (3,3,3,1,'Delivered');
INSERT INTO "Shopping_cart" VALUES (4,1,4,2,'Ordered');""")
        cls.database.connection.commit()

    @classmethod
    def tearDownClass(cls):
        cls.database.close()

    def test_get_shopping_cart(self):
        result = self.database.get_shopping_cart()
        self.assertEqual(result, [('BWB', 3)])

    def test_get_all_items_from_category(self):
        result = self.database.get_all_items_from_category()
        self.assertEqual(result, [('BWD', 3000), ('For GR', 1000)])

    def test_get_users_birthday_boys(self):
        request1 = "SELECT (substr(date('now'), 6));"
        request2 = "SELECT substr(date_of_birth, 6) FROM Accounts"
        self.database.cursor.execute(request1)
        now_date = self.database.cursor.fetchall()[0][0]
        self.database.cursor.execute(request2)
        dates_of_birth = []
        for d in self.database.cursor.fetchall():
            dates_of_birth.append(d[0])
        col = 0
        for date in dates_of_birth:
            col += int(date == now_date)
        result1 = self.database.get_all_users_id_bd()
        result2 = self.database.get_all_users_e_mail_bd()
        self.assertEqual(len(result1), col)
        self.assertEqual(len(result2), col)


if __name__ == "__main__":
    unittest.main(failfast=False)
