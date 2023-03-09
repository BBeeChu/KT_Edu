import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
#import pydot
#from networkx.drawing.nx_pydot import graphviz_layout
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'NanumGothic'


class Graph_Viz():

    def __init__(self, job, df):
        self.job = job

    def set_edge_list(self, df):
        if self.job not in list(df['job']):
            print('해당 직업이 데이터베이스에 없습니다.')
            raise NotImplementedError
        else:
            pass

        # 직업_전공 연결 그래프 리스트 생성
        # 전공 노드 리스트: major_node_list
        # 직업과 전공 엣지 리스트: job_major_edge_list
        major_list = list(
            df[df.job == self.job]['major'])
        major_node_list = list(set(major_list))
        job_major_edge_list = []
        if len(major_node_list) != 0:
            for major in major_node_list:
                job_major_edge_list.append((self.job, major))

        # 전공과 과목을 연결 그래프 리스트 생성
        # 과목 노드 리스트: subject_category_list
        # 전공과 과목 엣지 리스트: major_subject_edge_list
        major_subject_edge_list = []
        for major in major_node_list:
            subject_category_list = list(
                df[df.major == major]['subject_category'])
            subject_category_node_list = list(set(subject_category_list))
            if len(subject_category_node_list) != 0:
                for subject in subject_category_node_list:
                    major_subject_edge_list.append((major, subject))

        # 데이터 프레임의 subject_details에서 ':'를 ','로 변경하여 '수학교과:'같은 노이즈 데이터를 필터링하기 위함
        df['subject_details'] = df['subject_details'].apply(
            lambda x: x.replace(':', ','))

        # 과목 유형의 리스트 생성
        category_details_edge_list = []
        category_details_node_list = []
        for category in subject_category_node_list:
            details_list = list(df[(df.job == self.job) & (
                df.subject_category == category)]['subject_details'])

            # 과목 유형을 첫번째 원소로 하는 리스트 생성
            tmp_list = []
            details_subject_list = [category]

            # string_type으로 되어 있는 세부과목들을 ','로 구분하여 details_subject_list에 추가
            for a in details_list:
                l = a.split(',')
                tmp_list.extend(l)

            # '~교과'로 되어 있는 노이즈 데이터 제거
            for e in tmp_list:
                if '교과' in e:
                    tmp_list.remove(e)
            tmp_list = [i.strip() for i in tmp_list]

            # '수학II'가 아니라 그냥 'II'라고 되어 있는 과목명을 바로 직전의 과목명을 참고하여 '수학II'로 변경
            for e in tmp_list:
                if len(e) == 1:
                    i = tmp_list.index(e)
                    tmp_list[i] = tmp_list[i-1][:-1]+e

            category_details_node_list.extend(tmp_list)
            details_subject_list.extend(tmp_list)

            # 과목 유형과 세부과목을 연결한 리스트 생성
            # 과목 유형과 세부과목 엣지 리스트: category_details_edge_list

            category_details_list = []
            if len(details_subject_list) != 0:
                for detail in details_subject_list[1:]:
                    category_details_list.append(
                        (details_subject_list[0], detail))
                category_details_edge_list.append(category_details_list)

        category_details_node_list = list(set(category_details_node_list))
        return major_node_list, job_major_edge_list, subject_category_node_list, major_subject_edge_list, category_details_node_list, category_details_edge_list

    def draw_graph(self, major_node_list, job_major_edge_list, subject_category_node_list, major_subject_edge_list, category_details_node_list, category_details_edge_list, horizontal=30, vertical = 30, file_name='graph.png'):
        
        g = nx.Graph()
        g.add_node(self.job, kind='직업', color='silver')
        g.add_nodes_from(major_node_list, kind='전공',
                         color='darkkhaki', size=50)
        g.add_nodes_from(subject_category_node_list,
                         kind='교과 유형', color='sandybrown')
        g.add_nodes_from(category_details_node_list,
                         kind='세부교과', color='paleturquoise')
        g.add_edges_from(job_major_edge_list, color='cyan', weight=2, length=40)
        g.add_edges_from(major_subject_edge_list,
                         color='silver', weight=2, length=2)
        for n in category_details_edge_list:
            g.add_edges_from(n, color='sandybrown', weight=2, length=15)
        node_colors = nx.get_node_attributes(g, 'color').values()
        edge_colors = nx.get_edge_attributes(g, 'color').values()
        node_size = g.number_of_nodes()
        #pos = nx.spring_layout(g)
        pos = nx.nx_agraph.graphviz_layout(g, prog="sfdp")
        plt.figure(figsize=(g.number_of_nodes()*3.2, g.number_of_nodes()*3.2))
        nx.draw(g,
                pos=pos,
                with_labels=True,
                font_family='NanumGothic',
                edge_color=edge_colors,
                node_color=node_colors,
                node_size = node_size*9000,
                font_size = node_size*3,
                width = node_size/10)
        # node_size=[v * 100 for v in node_sizes.values()])
        plt.savefig('results/'+file_name)
