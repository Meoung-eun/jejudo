import pymysql
import sys
import csv
from PyQt5.QtWidgets import *
from PyQt5 import uic

form_class = uic.loadUiType("jeju.ui")[0]  # ui연결

class MainWindow(QMainWindow, form_class): #화면을 띄우는데 사용되는 Class 선언
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.table_widget_create()


    def table_widget_create(self):
        conn = pymysql.connect(host='localhost', user='root', password='160072', db='jejudo', charset='utf8')

        # Connection 으로부터 Cursor 생성
        cur = conn.cursor()

        # SQL문 실행
        sql = "select * from jejudo.jeju_table"
        cur.execute(sql)

        # 데이타 Fetch
        row = cur.fetchone()
        rows = cur.fetchall()
        for i in range(len(rows)):
            for j in range(len(row)):
                self.table.setItem(i, j, QTableWidgetItem(rows[i][j]))
        print(len(rows))


        # Connection 닫기
        conn.close()




if __name__ == "__main__":
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    # WindowClass의 인스턴스 생성
    mainWindow = MainWindow()

    # 프로그램 화면을 보여주는 코드
    mainWindow.show()

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
