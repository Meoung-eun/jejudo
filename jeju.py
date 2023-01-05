import pymysql
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from jejuForm import Add
from PyQt5 import QtWidgets, QtCore
# from PyQt5.QtCore import Qt


form_class = uic.loadUiType("jeju.ui")[0]  # ui연결

class MainWindow(QMainWindow, form_class): #화면을 띄우는데 사용되는 Class 선언
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.jejuFormShow = Add()   # Add클래스를 self.jejuFormShow로 선언

        self.table_widget_create()  # 테이블위젯 안에 데이터 생성
        self.btn_search.clicked.connect(self.search)    # 검색 버튼
        self.btn_edit.clicked.connect(self.edit)        # 수정 버튼
        self.btn_add.clicked.connect(self.add)          # 추가 버튼



    def table_widget_create(self):
        self.checkboxList = []  # 체크박스 넣을 빈 리스트 만들기
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
        self.table.setColumnCount(len(rows[0])+1)  # 테이블의 열 갯수를 rows[0]의 길이로 정함

        # 데이터베이스 전체를 테이블에 넣어주는 반복문
        for i in range(len(rows)):
            for j in range(len(rows[0])):
                self.table.setItem(i, j, QTableWidgetItem(str(rows[i][j])))


        # 체크박스 리스트 데이터 갯수만큼 만들어줌
        for i in range(len(rows)):
            self.ckBox = QCheckBox()
            self.checkboxList.append(self.ckBox)
            self.ckBox.pressed.connect(self.changeTitle)

        # 테이블 위젯 마지막 열에 체크박스 넣어줄 반복문
        for i in range(len(rows)):
            # cellWidget = QWidget()
            # layoutCB = QHBoxLayout(cellWidget)
            # layoutCB.addWidget(self.checkboxList[i])
            # self.checkboxList[i].setAlignment(QtCore.Qt.self.AlignCenter)
            # layoutCB.setContentsMargins(0, 0, 0, 0)
            # cellWidget.setLayout(layoutCB)
            self.table.setCellWidget(i,16,self.checkboxList[i])

        # Connection 닫기
        conn.close()


    def changeTitle(self):
        checkbox = self.sender()
        print(checkbox)
        item = self.table.indexAt(checkbox.pos())
        print(item)
        print(self.table.item(item.row(),0).text())




    def search(self):
        self.table_widget_create()
        self.checkboxList = []  # 체크박스 넣을 빈 리스트 만들기
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
        self.table.setColumnCount(len(rows[0])+1)  # 테이블의 열 갯수를 rows[0]의 길이로 정함

        # 데이터베이스 전체를 테이블에 넣어주는 반복문
        for i in range(len(rows)):
            for j in range(len(rows[0])):
                self.table.setItem(i, j, QTableWidgetItem(str(rows[i][j])))


        # 체크박스 리스트 데이터 갯수만큼 만들어줌
        for i in range(len(rows)):
            ckBox = QCheckBox()
            self.checkboxList.append(ckBox)

        # 테이블 위젯 마지막 열에 체크박스 넣어줄 반복문
        for i in range(len(rows)):
            self.table.setCellWidget(i,16,self.checkboxList[i])

        # Connection 닫기
        conn.commit()
        conn.close()

    def edit(self):
        print('수정')
        self.jejuFormShow.show()    # 수정버튼 누르면 폼창이 뜬다.  구현 - 은희

    def checkFuction(self):
        print('123')



    def checkbox_change(self, checkvalue):
        chbox = self.sender()
        print("checkbox sender row = ", chbox.get_row())









    def add(self):
        print('추가')
        self.jejuFormShow.show()    # 추가버튼 누르면 폼창이 뜬다.  구현 - 명은









if __name__ == "__main__":
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    # WindowClass의 인스턴스 생성
    mainWindow = MainWindow()

    # 프로그램 화면을 보여주는 코드
    mainWindow.show()

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()