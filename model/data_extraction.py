import pandas as pd
import numpy as np

df_vw_class_activity = pd.read_csv(
    '/mnt/c/Users/user/Desktop/KT_Edu/data/vw_class_activity.csv')

print(df_vw_class_activity.info(verbose=True))  # checks info of df


df_vw_class_activity = df_vw_class_activity.drop(columns=['tutor_user_idx', 'course_id', 'course_class_id', 'course_class_seq_id',
                                                          'registered_by_user_idx', 'registered_date', 'last_modified_by_user_idx', 'last_modified_date'])

# drops columns by names

df_vw_class_activity.to_excel('vw_class_activity.xlsx')

'''
at_info = pd.DataFrame(df_vw_attendance_info.iloc[:, 8])
df_vw_attendance_info = pd.merge(id, at_info, how='outer', left_index=True, right_index=True)  # data merge by column and index
# print(df_vw_attendance_info)
# df_vw_attendance_info.to_excel('vw_attendance_info.xlsx')

print(
    df_vw_attendance_info[df_vw_attendance_info['attend_absente_late'].isnull()])
'''
