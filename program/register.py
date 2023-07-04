import numpy as np
from datetime import datetime

# 2차원 데이터를 1차원 데이터로 변환한다.
def two2oneArray(nested_list):
    flat_list = [item for sublist in nested_list for item in sublist]
    return flat_list

# 교수님에 대응되는 id를 반환한다.
def search_instructor_id(cursor, name, dept):
    print("search_instructor_id:", name, dept)
    query = "SELECT INSTRUCTOR.instructorID FROM INSTRUCTOR WHERE INSTRUCTOR.instructorName=%s and INSTRUCTOR.deptName=%s"
    cursor.execute(query, (name, dept))
    instruction_id = cursor.fetchone()
    if instruction_id == None:
        return [-1]
    return instruction_id

def split_date(curdate):
    # 월수10:30-12:00
    # 월10:30-12:00
    # 월10:30-12:30,화10:30-12:30
    
    data_list = []
    if ',' in curdate:
        t = curdate.split(',')
        data_list.append(t[0], t[1])
    for i in range(len(curdate)):
        print("curdate in split_date:\n", curdate[i])
        if ',' in curdate[i]: # 월10:30-12:30,화10:30-12:30
            tmp = curdate[i].split(',')
            data_list.append(tmp[0])
            data_list.append(tmp[1])
        elif ord('0') > ord(curdate[i][1]) or ord(curdate[i][1]) > ord('9'): # 월수10:30-12:00
            data_list.append(curdate[i][0] + curdate[i][2:])
            data_list.append(curdate[i][1] + curdate[i][2:])
        else:
            data_list.append(curdate[i])
    return data_list

def register(cursor, value):
    # print('입력: studentId, instructorName, deptName, course_id, class_id')
    # studentId, instructorName, deptName, courseId, classId = input().split()
    value = [v.strip() for v in value]
    studentId, instructorName, deptName, courseId, classId = value[0], value[1], value[2], value[3], value[4]
    instructorId = search_instructor_id(cursor, instructorName, deptName)[0]
    print("instructorId=>", instructorId)
    if (instructorId == -1):
        print("wrong instructorName and deptName")
        return False
    # CREDIT이 18학점을 넘으면 안된다. (1)
    # 현재 수강하려고 하는 과목의 credit을 select한다.
    query = """
    SELECT COURSE.credit
    FROM COURSE
    WHERE COURSE.courseID=%s AND COURSE.classID=%s AND COURSE.deptName=%s
    """
    cursor.execute(query, (courseId, classId, deptName, ))
    cur_credit = cursor.fetchone()[0]

    # 지금까지 학생이 수강한 과목의 총 credit 더해서 select한다.
    query = """
    SELECT SUM(COURSE.credit)
    FROM TAKES
    INNER JOIN COURSE 
    ON TAKES.ref_courseID=COURSE.courseID AND TAKES.ref_classID=COURSE.classID AND TAKES.ref_deptName=COURSE.deptName
    WHERE TAKES.ref_studentID=%s
    """
    print(cur_credit)
    cursor.execute(query, (studentId, ))
    courseCredit = cursor.fetchone()[0]
    if courseCredit == None:
        query = "INSERT INTO TAKES (ref_studentID, ref_instructorID, ref_courseID, ref_classID, ref_deptName) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (studentId, instructorId, courseId, classId, deptName, ))
        cursor.fetchall()
        return True
    total_credit = int(cur_credit) + int(courseCredit)
    print('total_credit:', total_credit)
    # 총합이 18 credit보다 큰지를 확인한다.
    if total_credit > 18:
        print('your credit is over')
        return False

    # 같은 과목 재수강 허용안하는 쿼리 (2)
    # 같은 과목의 기준은 학수번호의 동일함이다.
    
    query = """
    SELECT COUNT(*) AS row_count
    FROM TAKES
    WHERE TAKES.ref_courseID=%s AND TAKES.ref_studentID=%s
    """
    cursor.execute(query, (courseId, studentId))
    overlap = cursor.fetchone()[0]
    if overlap == None:
        overlap = 0
    print('overlap:\n', overlap)
    if overlap > 0:
        print('your course is overlap')
        return False

    # 중복되는 시간대의 수업을 못 듣는 쿼리 (3)
    # 자신이 듣고 싶은 수업의 시간대를 받는다.
    query = """
    SELECT COURSE.courseDate
    FROM COURSE
    WHERE COURSE.courseID=%s AND COURSE.classID=%s AND COURSE.deptName=%s
    """
    cursor.execute(query, (courseId, classId, deptName, ))
    cur_date = []
    cur_date.append(cursor.fetchone()[0])
    if cur_date[0] == '없음': # 예외처리
        cur_date[0] = '없00:00-00:00'
    print(cur_date)
    # 지금까지 신청한 수업의 시간대를 받는다.
    query = """
    SELECT COURSE.courseDate
    FROM TAKES
    INNER JOIN COURSE 
    ON TAKES.ref_courseID=COURSE.courseID AND TAKES.ref_classID=COURSE.classID AND TAKES.ref_deptName=COURSE.deptName
    WHERE TAKES.ref_studentID=%s
    """
    cursor.execute(query, (studentId, ))
    date = cursor.fetchall()
    date = two2oneArray(date)
    
    print("date:", date)
    # 지금까지 신청한 수업의 시간대와 듣고자 하는 시간대를 비교한다.
    cur_date = split_date(cur_date)
    past_date = split_date(date)
    for i in range(len(cur_date)):
        print("cur_date:",cur_date[i])
        cur_week = cur_date[i][0]
        tmp = cur_date[i][1:]
        cur_start, cur_end = tmp.split('-')
        print("cur_start, cur_end:",cur_start, cur_end)
        cur_start_time = datetime.strptime(cur_start, "%H:%M")
        cur_end_time = datetime.strptime(cur_end, "%H:%M")
        for j in range(len(past_date)):
            past_week = past_date[j][0]
            tmp = past_date[j][1:]
            past_start, past_end = tmp.split('-')
            past_start_time = datetime.strptime(past_start, "%H:%M")
            past_end_time = datetime.strptime(past_end, "%H:%M")
            print("week:", cur_week, past_week)
            if cur_week == past_week:
                if cur_start_time < past_end_time and past_end_time <= cur_end_time:
                    print("cur_start_time, past_end_time:", cur_start_time, past_end_time)
                    print("cur_end_time, past_start_time:", cur_end_time, past_start_time)
                    return False
                elif cur_start_time <= past_start_time and past_start_time < cur_end_time:
                    print("cur_start_time, past_end_time:", cur_start_time, past_end_time)
                    print("cur_end_time, past_start_time:", cur_end_time, past_start_time)
                    return False

    # (1), (2), (3) 비교하고 INSERT한다.
    # studentId, instructorName, deptName, courseId, classId
    query = "INSERT INTO TAKES (ref_studentID, ref_instructorID, ref_courseID, ref_classID, ref_deptName) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (studentId, instructorId, courseId, classId, deptName, ))
    take_count = cursor.fetchall()
    return True


