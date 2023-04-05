from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QGraphicsWidget
import sqlite3

class sqlController(object):



    def __init__(self):
        print("sql_controller: Init")

    def connect(self):
        self.conn = sqlite3.connect('drinks.db')

    def disconnect(self):
        self.conn.close()

    def creatTable(self):
        self.creat_Table = """
            CREATE TABLE IF NOT EXISTS drinks (
                Id INT,
                Name TEXT,
                Price INT,
                Dateand Time datetime,
                PRIMARY KEY (Id)
            )
        """

        self.result = self.conn.execute(self.creat_Table)

    def insert_data(self, Id, Name, Price, DateandTime):
        self.conn = sqlite3.connect('D:/NCKH/AppQt/Project/ArmGUI/controllers/drinks.db')
        insert_Data = """INSERT INTO drinks VALUES (?,?,?,?)"""
        self.conn.execute(insert_Data, (Id, Name, Price, DateandTime))
        self.conn.commit()

    def select_all(self):
        print("select_all called")
        self.conn = sqlite3.connect('D:/NCKH/AppQt/Project/ArmGUI/controllers/drinks.db')
        self.sql_select_all = """SELECT * FROM drinks"""
        self.result = self.conn.execute(self.sql_select_all)
        return  self.result

    def delete_data(self):
        print("delete_data called")
        self.conn = sqlite3.connect('D:/NCKH/AppQt/Project/ArmGUI/controllers/drinks.db')
        self.delete_Data = """DELETE FROM drinks"""
        self.conn.execute(self.delete_Data)
        self.conn.commit()



