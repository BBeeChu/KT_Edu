from draw_graph_new import *
#import pandas as pd

job = input('직업을 입력해주세요: ')

#image_size = input('이미지의 크기를 숫자로 입력해주세요: ')

df = pd.read_csv('data_analysis/job_major_subject.csv')
'''
try:
    self.job not in df['job']
except:통
    print('해당 직업이 데이터베이스에 없습니다.
    )
    raise NotImplementedError
'''
file_name = input('이미지를 저장할 파일명을 입력해주세요: ')
g = Graph_Viz(job, df)
a, b, c, d, e, f = g.set_edge_list(df)
g.draw_graph(a, b, c, d, e, f, file_name=file_name)
