import sqlite3 as sql


class Person:
    def __init__(self, user_ID, name, role):
        self.user_ID = user_ID
        self.name = name
        self.role = role

    def users_list(self):
        print("Users: ")
        conn = sql.connect("Resit.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM User")
        managers = cursor.fetchall()
        print("ID" + "\t" + "NAME")
        for manager in managers:
            print(str(manager[0]) + "\t" + manager[1])
        conn.commit()
        conn.close()

    def show_accounts_by_user(self, ide):
        print("Accounts of user: ")

        conn = sql.connect("Resit.db")
        cursor = conn.cursor()

        cursor.execute("SELECT Account.id, Account.account_type, U.name, M.name "
                       "FROM Account "
                       "INNER JOIN Manager M "
                       "ON M.id = Account.account_manager_id "
                       "INNER JOIN User U ON U.id = Account.account_owner_id "
                       "WHERE account_owner_id = (?) ", (str(ide)))
        accounts = cursor.fetchall()
        print("ID" + "\t" + "USER" + "\t" + "Manager Name" + "\t" + " TYPE")
        for acc in accounts:
            print(str(acc[0]) + "\t" + acc[2] + "\t" + str(acc[3]) + "\t\t" + acc[1])
        conn.commit()
        conn.close()

    def managers_list(self):
        print("Managers: ")
        conn = sql.connect("Resit.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Manager")
        managers = cursor.fetchall()
        print("ID" + "\t" + "NAME")
        for manager in managers:
            print(str(manager[0]) + "\t" + manager[1])
        conn.commit()
        conn.close()

    def show_accounts_by_mananger(self, ide):
        print("Accounts of manager: ")
        conn = sql.connect("Resit.db")
        cursor = conn.cursor()

        cursor.execute("SELECT Account.id, Account.account_type, U.name, M.name "
                       "FROM Account "
                       "INNER JOIN Manager M "
                       "ON M.id = Account.account_manager_id "
                       "INNER JOIN User U ON U.id = Account.account_owner_id "
                       "WHERE account_manager_id = (?) ", (str(ide)))

        accounts = cursor.fetchall()
        print("ID" + "\t" + "Manager Name" + "\t" + "USER" + "\t" + " TYPE")
        for acc in accounts:
            print(str(acc[0]) + "\t" + acc[3] + "\t\t" + str(acc[2]) + "\t" + acc[1])
        conn.commit()
        conn.close()


class Account:
    def __init__(self, account_ID, account_type, account_owner, account_manager):
        self.account_manager = account_manager
        self.account_owner = account_owner
        self.account_type = account_type
        self.account_ID = account_ID

    def delete_account_by_id(self, ide):
        conn = sql.connect("Resit.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Account WHERE id = (?)", str(ide))
        conn.commit()
        conn.close()
        print("Successfully deleted!")

    def show_account_types(self):
        print("Account types:")
        conn = sql.connect("Resit.db")
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT account_type FROM Account")
        typ = cursor.fetchall()
        for i, ty in enumerate(typ, start=1):
            print(f"{i}.", ty[0])
        conn.commit()
        conn.close()

    def add_account(self, ide):
        self.show_account_types()
        print("Choose account type, write type carefully!")
        typ = input("Type: ")
        Person.managers_list(self="MANAGER_LIST")
        print("Choose Manager_ID")
        m_id = int(input("ID: "))
        conn = sql.connect("Resit.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Account(account_type, account_owner_id, account_manager_id) VALUES(?,?,?)",
                       (typ, ide, m_id))
        conn.commit()
        conn.close()
        print("Account added!")

    def change_manager_of_account(self, ide):

        conn = sql.connect("Resit.db")
        cursor = conn.cursor()

        cursor.execute("SELECT account_manager_id FROM Account WHERE id = (?)", str(ide))
        current_manager_id = cursor.fetchone()[0]
        print("Current manager id:", current_manager_id)
        conn.commit()

        cursor.execute("SELECT * FROM Manager WHERE id NOT IN (?)", str(current_manager_id))
        mans = cursor.fetchall()
        print("\nFree Managers:")
        print("ID" + "\t" + "NAME")
        for managers in mans:
            print(str(managers[0]) + "\t" + managers[1])

        print("Choose a new manager ID")
        new_ide = int(input("ID: "))
        conn.commit()

        query = "UPDATE Account SET account_manager_id = (?) WHERE id = (?)"
        value = (f"{new_ide}", f"{ide}")
        cursor.execute(query, value)

        conn.commit()
        conn.close()
        print("MANAGER UPDATED!")

    def show_all_accounts(self):
        print("\nAll accounts: ")
        conn = sql.connect("Resit.db")
        cursor = conn.cursor()
        cursor.execute("SELECT Account.id, Account.account_type, M.name, "
                       "U.name, Account.account_owner_id, Account.account_manager_id "
                       "FROM Account "
                       "INNER JOIN Manager M "
                       "ON M.id = Account.account_manager_id "
                       "INNER JOIN User U "
                       "ON U.id = Account.account_owner_id")
        accounts = cursor.fetchall()
        print("ID" + "\t" + "MANAGER" + "\t\t" + "MANAGER_ID" + "\t\t" + "USER" + "\t" + "USER_ID" + "\t\t" + "TYPE")
        for account in accounts:
            print(str(account[0]) + "\t" + account[2] + "\t\t" + str(account[5]) + "\t\t\t" + account[3] + "\t\t" + str(account[4]) + "\t" + "\t" + account[1])
        conn.commit()
        conn.close()


def choice():
    print("\nWelcome to the bank account management app!")
    print("(1) See accounts by userID\n"
          "(2) See accounts by managerID\n"
          "(3) See account types\n"
          "(4) Add account by existing userID\n"
          "(5) Change manager of account by accountID\n"
          "(6) Close/Delete account by accountID\n"
          "(7) See all accounts\n"
          "(8) Exit")


def demo():
    while True:

        choice()
        ch = input("\nEnter a number: ")
        if ch == '1':
            user = Person('', '', '')
            user.users_list()
            print("Enter ID of User")
            idee = input("ID: ")
            user.show_accounts_by_user(idee)

        elif ch == '2':
            manager = Person('', '', '')
            manager.managers_list()
            print("Enter ID of Manager")
            ide = input("ID: ")
            manager.show_accounts_by_mananger(ide)

        elif ch == '3':
            ac = Account('', '', '', '')
            ac.show_account_types()

        elif ch == '4':
            ass = Person('', '', '')
            ass.users_list()
            adam = Account('', '', '', '')
            print("Enter a user ID to add account")
            bell = input("ID: ")
            adam.add_account(bell)

        elif ch == '5':
            acco = Account('', '', '', '')
            acco.show_all_accounts()
            print("Enter account ID, which you wanna edit")
            ggg = int(input('ID: '))
            acco.change_manager_of_account(ggg)

        elif ch == '6':
            dele = Account('', '', '', '')
            dele.show_all_accounts()
            print("Enter account ID to remove")
            iee = input('ID: ')
            dele.delete_account_by_id(iee)

        elif ch == '7':
            show_all = Account('', '', '', '')
            show_all.show_all_accounts()

        elif ch == '8':
            print("Exiting...")
            exit(0)
        else:
            print("Enter a number.!>!.")


if __name__ == '__main__':
    # db_init()
    demo()
