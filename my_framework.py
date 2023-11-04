import sqlite3


class Model:
    def __init__(self, db_connection):
        self.db = db_connection

    def get(self, table, key):
        cursor = self.db.cursor()
        cursor.execute(f"SELECT value FROM {table} WHERE key = ?", (key,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return result[0]
        return None

    def set(self, table, key, value):
        cursor = self.db.cursor()
        cursor.execute(
            f"INSERT OR REPLACE INTO {table} (key, value) VALUES (?, ?)", (key, value))
        self.db.commit()
        cursor.close()


class View:
    def show(self, data):
        print(data)


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def process_request(self, request):
        if request == 'get':
            table = input("Enter table: ")
            key = input("Enter key: ")
            value = self.model.get(table, key)
            self.view.show(value)
        elif request == 'set':
            table = input("Enter table: ")
            key = input("Enter key: ")
            value = input("Enter value: ")
            self.model.set(table, key, value)
        else:
            self.view.show("Invalid command")


class Application:
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.model = None
        self.view = None
        self.controller = None

    def set_model(self, model):
        self.model = model

    def set_view(self, view):
        self.view = view

    def set_controller(self, controller):
        self.controller = controller

    def run(self):
        while True:
            request = input(
                "Enter a command (e.g., 'get', 'set', or 'quit'): ")
            if request == 'quit':
                break
            self.controller.process_request(request)

# Database handling


class DatabaseModel(Model):
    def __init__(self, db_connection, table):
        super().__init__(db_connection)
        self.table = table


def create_database_table(db_connection, table):
    cursor = db_connection.cursor()
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS {table} (
                        key TEXT PRIMARY KEY,
                        value TEXT
                      )''')
    db_connection.commit()
    cursor.close()


# Example usage
if __name__ == '__main__':
    db_connection = sqlite3.connect("my_framework.db")
    create_database_table(db_connection, "data")

    app = Application(db_connection)
    db_model = DatabaseModel(db_connection, "data")
    app.set_model(db_model)
    app.set_view(View())
    controller = Controller(app.model, app.view)
    app.set_controller(controller)

    app.run()
