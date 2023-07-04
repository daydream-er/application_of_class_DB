import register

def search_instructor_course(cursor, value): # course를 수업하시는 교수님 명단 출력
    # print('입력: 학수번호를 입력하세요.')
    # courseId = input().split()
    # print(courseId, "\n\n")
    courseId = value.strip()
    query = """
    SELECT INSTRUCTOR.instructorName
    FROM COURSE
    INNER JOIN INSTRUCTOR
    ON COURSE.ref_instructorID=INSTRUCTOR.instructorID
    WHERE COURSE.courseID=%s
    """
    cursor.execute(query, (courseId, ))
    names = cursor.fetchall()
    if not names:
        print('nothing')
        return ('nothing', False)
    names = register.two2oneArray(names)
    return (names, True)
    

def search_student_course(cursor, value): # course를 수강하는 학생들 명단 출력
    # print('입력: 학수번호를 입력하세요.')
    # courseId = input().split()
    courseId = value.strip()
    query = """
    SELECT STUDENT.student_name
    FROM TAKES
    INNER JOIN STUDENT 
    ON TAKES.ref_studentID=STUDENT.studentID
    WHERE TAKES.ref_courseID=%s
    """
    cursor.execute(query, (courseId, ))
    names = cursor.fetchall()
    if not names:
        print("nothing in course")
        return ('nothing', False)
    names = register.two2oneArray(names)
    return (names, True)
    
def search_score_course(cursor, value): # course를 수강하는 학생들의 평균 학점 및 인원 수
    # print('입력: 학수번호를 입력하세요.')
    # courseId = input().split()
    courseId = value.strip()
    query = """
    SELECT COUNT(*), AVG(STUDENT.student_grade)
    FROM TAKES
    INNER JOIN STUDENT 
    ON TAKES.ref_studentID=STUDENT.studentID
    WHERE TAKES.ref_courseID=%s
    """
    cursor.execute(query, (courseId, ))
    count, score = cursor.fetchone()
    if count == 0:
        print("nothing in score")
        return (0, 0, False)
    return (count, score, True)

def search_student_has(cursor, value): # 현재 학생이 수강 신청한 수업을 출력한다.
    studentId = value.strip()
    query = """
    SELECT COURSE.title
    FROM TAKES
    INNER JOIN COURSE 
    ON TAKES.ref_courseID=COURSE.courseID AND TAKES.ref_classID=COURSE.classID AND TAKES.ref_deptName=COURSE.deptName
    WHERE TAKES.ref_studentID=%s
    """
    cursor.execute(query, (studentId, ))
    course_name = cursor.fetchall()
    if not course_name:
        print("nothing")
        return ('nothing in course', False)
    course_name = register.two2oneArray(course_name)
    return (course_name, True)

def drop(cursor, value):
    # print('입력: 학수번호와 학번을 입력하세요.')
    # courseId, studentId = input().split()
    value = [v.strip() for v in value]
    courseId, studentId = value[0], value[1]
    # drop하기 전에 해당 과목을 신청했는지 확인합니다.
    query = "SELECT COUNT(*) FROM TAKES WHERE ref_courseID=%s and ref_studentID=%s"
    cursor.execute(query, (courseId, studentId, ))
    take_count = cursor.fetchone()[0]
    if take_count == 0:
        print("drop fail\n")
        return False

    query = """
    SELECT SUM(COURSE.credit)
    FROM TAKES
    INNER JOIN COURSE 
    ON TAKES.ref_courseID=COURSE.courseID AND TAKES.ref_classID=COURSE.classID AND TAKES.ref_deptName=COURSE.deptName
    WHERE TAKES.ref_studentID=%s
    """
    cursor.execute(query, (studentId, ))
    courseCredit = cursor.fetchone()[0]
    
    query = """
    SELECT SUM(COURSE.credit)
    FROM TAKES
    INNER JOIN COURSE 
    ON TAKES.ref_courseID=COURSE.courseID AND TAKES.ref_classID=COURSE.classID AND TAKES.ref_deptName=COURSE.deptName
    WHERE TAKES.ref_studentID=%s AND TAKES.ref_courseID=%s
    """
    cursor.execute(query, (studentId, courseId, ))
    dropCredit = cursor.fetchone()[0]
    print('drop 전과 drop 후', courseCredit, courseCredit - dropCredit)
    
    # drop한다.
    query = "DELETE FROM TAKES WHERE ref_studentID=%s and ref_courseID=%s"
    cursor.execute(query, (studentId, courseId, ))
    print("drop successfully")
    return True