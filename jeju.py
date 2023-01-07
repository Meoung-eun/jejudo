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

        self.checkboxList = []  # 체크박스 넣을 빈 리스트 만들기
        self.item_list = []     # 체크한 해당 데이터가 들어갈 리스트

        #### 실행 매서드 ###
        # self.table_widget_create()  # 테이블 안에 데이터 생성
        self.search() # 테이블 안에 데이터 생성
        self.btn_search.clicked.connect(self.search)    # 검색 버튼
        self.btn_edit.clicked.connect(self.edit)        # 수정 버튼
        self.btn_add.clicked.connect(self.add)          # 추가 버튼
        self.jejuFormShow.btn_save.clicked.connect(self.editSave) # jeju폼 안에 있는 수정-저장버튼
        self.btn_del.clicked.connect(self.del_pressed)  # 삭제 버튼
        # self.jejuFormShow.btn_save.clicked.connect(self.addSave) # jeju폼 안에 있는 추가-저장버튼 # 터진다!!!!!!









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
        # self.row = cur.fetchone()
        # print(row) # ('카페송키','일반음식점..) 한 행이 튜플형태로 나온다.
        self.rows = cur.fetchall()
        # print(self.rows) # 튜플안에 튜플로 전체 데이터를 불러온다.

        self.table.setRowCount(len(self.rows)) # 테이블의 행 갯수를 self.rows의 길이로 정함
        self.table.setColumnCount(len(self.rows[0])+1)  # 테이블의 열 갯수를 self.rows[0]의 길이로 정함
        # 테이블 column명 지정 하기
        self.table.setHorizontalHeaderLabels(['', '사업장명', '업종구분대분류', '업종구분소분류', '인허가일자'
                                                 , '인허가취소일자', '영업상태명', '상세영업상태명', '폐업일자'
                                                 , '휴업시작일자', '휴업종료일자', '재개업일자', '소재지면적'
                                                 , '소재지전체주소', '도로명전체주소', '도로명우편번호', '데이터갱신일자'])

        # 데이터베이스 전체를 테이블에 넣어주는 반복문
        for i in range(len(self.rows)):
            for j in range(len(self.rows[i])):
                self.table.setItem(i, j+1, QTableWidgetItem(str(self.rows[i][j])))


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
            self.table.setCellWidget(i,0,self.checkboxList[i])
        # Connection 닫기
        conn.close()




    def get_checked(self): # 체크박스를 누를 때마다 실행되는 매서드
        self.checkbox_clicked = True
        self.checked_list = []
        checkbox = self.sender()
        print(checkbox)
        item = self.table.indexAt(checkbox.pos())
        print(item)
        for i in range(len(self.rows[0])):
            self.checked_list.append(self.table.item(item.row(), i+1).text())
        print(self.checked_list)

        if self.checked_list not in self.item_list:
            self.item_list.append(self.checked_list)
            print(self.item_list)
        else:
            self.item_list.remove(self.checked_list)
            print('체크해제')
            print(self.item_list)


    def search(self):
        self.table.clearContents()
        self.checkboxList = []  # 체크박스 넣을 빈 리스트 만들기

        conn = pymysql.connect(host='localhost', user='root', password='0000', db='jejudo',
                               charset='utf8')
        ## conn로부터  결과를 얻어올 때 사용할 Cursor 생성
        cur = conn.cursor()
        ## SQL문 실행
        data = self.lineEdit.text()
        data2 = f"%{data}%"
        sql = f"SELECT * FROM jejudo.jeju_table WHERE Restaurant_name LIKE '{data2}' or full_address LIKE '{data2}' \
              or full_address_new LIKE '{data2}'"
        cur.execute(sql)
        ## 데이타 Fetch
        # self.row = cur.fetchone()
        self.rows = cur.fetchall() # 실행(excute) 했더니 10884줄이 나온다.
        print(self.rows[0])


        if len(self.rows) > 0:
            self.table.setRowCount(len(self.rows)) # 테이블의 행 갯수를 self.rows의 길이로 정함
            self.table.setColumnCount(len(self.rows[0])+1)  # 테이블의 열 갯수를 self.rows[0]의 길이로 정함
            # 테이블 column명 지정 하기
            self.table.setHorizontalHeaderLabels(['', '사업장명', '업종구분대분류', '업종구분소분류', '인허가일자'
                                                     , '인허가취소일자', '영업상태명', '상세영업상태명', '폐업일자'
                                                     , '휴업시작일자', '휴업종료일자', '재개업일자', '소재지면적'
                                                     , '소재지전체주소', '도로명전체주소', '도로명우편번호', '데이터갱신일자'])

            # 데이터베이스 전체를 테이블에 넣어주는 반복문
            for i in range(len(self.rows)):
                for j in range(len(self.rows[0])):
                    self.table.setItem(i, j+1, QTableWidgetItem(str(self.rows[i][j])))
            # 체크박스 리스트 데이터 갯수만큼 만들어줌
            for i in range(len(self.rows)):
                ckBox = QCheckBox()
                self.checkboxList.append(ckBox)
                ckBox.pressed.connect(self.get_checked)    # 체크박스를 누를 때마다 실행되는 매서드
            # 테이블 위젯 첫번째 열에 체크박스 넣어줄 반복문
            for i in range(len(self.rows)):
                self.table.setCellWidget(i,0,self.checkboxList[i])
            # Connection 닫기
            conn.commit()
            conn.close()
            self.item_list.clear()
            print(self.item_list)

        else:
            self.table.setHorizontalHeaderLabels(['', '사업장명', '업종구분대분류', '업종구분소분류', '인허가일자'
                                                     , '인허가취소일자', '영업상태명', '상세영업상태명', '폐업일자'
                                                     , '휴업시작일자', '휴업종료일자', '재개업일자', '소재지면적'
                                                     , '소재지전체주소', '도로명전체주소', '도로명우편번호', '데이터갱신일자'])
            print('wrong')
            QtWidgets.QMessageBox.information(self, "QMessageBox", "검색결과가 없습니다.")

            self.lineEdit.clear()
            self.item_list.clear()
            print(self.item_list)









    def edit(self): # 수정 버튼 누를 때 매소드
        self.rs_name = self.jejuFormShow.Restaurant_name
        self.bs_typeA = self.jejuFormShow.Business_typeA
        self.bs_typeB = self.jejuFormShow.Business_typeB
        self.auth_date = self.jejuFormShow.Authorized_date
        self.cel_date = self.jejuFormShow.Cancel_date
        self.State = self.jejuFormShow.State
        self.st_detail = self.jejuFormShow.state_detail
        self.clo_date = self.jejuFormShow.closing_date
        self.vac_start_date = self.jejuFormShow.vacation_start_date
        self.vac_end_date = self.jejuFormShow.vacation_end_date
        self.rest_date = self.jejuFormShow.restarting_date
        self.regi_square = self.jejuFormShow.region_square
        self.fu_address = self.jejuFormShow.full_address
        self.fu_address_new = self.jejuFormShow.full_address_new
        self.po = self.jejuFormShow.post
        self.upda_date = self.jejuFormShow.updated_date
        self.lineEditli = [self.rs_name, self.bs_typeA, self.bs_typeB, self.auth_date, self.cel_date, self.State
            , self.st_detail, self.clo_date, self.vac_start_date, self.vac_end_date, self.rest_date
            , self.regi_square, self.fu_address, self.fu_address_new, self.po, self.upda_date]

        if len(self.item_list) == 1:     # 아이템 리스트의 길이가 1개 일 때 수정 할 수 있는 것 구현
            self.jejuFormShow.show()    # 수정버튼 누르면 폼창이 뜬다.  구현 - 은희
            print('수정')
            print(f'사업장명 = \'{self.checked_list[0]}\', full_address = \'{self.checked_list[12]}\' 에 해당되는 데이터가 수정됩니다.')
            for i in range(len(self.lineEditli)):
                self.lineEditli[i].setText(self.checked_list[i])

        elif len(self.item_list) < 1:   # 아이템 리스트의 길이가 1개 미만(0개)일 때 수정을 막는 것 구현
            print('wrong')
            option = QtWidgets.QMessageBox.information(self, "QMessageBox", "체크박스를 선택 해 주세요",
                                          QtWidgets.QMessageBox.Ok )

        elif len(self.item_list) >= 2:     # 아이템 리스트의 길이가 2개 이상일 때 수정을 막는 것 구현
            print('wrong')
            QtWidgets.QMessageBox.information(self, "QMessageBox", "한개만 선택 해 주세요")
            self.search()





    def editSave(self): # 수정 후 jeju폼 안에 있는 저장버튼
        print(f'사업장명 = \'{self.checked_list[0]}\', 전체주소 = \'{self.checked_list[12]}\' 에 해당되는 데이터 수정 완료.')
        #######################################################################################################
        conn = pymysql.connect(host='localhost', user='root', password='0000', db='jejudo', charset='utf8')
        cur = conn.cursor()
        # SQL문 실행
        if len(self.item_list) == 1:     # 아이템 리스트의 길이가 1개 일 때 수정 할 수 있는 것 구현
            for item in self.item_list:  # itemlist[item] 은 itemlist 0번째 요소부터~
                cur.execute(f"UPDATE jejudo.jeju_table SET \
                            Restaurant_name = '{self.rs_name.text()}', Business_typeA = '{self.bs_typeA.text()}', \
                            Business_typeB = '{self.bs_typeB.text()}', Authorized_date = '{self.auth_date.text()}',\
                            Cancel_date = '{self.cel_date.text()}', State = '{self.State.text()}',\
                            state_detail = '{self.st_detail.text()}', closing_date = '{self.clo_date.text()}',\
                            vacation_start_date = '{self.vac_start_date.text()}', vacation_end_date = '{self.vac_end_date.text()}',\
                            restarting_date = '{self.rest_date.text()}', region_square = '{self.regi_square.text()}',\
                            full_address = '{self.fu_address.text()}', full_address_new = '{self.fu_address_new.text()}',\
                            post = '{self.po.text()}', updated_date = '{self.upda_date.text()}'\
                            WHERE full_address = '{item[12]}'")
        cur.execute("select * from jejudo.jeju_table")

        # 데이터를 sql에 반영
        conn.commit()
        # Connection 닫기
        conn.close()
        # 테이블 헤더를 제외한 데이터 삭제
        self.table.clearContents()
        # 테이블 안에 데이터 생성
        self.table_widget_create()
        # self.search()
        self.item_list.clear()


    def add(self):
        print('추가')
        self.jejuFormShow.show()    # 추가버튼 누르면 폼창이 뜬다.  구현 - 명은



    def addSave(self):
        print("hello")
        conn = pymysql.connect(host='localhost', user='root', password='0000', db='jejudo', charset='utf8')
        cur = conn.cursor()
        # # SQL문 실행
        # cur.execute(f"INSERT INTO jejudo.jeju_table (Restaurant_name, Business_typeA, Business_typeB,\
        #              Authorized_date, Cancel_date, State, state_detail, closing_date, vacation_start_date,\
        #             vacation_end_date, restarting_date, region_square, full_address, full_address_new,\
        #             post, updated_date )\
        #             VALUES ('{self.rs_name.text()}', '{self.bs_typeA.text()}', '{self.bs_typeB.text()}',\
        #                     '{self.auth_date.text()}', '{self.cel_date.text()}', '{self.State.text()}'\
        #                      , '{self.st_detail.text()}', '{self.clo_date.text()}', '{self.vac_start_date.text()}'\
        #                      , '{self.vac_end_date.text()}', '{self.rest_date.text()}', '{self.regi_square.text()}'\
        #                      , '{self.fu_address.text()}', '{self.fu_address_new.text()}', '{self.po.text()}'\
        #                      , '{self.upda_date.text()}')")
        # SQL문 실행
        cur.execute(f"INSERT INTO jejudo.jeju_table \
                            VALUES ('{self.rs_name.text()}', '{self.bs_typeA.text()}', '{self.bs_typeB.text()}',\
                                    '{self.auth_date.text()}', '{self.cel_date.text()}', '{self.State.text()}'\
                                     , '{self.st_detail.text()}', '{self.clo_date.text()}', '{self.vac_start_date.text()}'\
                                     , '{self.vac_end_date.text()}', '{self.rest_date.text()}', '{self.regi_square.text()}'\
                                     , '{self.fu_address.text()}', '{self.fu_address_new.text()}', '{self.po.text()}'\
                                     , '{self.upda_date.text()}')")
        # cur.execute("update jeju_table set jeju_table.Restaurant_name = " " where jeju_table.Restaurant_name is NULL")
        # cur.execute("update jeju_table set jeju_table.Business_typeA = " " where jeju_table.Business_typeA is NULL")
        # cur.execute("update jeju_table set jeju_table.Business_typeB = " " where jeju_table.Business_typeB is NULL")
        # cur.execute("update jeju_table set jeju_table.Authorized_date = " " where jeju_table.Authorized_date is NULL")
        # cur.execute("update jeju_table set jeju_table.Cancel_date = " " where jeju_table.Cancel_date is NULL")
        # cur.execute("update jeju_table set jeju_table.state = " " where jeju_table.state is NULL")
        # cur.execute("update jeju_table set jeju_table.state_detail = " " where jeju_table.state_detail is NULL")
        # cur.execute("update jeju_table set jeju_table.closing_date = " " where jeju_table.closing_date is NULL")
        # cur.execute("update jeju_table set jeju_table.vacation_start_date = " " where jeju_table.vacation_start_date is NULL")  #
        # cur.execute("update jeju_table set jeju_table.vacation_end_date = " " where jeju_table.vacation_end_date is NULL")
        # cur.execute("update jeju_table set jeju_table.restarting_date = " " where jeju_table.restarting_date is NULL")
        # cur.execute("update jeju_table set jeju_table.region_square = " " where jeju_table.region_square is NULL")
        # cur.execute("update jeju_table set jeju_table.full_address = " " where jeju_table.full_address is NULL")

        # cur.execute(WHERE IS NULL(f"UPDATE SET jejudo.jeju_table(Restaurant_name, Business_typeA, Business_typeB, Authorized_date ) VALUES ('{self.rs_name}', '{self.bs_typeA}', '{self.bs_typeB}', '{self.auth_date}'))
        cur.execute("select * from jejudo.jeju_table")

        # 데이터를 sql에 반영
        conn.commit()
        # Connection 닫기
        conn.close()
        # 테이블 헤더를 제외한 데이터 삭제
        self.table.clearContents()
        # 테이블 안에 데이터 생성
        # self.table_widget_create()
        self.search()




    def del_pressed(self):
        print('삭제')

        conn = pymysql.connect(host='localhost', user='root', password='0000', db='jejudo',
                               charset='utf8')
        cur = conn.cursor()

        # SQL문 실행
        # 체크박스로 선택한것에 해당되는 "소재지 전체주소"가 포함 하는 행 삭제하는 기능

        if self.item_list != []:
            for item in self.item_list:
                cur.execute(f"DELETE FROM jejudo.jeju_table WHERE full_address = '{item[12]}'") # 아이템의 12번째 값은 소재지전체주소
                print(item[12])
        else:
            print('wrong')
            option = QtWidgets.QMessageBox.information(self, "QMessageBox", "체크박스를 선택 해 주세요",
                                                       QtWidgets.QMessageBox.Ok)
        cur.execute("select * from jejudo.jeju_table")

        # 데이터를 sql에 반영
        conn.commit()
        # # Connection 닫기
        conn.close()
        # 테이블 헤더를 제외한 데이터 삭제
        self.table.clearContents()
        # 테이블 안에 데이터 생성
        # self.table_widget_create()
        self.search()








if __name__ == "__main__":
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    # WindowClass의 인스턴스 생성
    mainWindow = MainWindow()

    # 프로그램 화면을 보여주는 코드
    mainWindow.show()

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()