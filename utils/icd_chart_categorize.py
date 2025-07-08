# -*- coding: utf-8 -*-
"""
Created on Fri Jun 13 11:07:30 2025

@author: HangXu
"""
import pandas as pd
import os
    
def icd_chart(
        data_dir, 
        filename=[
            'Encounter_Daignoses.csv',
            'Patient_Identifiders.csv',
        ]
    ):

    path = os.path.join(data_dir, filename[0])
    df = pd.read_csv(path, header= 0)
    terms =['Q20.4','Q22.4','Q23.4','745.3','746.7',]
    pattern = '|'.join(terms)
    df0 = df[df['ICD_CODE'].astype(str).str.contains(pattern, na=False, case=False)].reset_index()
    data1 = {'IP_PATIENT_ID': df0['IP_PATIENT_ID'].unique()}
    df1 = pd.DataFrame(data1)
    df0 = df0.drop_duplicates(subset=['IP_PATIENT_ID', 'ICD_CODE'])
    df00 = df0.groupby('IP_PATIENT_ID')['ICD_CODE'].agg(lambda x: ', '.join(x)).reset_index()

    path = os.path.join(data_dir, filename[1])
    df3 = pd.read_csv(path, header= 0)
    result = [find_mrn(patient_id, df3) for patient_id in df00['IP_PATIENT_ID']]
    df00['MRN'] = result
    chart1 = df00
    
    terms =['Q20.1','Q21.2','Q22.0','Q22.1','Q22.2','Q22.3','Q22.5','Q22.6','746.1','Q22.8','Q22.9','Q23.2','Q25.41','Q25.5','745.11','746.00','746.702','746.09','746.2','746.5','747.22','747.29','747.31']
    pattern = '|'.join(terms)
    df2 = df[df['ICD_CODE'].astype(str).str.contains(pattern, na=False, case=False)].reset_index()
    df2 = df2.drop_duplicates(subset=['IP_PATIENT_ID', 'ICD_CODE'])
    df22= df2.groupby('IP_PATIENT_ID')['ICD_CODE'].agg(lambda x: ', '.join(x)).reset_index()
    df22 = df22[~df22['IP_PATIENT_ID'].isin(df1['IP_PATIENT_ID'])]
   
    result = [find_mrn(patient_id, df3) for patient_id in df22['IP_PATIENT_ID']]
    df22['MRN'] = result 
    chart2 = df22
    
    dfa = df.drop_duplicates(subset=['IP_PATIENT_ID'])
    combined_df1_df2 = pd.concat([df0, df22]).drop_duplicates()
    remaining_df = dfa[~dfa['IP_PATIENT_ID'].isin(combined_df1_df2['IP_PATIENT_ID'])]
    df4 = remaining_df [['IP_PATIENT_ID']]
    result = [find_mrn(patient_id, df3) for patient_id in df4['IP_PATIENT_ID']]
    df4['MRN'] = result 
    chart3 = df4
    
    df_t1 = icd123(df, chart1)
    df_t2 = icd123(df, chart2)
    df_t3 = icd123(df, chart3)
    
    return df_t1, df_t2, df_t3

def find_mrn(patient_id, df):
    mrn = df.loc[df['IP_PATIENT_ID'] == patient_id, 'MRN'].values
    if len(mrn) > 0:
        return mrn[0]
    else:
        return None
    
def icd123(df0, chart, topic):
    df = chart
    df = df.rename(columns={'IP_PATIENT_ID': 'ip_patient_id',  'ICD_CODE':'icd_code'})
    merged_df1 = pd.merge(df, df0, on='ip_patient_id', how='left')
    merged_df1 = merged_df1 [(merged_df1 .drop(columns=['ip_patient_id','mrn','age']) != 0).any(axis=1)]
    merged_df1 = merged_df1.drop_duplicates()
    return merged_df1

def filtering(df1):
    condition1 = df1['fontan']== 1
    condition2 = df1['fontan']== 0
    condition3 = df1['age'] <=25
    #condition4 = df1['single ventricle'] == 1
    condition5 = df1['hypoplastic left ventricle'] == 1 
    condition6 = df1['tricuspid atresia'] == 1 
    condition7 = df1['double inlet ventricle'] == 1
    condition8 = df1['hypoplastic left heart syndrome'] == 1
    condition9 = df1['norwood'] == 1 
    condition10 = df1['rastelli'] == 0
    condition11 = df1['good biventricular size'] == 0
    condition12 = df1['1.5 ventricle repair'] == 0
    condition13 = df1['biventricle repair'] == 0
    condition14 = df1['Normalized_LVEDV'] <= 20
    condition15 = df1['Normalized_LVEDV'].isna()
    df11 = df1[condition1]
    df12 = df1[condition2 & condition3 &(condition5| condition6|condition7| condition8|condition9 )& condition10 & condition11 & condition12 & condition13 & (condition14|condition15)]#
    return df11, df12 
