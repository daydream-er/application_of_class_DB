import pandas as pd
import numpy as np

# 인공지능학과, 소프트웨어학과, 컴퓨터공학과, 전자정보통신학과의 23-1 강의시간표를 하나의 exel로 합친 후 read하였습니다.
data = pd.read_excel('data\sejong_univ_data.xlsx')
print(data.columns)

# course에 대한 data를 생성합니다.
preprocessed_data = data[['학수번호', '분반', '교과목명', '교수명', '주관학과', '요일 및 강의시간', '학점/이론/실습']]

# '요일 및 강의시간'에 대하여 값이 없을 경우 '없음'으로 대체하였습니다.
preprocessed_data['요일 및 강의시간'] = preprocessed_data['요일 및 강의시간'].fillna('없음')

# mysql을 통해 table에 쉽게 넣기 위해 table column명과 동일하게 합니다.
preprocessed_data.columns = [['courseID', 'classID', 'title', 'instructorName', 'deptName', 'courseDate', 'credit']]

# '학점/이론/실습'에서 'credit'만 뽑는 코드입니다.
credit = preprocessed_data['credit'].values
tmp = []
for value in credit:
    value = str(value)[2:-1]
    value = value.split('/')[0]
    tmp.append(float(value))
preprocessed_data['credit'] = tmp

# instruction_id를 생성하는 코드입니다.
# one-hot encoding의 embedding 방식을 활용했습니다.
tmp = preprocessed_data[['instructorName', 'deptName']].values
dictonary = {}
instructor_id_column = []
instructor_id = 0
for i in range(len(tmp)):
    key = tuple(tmp[i])
    if key not in dictonary:
        dictonary[key] = instructor_id
        instructor_id+=1
    instructor_id_column.append(dictonary[key])
print(instructor_id)
print(len(instructor_id_column), preprocessed_data.shape)
preprocessed_data['instructorID'] = instructor_id_column

# PROJECT.INSTRUCTOR TABLE
instructor_data = preprocessed_data[['instructorID', 'instructorName', 'deptName']]
# print("this=>\n", instructor_data.columns)
instructor_data = instructor_data.drop_duplicates(subset=[('instructorID',)])
instructor_data.to_csv('data\instructor_data.csv', index = False)

# PROJECT.COURSE TABLE
preprocessed_data = preprocessed_data.rename(columns = {'instructorID': 'ref_instructorID'})
course_data = preprocessed_data[['courseID', 'classID', 'title', 'deptName', 'courseDate', 'ref_instructorID', 'credit']]
course_data.to_csv('data\course_data.csv', index = False)


