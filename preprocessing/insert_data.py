import mysql.connector
import pandas as pd
import numpy as np

# Login id: director
# password: 19011547kimsangwon
# 권한: 모든 권한

# Login id: selector
# password: selector
# 권한: select만 가능

# table_name과 data_name을 통해 table에 data를 insert하였습니다.
def insert_query(cursor, table_name, data_name):
    # insert_query
    df = pd.read_csv('data\\' + data_name)
    columns_name = df.columns.tolist()
    print(columns_name)
    columns = df.shape[1]
    rows = df.shape[0]
    
    query_columns = ', '.join(['%s'] * columns)
    for i in range(rows):
        result = df.iloc[i].astype(str)
        row_data = tuple(result)
        print(result)
        insert_query = f"INSERT INTO {table_name} ({', '.join(columns_name)}) VALUES ({query_columns})"
        
        print(row_data, "\n")
        print(insert_query, "\n")
        cursor.execute(insert_query, row_data)

# Connect database
# id = 'director'
# password = '19011547kimsangwon'
id = 'root'
password = '1234'

dbConn = mysql.connector.connect(host='localhost', user=id, password=password, db='project')
cursor = dbConn.cursor()

insert_query(cursor, 'PROJECT.STUDENT', 'student_data.csv')
insert_query(cursor, 'PROJECT.INSTRUCTOR', 'instructor_data.csv')
insert_query(cursor, 'PROJECT.COURSE', 'course_data.csv')
take_count = cursor.fetchall()
dbConn.commit()
cursor.close()
dbConn.close()


# https://happyeuni.tistory.com/19
# f-string 방식 참고하였습니다.