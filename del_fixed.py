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
        self.jejuFormShow = Add()   # Add클래스를 self.jejuFormShow로 선언
        self.setupUi(self)
        self.table_widget_create()
        self.btn_search.clicked.connect(self.search)
        self.btn_edit.clicked.connect(self.edit)
        self.btn_del.clicked.connect(self.del_pressed)
        self.checkbox_clicked = False
        self.item_list = []




    def table_widget_create(self):
        self.checkboxList = []  # 체크박스 넣을 빈 리스트 만들기
        ## sql파일 커넥트
        conn = pymysql.connect(host='localhost', user='root', password='0000', db='jeju_project', charset='utf8')   # password 변경 해주세요
        ## conn로부터  결과를 얻어올 때 사용할 Cursor 생성
        cur = conn.cursor()
        ## SQL문 실행
        sql = "select * from jeju_project.jeju_table"
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
            self.ckBox.pressed.connect(self.get_checked)

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

    def get_checked(self): # 체크박스 클릭할 때마다 행 삭제
        self.checkbox_clicked = True

        checkbox = self.sender()
        print(checkbox)
        item = self.table.indexAt(checkbox.pos())
        print(item)
        self.checked_item = self.table.item(item.row(), 0).text()
        print(self.checked_item)

        print(self.checked_item, 'yesyesyes')


        # SQL문 실행
        # 검색창에 입력된 'pop_name'을 포함하는 행 삭제하는 기능

        if self.checked_item not in self.item_list:
            self.item_list.append(self.checked_item)
            print(self.item_list)
        else:
            self.item_list.remove(self.checked_item)
            print(self.item_list)





        # print(self.temp)
        # self.table.clearContents()
        # for i in range(len(self.temp)):
        #     for j in range(len(self.temp[i])):
        #
        # #         self.table.setItem(i, j, QTableWidgetItem(str(self.temp[i][j])))
        #
        # self.confu.commit()
        # self.confu.close()

    def del_pressed(self):
        if self.checkbox_clicked == True:
        #     checkbox = self.sender()
        #     print(checkbox)
        #     item = self.table.indexAt(checkbox.pos())
        #     print(item)
        #     self.checked_item = self.table.item(item.row(), 0).text()
        #     print(self.checked_item)
        #
        #     print(self.checked_item, 'yesyesyes')
        #     pop_name = self.lineEdit.text()
        #
        #     self.confu = pymysql.connect(host='localhost', user='root', password='0000', db='jeju_project',
        #                            charset='utf8')
        #     curr = self.confu.cursor()
        #     print(pop_name)
        #     # SQL문 실행
        #     # 검색창에 입력된 'pop_name'을 포함하는 행 삭제하는 기능
        #     curr.execute(f"DELETE FROM jeju_project.jeju_table WHERE Restaurant_name = '{self.checked_item}'")
        #     curr.execute("select * from jeju_project.jeju_table")
        #     self.temp = curr.fetchall()
        #     self.confu.commit()
        #     # print(self.temp)
        #     self.table.clearContents()

        #
        #     self.confu.commit()
        #     self.confu.close()
        # else:
        #     print('wrong')
        #     QtWidgets.QMessageBox.information(self, "QMessageBox", "체크박스를 클릭해 주세요")
        # print(self.item_list)
            self.confu = pymysql.connect(host='localhost', user='root', password='0000', db='jeju_project',
                                         charset='utf8')
            curr = self.confu.cursor()
            for item in self.item_list:
                curr.execute(f"DELETE FROM jeju_project.jeju_table WHERE Restaurant_name = '{item}'")
            curr.execute("select * from jeju_project.jeju_table")
            self.temp = curr.fetchall()
            self.confu.commit()

            for i in range(len(self.temp)):
                for j in range(len(self.temp[i])):

                    self.table.setItem(i, j, QTableWidgetItem(str(self.temp[i][j])))


    def search(self):
        self.table_widget_create()
        self.checkboxList = []  # 체크박스 넣을 빈 리스트 만들기
        self.table.clearContents()
        conn = pymysql.connect(host='localhost', user='root', password='0000', db='jeju_project',
                               charset='utf8')
        cur = conn.cursor()
        data = self.lineEdit.text()
        data2 = f"%{data}%"
        sql = "SELECT * FROM jeju_project.jeju_table WHERE full_address like %s"
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
        print(self.checkboxList, 'ckBox')



        # 테이블 위젯 마지막 열에 체크박스 넣어줄 반복문
        for i in range(len(rows)):
            self.table.setCellWidget(i,16,self.checkboxList[i])

        # Connection 닫기
        conn.commit()
        conn.close()

    def edit(self): # 수정버튼 눌렀을 때 실행되는 메서드
        print('수정')
        self.checked_item
        self.jejuFormShow.show()    # 수정버튼 누르면 폼창이 뜬다.  구현 - 은희


    def pop(self):
        print(self.checked_item, 'yesyesyes')
        pop_name = self.lineEdit.text()

        self.confu = pymysql.connect(host='localhost', user='root', password='0000', db='jeju_project',
                               charset='utf8')
        curr = self.confu.cursor()
        print(pop_name)
        # SQL문 실행
        # 검색창에 입력된 'pop_name'을 포함하는 행 삭제하는 기능
        curr.execute(f"DELETE FROM jeju_project.jeju_table WHERE Restaurant_name = '{self.checked_item}'")
        curr.execute("select * from jeju_project.jeju_table")
        self.temp = curr.fetchall()
        self.confu.commit()
        # print(self.temp)
        self.table.clearContents()
        for i in range(len(self.temp)):
            for j in range(len(self.temp[i])):

                self.table.setItem(i, j, QTableWidgetItem(str(self.temp[i][j])))

        self.confu.commit()
        self.confu.close()










if __name__ == "__main__":
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    # WindowClass의 인스턴스 생성
    mainWindow = MainWindow()

    # 프로그램 화면을 보여주는 코드
    mainWindow.show()

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
