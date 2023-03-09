import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx


class Graph_Viz():

    def __init__(self, job, df):   
        self.job = job

    def set_edge_list(self, df):
                

        # 직업과 과목을 연결하는 리스트 생성
        # 직업과 과목 엣지 리스트: job_subject_edge_list
        subject_category_list = list(
            df[df.job == self.job]['subject_category'])
        subject_category_node_list = list(set(subject_category_list))
        job_subject_edge_list = []
        if len(subject_category_node_list) != 0:
            for subject in subject_category_node_list:
                job_subject_edge_list.append((self.job, subject))

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
        return subject_category_node_list, job_subject_edge_list, category_details_node_list, category_details_edge_list

    def draw_graph(self, subject_category_node_list, job_subject_edge_list, category_details_node_list, category_details_edge_list, graph_size=15, file_name='graph.png'):
        plt.figure(figsize=(graph_size, graph_size))
        g = nx.Graph()
        g.add_node(self.job, kind='직업', color='silver')
        g.add_nodes_from(subject_category_node_list,
                         kind='교과 유형', color='sandybrown')
        g.add_nodes_from(category_details_node_list,
                         kind='세부교과', color='lightskyblue')
        g.add_edges_from(job_subject_edge_list,
                         color='silver', weight=2, length=10)
        for n in category_details_edge_list:
            g.add_edges_from(n, color='sandybrown', weight=2, length=10)
        node_colors = nx.get_node_attributes(g, 'color').values()
        edge_colors = nx.get_edge_attributes(g, 'color').values()
        node_sizes = dict(g.degree)
        pos = nx.spring_layout(g)
        nx.draw(g,
                pos=pos,
                with_labels=True,
                font_family='NanumGothic',
                edge_color=edge_colors,
                node_color=node_colors,
                node_size=[v * 100 for v in node_sizes.values()])
        plt.savefig('/home/seongyeub/2022/KT_Project/KT_Edu/job_map/result_image/'+file_name)
