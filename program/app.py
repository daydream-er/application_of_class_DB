from flask import Flask, render_template, request, redirect
import numpy as np
app = Flask(__name__)

import mysql.connector
import register
import other_utility

log_in = {}
@app.route('/', methods=['GET', 'POST'])
def ft_main():
    if request.method == 'POST':
        name = request.form['name'] # user_id
        password = request.form['password'] # password
        
        # 위의 값을 log_in라는 dictonary에 저장하여 후에 mysql.connector.connect을 할 때 사용합니다.
        # 이를 통해 사용자 권한에 따라 사용할 수 있는 Query 종류가 제한됩니다.
        log_in['name'] = name
        log_in['password'] = password
        print(name, password)
        return redirect('/main')
    return render_template('index.html')


# 함수 설명

# register 즉 수강 신청 함수
# drop 즉 수강 취소 함수
# search_instructor_course 즉 course를 수업하시는 교수님 명단을 반환하는 함수
# search_student_course 즉 course를 수강하는 학생들의 명단을 반환하는 함수
# search_score_course 즉 course를 수강하는 학생들의 명수와 평균을 반환하는 함수
# search_student_has 즉 특정 학생이 수강 신청한 수업의 명단을 반환하는 함수


@app.route('/main', methods=['GET', 'POST'])
def ft_query():
    result = []
    selected_sql = ""
    if request.method == 'POST':
        # 6종류의 기능을 수행하기 위해 6번의 input을 받을 수 있지만, front-end 코드를 간단하게 구성하기 위해 간단한 제약제항을 만들었습니다.
        # 가장 최상단 값이 ""이 아니라면 해당 값을 실행합니다.
        # 예를 들어 register_value와 SearchScore에 값이 들어왔다면 register_value에 해당되는 명령이 수행됩니다.
        register_value = request.form.getlist('input1')
        drop_value = request.form.getlist('input2')
        Instructor_value = request.form['input3'] 
        Student_value = request.form['input4']
        SearchScore = request.form['input5']
        SearchStudentHas = request.form['input6']
        # print(Student_value)
        try:
            dbConn = mysql.connector.connect(host='localhost', user=log_in['name'], password=log_in['password'], db='project')
            print("DB Connection Success")
            cursor = dbConn.cursor()
            if register_value[0] != '':
                selected_sql = 'register'
                result.append(register.register(cursor, register_value))
            elif drop_value[0] != '':
                selected_sql = 'drop'
                result.append(other_utility.drop(cursor, drop_value))
            elif Instructor_value != '':
                selected_sql = 'instructor'
                result = other_utility.search_instructor_course(cursor, Instructor_value)
            elif Student_value != '':
                selected_sql = 'student'
                result = other_utility.search_student_course(cursor, Student_value)
            elif SearchScore != '':
                selected_sql = 'score'
                result = other_utility.search_score_course(cursor, SearchScore)
            elif SearchStudentHas != '':
                selected_sql = 'having'
                result = other_utility.search_student_has(cursor, SearchStudentHas)
            dbConn.commit()
            cursor.close()
            dbConn.close()
            print('MySQL Connection Close')
        except mysql.connector.Error as e: # 예외처리
            print('Database connecting Error: ',e)
            print("Error:\n\n", selected_sql, result)
            return 'Fail'
        if result[-1] == False: # 함수 실패를 반환합니다.
            return 'Fail in function'
        result = result[:-1]
        return render_template('result.html', my_array = result, sql = selected_sql) # 값과 sql 종류를 html로 넘깁니다.
    return render_template('main.html')

if __name__ == '__main__':
    app.run()
