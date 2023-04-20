from flask import Flask, render_template
import pandas as pd
import sqlite3


class ReadFromDB:
    def __init__(self):
        self.connection = sqlite3.connect('employees.db')
        self.cur = self.connection.cursor()

    def read_db(self):
        loaded_sql = pd.read_sql('SELECT id, firstname, lastname, age, date FROM employees', self.connection)
        l = loaded_sql.to_dict('records')

        return l


class SelfBrowser:
    def __init__(self, name):
        self.app = Flask(name)
        self.db = ReadFromDB()
        self.loaded_db = self.db.read_db()

        @self.app.route('/')
        @self.app.route('/home')
        def home():
            return render_template('index.html', l=self.loaded_db)

