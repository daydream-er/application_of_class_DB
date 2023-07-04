import sys
import mysql.connector
import register
import other_utility

##########################################################################
##########################################################################
##                                                                      ##
##                                                                      ##
##                  compile용도  demo_version                           ##
##                                                                      ##
##                                                                      ##
##########################################################################
##########################################################################


print('What do you want to do?')
print('1. Register a course') # insert
print('2. Drop a course') # drop
print('3. search, instructor\'s course') # search instrucotr
print('4. search, student\'s course') # search student
print('5. search, score in course') # search student score, number
print('6. search, student has course') # search_student_has
print('7. end')
print('input!')
    
    
# Connect database
id = 'director'
password = '19011547kimsangwon'

try:
    dbConn = mysql.connector.connect(host='localhost', user=id, password=password, db='project')
    print("DB Connection Success")
except mysql.connector.Error as e:
    print("Error connecting to MySQL Platform:", e)
    sys.exit(1)

while True:
    command = input()
    print('input!')
    
    cursor = dbConn.cursor()
    ret = [False]
    print('this is =>', command)
    value = input().split()
    if command == '1':
        ret = [register.register(cursor, value)]
    elif command == '2':
        ret = [other_utility.drop(cursor, value)]
    elif command == '3':
        ret = other_utility.search_instructor_course(cursor, value)
        if ret[-1] == False:
            break
        print(ret[0], ret[1])
    elif command == '4':
        ret = other_utility.search_student_course(cursor, value)
        if ret[-1] == False:
            break
        print(ret[0])
    elif command == '5':
        ret = other_utility.search_score_course(cursor, value)
        if ret[-1] == False:
            break
        print(ret[0], ret[1])
    elif command == '6':
        ret = other_utility.search_student_has(cursor, value)
        if ret[-1] == False:
            break
        print(ret[0], ret[1])
    else:
        break
    
    
    if ret[-1] == False:
        print("fail")
        break
    else:
        print("success")
    dbConn.commit()
    cursor.close()
    
dbConn.close()


