import pandas as pd
import numpy as np
import zipfile

# import data
zf = zipfile.ZipFile(
    '/home/seongyeub/2022/KT_Project/KT_Edu/ou_student_predictions/content/anonymisedData.zip')

registrations = pd.read_csv(zf.open('studentRegistration.csv'))
courseInfo = pd.read_csv(zf.open('courses.csv'))
students = pd.read_csv(zf.open('studentInfo.csv'))
student_vle = pd.read_csv(zf.open('studentVle.csv'))
vle_info = pd.read_csv(zf.open('vle.csv'))
student_assessments = pd.read_csv(
    zf.open('studentAssessment.csv'), skiprows=[128223, 64073])
assessments_info = pd.read_csv(zf.open('assessments.csv'))
index_columns = ['code_module', 'code_presentation', 'id_student']


index_columns = ['code_module', 'code_presentation', 'id_student']
# Registrations
full_registrations = pd.merge(
    students, registrations, on=index_columns, validate='1:1')
full_registrations = pd.merge(full_registrations, courseInfo,
                              on=['code_module', 'code_presentation'], validate='many_to_one')
full_registrations.dropna(
    subset=['date_registration', 'imd_band'], inplace=True)

full_registrations.drop(columns=['imd_band', 'age_band', 'num_of_prev_attempts',
                        'studied_credits', 'disability', 'date_registration', 'date_unregistration'], inplace=True)

full_registrations = pd.merge(full_registrations, student_vle, how='left', on=[
                              'code_module', 'code_presentation', 'id_student'], validate='m:m')

full_registrations = pd.merge(full_registrations, assessments_info, how='left', on=[
                              'code_module', 'code_presentation'], validate='m:m')

full_registrations.drop(columns=['date_y', 'weight'], inplace=True)

#full_registrations.rename(columns={'date_x': 'date'})

full_registrations = full_registrations[full_registrations['date_x'] > 0]

full_registrations.to_csv(
    '/home/seongyeub/2022/KT_Project/KT_Edu/ou_student_predictions/data/eda_data.csv')
