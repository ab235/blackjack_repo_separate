import csv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
class User:
    def __init__(self, username = '', password = '', money = 0):
        self.username = username
        self.password = password
        self.money = money

    def __str__(self):
        return '{}: ${}'.format(self.username, self.money)
    def __repr__(self):
        return '{}: ${}'.format(self.username, self.money)

    def save_db(self, db):
        data = User.read_file(db)
        data.append([self.username, self.password, self.money])
        with open(db, 'w', newline = '') as file:
            csv_writer = csv.writer(file, delimiter = ',')
            for row in data:
                csv_writer.writerow(row)
    def update(self, db):
        data = User.read_file(db)
        with open(db, 'w') as file:
            csv_writer = csv.writer(file, delimiter = ",")
            for i in range(len(data)):
                if (data[i][0]==self.username):
                    data[i] = [self.username, self.password, self.money]
            for row in data:
                csv_writer.writerow(row)

    @staticmethod
    def get_user(username, db):
        with open(db, 'r') as file:
            csv_reader = csv.reader(file, delimiter = ',')
            for row in csv_reader:
                if (row[0]==username):
                    return User(row[0], row[1], row[2])
                
        return False
    @staticmethod
    def read_file(db):
        data = []
        with open(db) as file:
            csv_reader = csv.reader(file, delimiter = ',')
            for row in csv_reader:
                data.append(row)
        return data