import pymysql

# MySQL Connection 연결
conn = pymysql.connect(host='localhost', user='root', password='160072', db='jejudo', charset='utf8')

# Connection 으로부터 Cursor 생성
cur = conn.cursor()

# SQL문 실행
sql = "select * from jejudo.jeju_table"
cur.execute(sql)

# 데이타 Fetch
rows = cur.fetchall()

print(rows)  # 전체 rows
# print(rows[0])  # 첫번째 row: (1, '김정수', 1, '서울')
# print(rows[1])  # 두번째 row: (2, '강수정', 2, '서울')

# Connection 닫기
conn.close()

# ---------
# import pymysql
#  conn = pymysql.connect(host=’127.0.0.1′, user=’root’, password=’0000′, db=’soloDB’, charset=‘utf8’)