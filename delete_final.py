```py
class MainWindow(QMainWindow, form_class): #화면을 띄우는데 사용되는 Class 선언
    def __init__(self):
        super().__init__()
        self.jejuFormShow = Add()   # Add클래스를 self.jejuFormShow로 선언
        self.setupUi(self)
        self.table_widget_create()
        self.btn_search.clicked.connect(self.search)
        self.btn_edit.clicked.connect(self.edit)
        self.btn_del.clicked.connect(self.del_pressed)
        self.checkbox_clicked = False ################################## 이 줄만 복붙하면 됩니다.
        self.item_list = [] #체크박스 클릭된 것들 리스트
        
    ### 통째로 복붙!!    +     def table_widget_create(self):get_checked 로 연결
    def get_checked(self): # 체크박스 클릭된 것  리스트로 넣기
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
    
    def del_pressed(self):
        if self.checkbox_clicked == True:

            self.confu = pymysql.connect(host='localhost', user='root', password='0000', db='jeju_project',
                                         charset='utf8')
            curr = self.confu.cursor()
            for item in self.item_list:
                curr.execute(f"DELETE FROM jeju_project.jeju_table WHERE Restaurant_name = '{item}'")
            curr.execute("select * from jeju_project.jeju_table")
            self.temp = curr.fetchall()
            self.confu.commit()

            self.table.clearContents()
            for i in range(len(self.temp)):
                for j in range(len(self.temp[i])):

                    self.table.setItem(i, j, QTableWidgetItem(str(self.temp[i][j])))
        else:
            print('wrong')
            QtWidgets.QMessageBox.information(self, "QMessageBox", "체크박스를 클릭해 주세요")
```
