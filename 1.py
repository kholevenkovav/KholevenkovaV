import sqlite3

conn = sqlite3.connect('testdb.db')

cursor = conn.cursor()

cursor.execute("SELECT User_ID FROM Accounts WHERE substr(Date_of_birth, 6) == (substr(date('now'), 6));")
print(cursor.fetchall())

cursor.execute("SELECT E_mail FROM Accounts WHERE substr(Date_of_birth, 6) == (substr(date('now'), 6));")
print(cursor.fetchall())

cursor.execute("SELECT (SELECT Items.Name FROM Items WHERE Items.Item_ID = Shopping_cart.Item_ID) AS Item_name, Count_of_items FROM Shopping_cart WHERE User_ID = 1 AND Status_of_item = 'In the shopping cart';")
print(cursor.fetchall())

cursor.execute("SELECT Name, Price FROM Items WHERE Category = 'Digit';")
print(cursor.fetchall())

conn.close()
