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
        self.checkboxList = []  # 체크박스 넣을 빈 리스트 만들기

        self.setupUi(self)
        self.jejuFormShow = Add()   # Add클래스를 self.jejuFormShow로 선언

        self.table_widget_create()  # 테이블 안에 데이터 생성
        self.btn_search.clicked.connect(self.search)    # 검색 버튼
        self.btn_edit.clicked.connect(self.edit)        # 수정 버튼
        self.btn_add.clicked.connect(self.add)          # 추가 버튼
        self.jejuFormShow.btn_save.clicked.connect(self.editSave) # jeju폼 안에 있는 저장버튼
        self.btn_del.clicked.connect(self.del_pressed)  # 삭제 버튼
        self.checkbox_clicked = False   # 체크박스 클릭 안했을 때




    def table_widget_create(self):  # 테이블 안에 데이터 생성
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

        self.rows = cur.fetchall()
        # print(self.rows) # 튜플안에 튜플로 전체 데이터를 불러온다.
        self.table.setRowCount(len(self.rows)) # 테이블의 행 갯수를 self.rows의 길이로 정함
        self.table.setColumnCount(len(self.rows[0])+1)  # 테이블의 열 갯수를 self.rows[0]의 길이로 정함

        # 데이터베이스 전체를 테이블에 넣어주는 반복문
        for i in range(len(self.rows)):
            for j in range(len(self.rows[i])):
                self.table.setItem(i, j, QTableWidgetItem(str(self.rows[i][j])))


        # 체크박스 리스트 데이터 갯수만큼 만들어줌
        for i in range(len(self.rows)):
            self.ckBox = QCheckBox()
            self.checkboxList.append(self.ckBox)
            self.ckBox.pressed.connect(self.get_checked)    # 체크박스를 누를 때마다 실행되는 매서드


        # 테이블 위젯 마지막 열에 체크박스 넣어줄 반복문
        for i in range(len(self.rows)):
            # cellWidget = QWidget()
            # layoutCB = QHBoxLayout(cellWidget)
            # layoutCB.addWidget(self.checkboxList[i])
            # self.checkboxList[i].setAlignment(QtCore.Qt.self.AlignCenter)
            # layoutCB.setContentsMargins(0, 0, 0, 0)
            # cellWidget.setLayout(layoutCB)
            self.table.setCellWidget(i,16,self.checkboxList[i])
        # Connection 닫기
        conn.close()




    def get_checked(self): # 체크박스를 누를 때마다 실행되는 매서드
        self.checkbox_clicked = True
        self.editli = []
        checkbox = self.sender()
        print(checkbox)
        item = self.table.indexAt(checkbox.pos())
        print(item)
        for i in range(len(self.rows[0])):
            self.editli.append(self.table.item(item.row(), i).text())
        print(self.editli)




    def search(self):
        self.table.clearContents()
        self.checkboxList = []  # 체크박스 넣을 빈 리스트 만들기

        conn = pymysql.connect(host='localhost', user='root', password='0000', db='jejudo',
                               charset='utf8')
        cur = conn.cursor()
        data = self.lineEdit.text()
        data2 = f"%{data}%"
        sql = f"SELECT * FROM jejudo.jeju_table WHERE Restaurant_name LIKE '{data2}' or full_address LIKE '{data2}' \
              or full_address_new LIKE '{data2}'"
        cur.execute(sql)

        self.rows = cur.fetchall()
        if len(self.rows) > 0:
            self.table.setRowCount(len(self.rows)) # 테이블의 행 갯수를 self.rows의 길이로 정함
            self.table.setColumnCount(len(self.rows[0])+1)  # 테이블의 열 갯수를 self.rows[0]의 길이로 정함
            # 데이터베이스 전체를 테이블에 넣어주는 반복문
            for i in range(len(self.rows)):
                for j in range(len(self.rows[0])):
                    self.table.setItem(i, j, QTableWidgetItem(str(self.rows[i][j])))
            # 체크박스 리스트 데이터 갯수만큼 만들어줌
            for i in range(len(self.rows)):
                ckBox = QCheckBox()
                self.checkboxList.append(ckBox)
                ckBox.pressed.connect(self.get_checked)    # 체크박스를 누를 때마다 실행되는 매서드
            # 테이블 위젯 마지막 열에 체크박스 넣어줄 반복문
            for i in range(len(self.rows)):
                self.table.setCellWidget(i,16,self.checkboxList[i])
            # Connection 닫기
            conn.commit()
            conn.close()

        else:
            print('wrong')
            QtWidgets.QMessageBox.information(self, "QMessageBox", "검색결과가 없습니다.")








    def edit(self):
        self.search()
        self.jejuFormShow.show()    # 수정버튼 누르면 폼창이 뜬다.  구현 - 은희
        print('수정')
        print(f'사업장명 = \'{self.editli[0]}\', full_address = \'{self.editli[12]}\' 에 해당되는 데이터가 수정됩니다.')



    def editSave(self): # jeju폼 안에 있는 저장버튼
        self.rs_name = self.jejuFormShow.Restaurant_name.text()
        self.bs_typeA = self.jejuFormShow.Business_typeA.text()
        self.bs_typeB = self.jejuFormShow.Business_typeB.text()
        self.auth_date = self.jejuFormShow.Authorized_date.text()
        self.cel_date = self.jejuFormShow.Cancel_date.text()
        self.State = self.jejuFormShow.State.text()
        self.st_detail = self.jejuFormShow.state_detail.text()
        self.clo_date = self.jejuFormShow.closing_date.text()
        self.vac_start_date = self.jejuFormShow.vacation_start_date.text()
        self.vac_end_date = self.jejuFormShow.vacation_end_date.text()
        self.rest_date = self.jejuFormShow.restarting_date.text()
        self.regi_square = self.jejuFormShow.region_square.text()
        self.fu_address = self.jejuFormShow.full_address.text()
        self.fu_address_new = self.jejuFormShow.full_address_new.text()
        self.po = self.jejuFormShow.post.text()
        self.upda_date = self.jejuFormShow.updated_date.text()


        print(f'사업장명 = \'{self.editli[0]}\', 전체주소 = \'{self.editli[12]}\' 에 해당되는 데이터 수정 완료.')
        #######################################################################################################
        conn = pymysql.connect(host='localhost', user='root', password='0000', db='jejudo', charset='utf8')
        cur = conn.cursor()
        # # SQL문 실행
        # cur.execute(f"UPDATE jejudo.jeju_table SET Restaurant_name = '{self.rs_name}', Business_typeA = '{self.bs_typeA}'\
        #             , Business_typeB = '{self.bs_typeB}', Authorized_date = '{self.auth_date}', Cancel_date = '{self.cel_date}'\
        #             , State = '{self.State}', state_detail = '{self.st_detail}', closing_date = '{self.clo_date}'\
        #             , vacation_start_date = '{self.vac_start_date}', vacation_end_date = '{self.vac_end_date}', restarting_date = '{self.rest_date}'\
        #             , region_square = '{self.regi_square}', full_address = '{self.fu_address}', full_address_new = '{self.fu_address_new}'\
        #             , post = '{self.po}', updated_date = '{self.upda_date}'\
        #             WHERE full_address = '{self.editli[12]}'")
        # SQL문 실행
        cur.execute(f"UPDATE jejudo.jeju_table SET Restaurant_name = '{self.rs_name}', Business_typeA = '{self.bs_typeA}', Business_typeB = '{self.bs_typeB}', Authorized_date = '{self.auth_date}'\
                    WHERE full_address = '{self.editli[12]}'")
        cur.execute("select * from jejudo.jeju_table")

        # 데이터를 sql에 반영
        conn.commit()
        # Connection 닫기
        conn.close()
        # 테이블 헤더를 제외한 데이터 삭제
        self.table.clearContents()
        # 테이블 안에 데이터 생성
        self.table_widget_create()















    def add(self):
        print('추가')
        self.jejuFormShow.show()    # 추가버튼 누르면 폼창이 뜬다.  구현 - 명은


    def del_pressed(self):
        if self.checkbox_clicked == True:
            print(self.editli, '\n삭제?')

            self.conn = pymysql.connect(host='localhost', user='root', password='0000', db='jejudo',
                                   charset='utf8')
            cur = self.conn.cursor()

            # SQL문 실행
            # 체크박스로 선택한것에 해당되는 "소재지 전체주소"가 포함 하는 행 삭제하는 기능
            cur.execute(f"DELETE FROM jejudo.jeju_table WHERE full_address = '{self.editli[12]}'")
            cur.execute("select * from jejudo.jeju_table")

            # 데이터를 sql에 반영
            self.conn.commit()
            # # Connection 닫기
            self.conn.close()
            # # 테이블 헤더를 제외한 데이터 삭제
            self.table.clearContents()
            self.table_widget_create()

        else:
            print('wrong')
            QtWidgets.QMessageBox.information(self, "QMessageBox", "체크박스를 클릭해 주세요")







if __name__ == "__main__":
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    # WindowClass의 인스턴스 생성
    mainWindow = MainWindow()

    # 프로그램 화면을 보여주는 코드
    mainWindow.show()

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()