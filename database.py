import sqlite3

class Database:

    def __init__(self, path):
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()

    def close(self):
        self.connection.close()

    def get_all_users_id_bd(self):
        request = "SELECT User_ID FROM Accounts WHERE substr(Date_of_birth, 6) == (substr(date('now'), 6));"
        result = self.cursor.execute(request)
        return result.fetchall()

    def get_all_users_e_mail_bd(self):
        request = "SELECT E_mail FROM Accounts WHERE substr(Date_of_birth, 6) == (substr(date('now'), 6));"
        result = self.cursor.execute(request)
        return result.fetchall()

    def get_shopping_cart(self):
        request = 'SELECT (SELECT Items.Name FROM Items WHERE Items.Item_ID = Shopping_cart.Item_ID) AS Item_name, Count_of_items FROM Shopping_cart WHERE User_ID = 1 AND Status_of_item = "In the shopping cart";'
        result = self.cursor.execute(request)
        return result.fetchall()

    def get_all_items_from_category(self):
        request = 'SELECT Name, Price FROM Items WHERE Category = "Digit";'
        result = self.cursor.execute(request)
        return result.fetchall()