import pandas as pd
import random

student_name = '김상원 김상우 김상우 박동규 김효성 김정훈 최진수 강주현 최우석 안희찬 윤태강 윤태형 안치원 이영우 이로운 임수진 권대완 김상원 정태헌 노윤석 박단비 박수진 여다건 권하윤 김동우 김민준 허진호 김동근 박경범 김인성 정주영 홍철개 이학균 김명동 최예진 유미현 이동훈'
student_name = student_name.split(' ')
student_id = [str(19011547 + i) for i in range(len(student_name))]
score = [round(random.uniform(1, 4.5),3) for i in range(len(student_name))]


student = pd.DataFrame({'student_name': student_name, 'studentID': student_id, 'student_grade':score})
print(student)
student.to_csv('data\student_data.csv', index = False)