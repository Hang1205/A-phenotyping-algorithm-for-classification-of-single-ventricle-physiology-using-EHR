# -*- coding: utf-8 -*-
"""
Created on Thu Jun 12 16:57:52 2025

@author: HangXu
"""
import pandas as pd
import re
import os

def impression2features(df1, topic, data_dir):
    '''
    df1 (pd.DataFrame): dataframe for feature extraction
    topic (str): {'echo', 'mri', 'ct', 'cardiology consultation'} topic of report
    data_dir (str): data directory
    '''
    columns = ['ip_patient_id','result_time','impression']
    df1 = df1[columns]
    df = df1.dropna(subset=['impression'])
    df = replace_repeat_terms(df)
    words =['fontan', 'single ventricle','hypoplastic left ventricle','tricuspid atresia', 'double inlet ventricle','hypoplastic left heart syndrome','norwood', 
              'good biventricular size', 'rastelli', '1.5 ventricle repair', 'biventricle repair']
    patterns = {word: re.compile(rf'\b{word}\b', re.IGNORECASE) for word in words}
    df = apply_check(df, words, patterns)
    df = merge_dob(df, data_dir)
    df['result_time'] =  pd.to_datetime(df['result_time'])
    df['dob'] = pd.to_datetime(df['dob'])
    df['age'] = (df['result_time'] - df['dob']).astype('<m8[Y]')
    new_order = ['ip_patient_id','mrn','age','dob','result_time','impression','fontan', 'single ventricle', 'hypoplastic left ventricle','tricuspid atresia', 'double inlet ventricle',
                 'hypoplastic left heart syndrome','norwood','good biventricular size', 'rastelli', '1.5 ventricle repair', 'biventricle repair']
    df = df[new_order]
    merged_df = df.groupby('ip_patient_id', as_index=False).max()
    return merged_df

def replace_repeat_terms(df):
    df['impression']=df['impression'].str.replace("DILV", "double inlet ventricle", case= False)
    df['impression']=df['impression'].str.replace("double inlet left ventricle", "double inlet ventricle", case= False)
    df['impression']=df['impression'].str.replace("hypoplastic LV", "hypoplastic left ventricle", case= False)
    df['impression']=df['impression'].str.replace('hlhs', 'hypoplastic left heart syndrome', case= False)
    df['impression']=df['impression'].str.replace('HLHS', 'hypoplastic left heart syndrome', case= False)
    df['impression']=df['impression'].str.replace('Hypoplastic left heart', 'hypoplastic left heart syndrome', case= False)
    df['impression']=df['impression'].str.replace('Norwood/Sano', 'norwood', case= False)
    df['impression']=df['impression'].str.replace("no fontan", "", case= False)
    df['impression']=df['impression'].str.replace("no tricuspid atresia", "", case= False)
    df['impression']=df['impression'].str.replace("no hlhs", "", case= False)
    df['impression']=df['impression'].str.replace("no hypoplastic left heart syndrome", "", case= False)
    df['impression']=df['impression'].str.replace("no norwood", "", case= False)
    df['impression']=df['impression'].str.replace("Tricuspid and pulmonary valve atresia", "tricuspid atresia", case= False)
    df['impression']=df['impression'].str.replace("severely hypoplastic ventricle", "hypoplastic left heart syndrome", case= False)
    return df

# Function to create a DataFrame to check all words in multiple texts
def apply_check(df, words, patterns):
    for word in words:
        df[word] = df['impression'].apply(lambda x: check_word(word, x, patterns))
    return df

def check_word(word, text, patterns):
    return 1 if patterns[word].search(text) else 0

def merge_dob(df, data_dir, filename='adjudication_case_2500.xlsx'):
    path0 = os.path.join(data_dir, filename)
    df1= pd.read_excel(path0, header= 0)
    
    df1 =df1[['IP_PATIENT_ID','MRN','DOB']]
    df1 = df1.rename(columns={'IP_PATIENT_ID': 'ip_patient_id', 'MRN':'mrn','DOB': 'dob'})
    columns = ['ip_patient_id','mrn','dob']
    df0 = df1[columns]
    merged_df = pd.merge(df, df0, on='ip_patient_id', how='left') 
    return merged_df
