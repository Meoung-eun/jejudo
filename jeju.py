import pymysql
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from jejuForm import Add

form_class = uic.loadUiType("jeju.ui")[0]  # ui연결

class MainWindow(QMainWindow, form_class): #화면을 띄우는데 사용되는 Class 선언
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.table_widget_create()
        self.btn_search.clicked.connect(self.search)



    def table_widget_create(self):
        ## sql파일 커넥트
        conn = pymysql.connect(host='localhost', user='root', password='0000', db='jejudo', charset='utf8')   # password 변경 해주세요
        ## conn로부터  결과를 얻어올 때 사용할 Cursor 생성
        cur = conn.cursor()
        ## SQL문 실행
        sql = "select * from jejudo.jeju_table"
        cur.execute(sql)
        print(cur.execute(sql))   # 실행(excute) 했더니 10884줄이 나온다.
        ## 데이타 Fetch
        # row = cur.fetchone()
        # print(row) # ('카페송키','일반음식점..) 한 행이 튜플형태로 나온다.
        rows = cur.fetchall()
        # print(rows) # 튜플안에 튜플로 전체 데이터를 불러온다.
        self.table.setRowCount(len(rows)) # 테이블의 행 갯수를 rows의 길이로 정함
        self.table.setColumnCount(len(rows[0]))  # 테이블의 열 갯수를 row의 길이로 정함

        for i in range(len(rows)):
            for j in range(len(rows[0])):
                self.table.setItem(i, j, QTableWidgetItem(str(rows[i][j])))
        # Connection 닫기
        conn.close()

    def search(self):
        self.table.clearContents()
        conn = pymysql.connect(host='localhost', user='root', password='0000', db='jejudo',
                               charset='utf8')
        cur = conn.cursor()
        data = self.lineEdit.text()
        data2 = f"%{data}%"
        sql = "SELECT * FROM jejudo.jeju_table WHERE full_address like %s"
        cur.execute(sql, data2)
        rows = cur.fetchall()
        self.table.setRowCount(len(rows)) # 테이블의 행 갯수를 rows의 길이로 정함
        self.table.setColumnCount(len(rows[0]))  # 테이블의 열 갯수를 row의 길이로 정함
        for i in range(len(rows)):
            for j in range(len(rows[i])):
                self.table.setItem(i, j, QTableWidgetItem(str(rows[i][j])))
        conn.commit()
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