# Register.py

# 컴파일용

# 학번, 교수님 성함, 학부, 학수번호, 분반
# 19011547 박태순 컴퓨터공학과 009912 001 // 목16:30-18:30
# 19011547 송상훈 컴퓨터공학과 004118 001 // 월수13:30-15:30
# 19011547 문승빈 컴퓨터공학과 004118 002 // 월수 15:00-17:00 >> fail, 겹치는 시간대
# 19011547 노재춘 컴퓨터공학과 004310 003 // 월수13:30-15:00 >> fail, 겹치는 시간대
# 19011547 양효식 컴퓨터공학과 010111 013 // 화 >> success	
		
# 19011547 이성주 전자정보통신공학과 008626 001 // 목15:00-18:00 >> fail, 겹치는 시간대
# 19011547 김천식 소프트웨어학과 009912 001 // 금14:00-16:00 >> fail, 동일 과목 수강
# 19011547 김청원 소프트웨어학과 004310 001 // 월수09:00-10:30		
# 19011547 김종열 전자정보통신공학과 007806 003 //화목12:00-13:30
# 19011547 송형규 전자정보통신공학과 011302 015 //화19:30-20:30
# 19011547 노재춘 컴퓨터공학과 009912 002 // 월 16:30-18:30 >> fail 동일과목
# 19011547 김성호 전자정보통신공학과 007806 001	// 화목09:00-10:30 >> fail 동일과목
# 19011547 송형규 전자정보통신공학과 004474 002 // 화목13:30-15:00	>> fail, credit is over

# 19011550 송형규 전자정보통신공학과 004474 002 // 화목13:30-15:00 >> successs, 다른 student_id에 할당
# 19011547 김우식 전자정보통신공학과 008621 001 // 화목10:30-12:00 >> fail, credit is over
# 19011550 김우식 전자정보통신공학과 008621 001 // 화목10:30-12:00 >> success, 다른 student_id에 할당


