# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 16:35:40 2024

@author: HangXu
"""
import pandas as pd
import re

def impression2features(df1, topic):
    columns = ['ip_patient_id','result_time','impression']
    df1 = df1[columns]
    df = df1.dropna(subset=['impression'])
    #df = replace_repeat_terms(df1)
    words =['fontan', 'single ventricle','hypoplastic left ventricle','tricuspid atresia', 'double inlet ventricle','hypoplastic left heart syndrome','norwood', 
              'good biventricular size', 'rastelli', '1.5 ventricle repair', 'biventricle repair']
    patterns = {word: re.compile(rf'\b{word}\b', re.IGNORECASE) for word in words}
    df = apply_check(df, words, patterns)
    df = merge_dob(df)
    df['age'] = (df['result_time'] - df['dob']).astype('<m8[Y]')
    new_order = ['ip_patient_id','mrn','age','dob','result_time','impression','fontan', 'single ventricle', 'hypoplastic left ventricle','tricuspid atresia', 'double inlet ventricle',
                 'hypoplastic left heart syndrome','norwood','good biventricular size', 'rastelli', '1.5 ventricle repair', 'biventricle repair']
    df = df[new_order]
    merged_df = df.groupby('ip_patient_id', as_index=False).max()
    merged_df.to_excel('U:/HangXu/SVP/data_analysis/Data_analysis_1020/data/Phenotype_algorithm_v3/MRI_CT_ECHO_CARDIO/features/'+ topic +'_features.xlsx', index =False) 
    return merged_df

def replace_repeat_terms(df):
    df['impression']=df['impression'].str.replace("hypoplastic LV", "hypoplastic left ventricle", case= False)
    df['impression']=df['impression'].str.replace('hlhs', 'hypoplastic left heart syndrome', case= False)
    df['impression']=df['impression'].str.replace('HLHS', 'hypoplastic left heart syndrome', case= False)
    df['impression']=df['impression'].str.replace("no fontan", "", case= False)
    df['impression']=df['impression'].str.replace("no tricuspid atresia", "", case= False)
    df['impression']=df['impression'].str.replace("no hlhs", "", case= False)
    df['impression']=df['impression'].str.replace("no hypoplastic left heart syndrome", "", case= False)
    df['impression']=df['impression'].str.replace("no norwood", "", case= False)
    return df

def check_word(word, text, patterns):
    return 1 if patterns[word].search(text) else 0

# Function to create a DataFrame to check all words in multiple texts
def apply_check(df,words,patterns):
    for word in words:
        df[word] = df['impression'].apply(lambda x: check_word(word, x, patterns))
    return df
    
def merge_dob(df):
    path0 = r'U:\HangXu\SVP\data_analysis\data_analysis_25000\excel_data\random_validation_phenotyping_algorithm\random_patient_id\adjudication_case_2500.xlsx'
    Pat_Identifier= pd.read_excel(path0, header= 0)

    columns = ['ip_patient_id','mrn','dob']
    df0 = Pat_Identifier[columns]
    merged_df = pd.merge(df, df0, on='ip_patient_id', how='left') 
    return merged_df

def impression_merging(df1,df2):
    merged_df1 = pd.merge(df1, df2, on='ip_patient_id', how='outer', suffixes=('_df1', '_df2'))
    merged_df1['mrn'] = merged_df1[['mrn_df1', 'mrn_df2']].max(axis=1)
    merged_df1['age'] = merged_df1[['age_df1', 'age_df2']].max(axis=1)
    merged_df1['fontan'] = merged_df1[['fontan_df1', 'fontan_df2']].max(axis=1)
    merged_df1['single ventricle'] = merged_df1[['single ventricle_df1', 'single ventricle_df2']].max(axis=1)
    merged_df1['hypoplastic left ventricle'] = merged_df1[['hypoplastic left ventricle_df1', 'hypoplastic left ventricle_df2']].max(axis=1)
    merged_df1['tricuspid atresia'] = merged_df1[['tricuspid atresia_df1', 'tricuspid atresia_df2']].max(axis=1)
    merged_df1['double inlet ventricle'] = merged_df1[['double inlet ventricle_df1', 'double inlet ventricle_df2']].max(axis=1)
    merged_df1['hypoplastic left heart syndrome'] = merged_df1[['hypoplastic left heart syndrome_df1',
            'hypoplastic left heart syndrome_df2']].max(axis=1)
    merged_df1['norwood'] = merged_df1[['norwood_df1', 'norwood_df2']].max(axis=1)   
    merged_df1['good biventricular size'] = merged_df1[['good biventricular size_df1', 'good biventricular size_df2']].max(axis=1) 
    merged_df1['rastelli'] = merged_df1[['rastelli_df1', 'rastelli_df2']].max(axis=1) 
    merged_df1['1.5 ventricle repair'] = merged_df1[['1.5 ventricle repair_df1', '1.5 ventricle repair_df2']].max(axis=1) 
    merged_df1['biventricle repair'] = merged_df1[['biventricle repair_df1', 'biventricle repair_df2']].max(axis=1) 
    merged_df1 = merged_df1.dropna(subset=['mrn'])
    return merged_df1

def icd123(df0,path, topic):
    df = pd.read_excel(path, header= 0)
    merged_df1 = pd.merge(df, df0, on='ip_patient_id', how='left')
    merged_df1 = merged_df1 [(merged_df1 .drop(columns=['ip_patient_id','mrn','age']) != 0).any(axis=1)]
    merged_df1.to_excel('U:/HangXu/SVP/data_analysis/Data_analysis_1020/data/Phenotype_algorithm_v3/MRI_CT_ECHO_CARDIO/result/' +topic +'_merged.xlsx', index =False) 
    return merged_df1

def filtering(df1):
    condition1 = df1['fontan']== 1
    condition2 = df1['fontan']== 0
    condition3 = df1['age'] <=25
    condition4 = df1['single ventricle'] == 1
    #condition5 = df1['hypoplastic left ventricle'] == 1 
    condition6 = df1['tricuspid atresia'] == 1 
    condition7 = df1['double inlet ventricle'] == 1
    condition8 = df1['hypoplastic left heart syndrome'] == 1
    condition9 = df1['norwood'] == 1 
    condition10 = df1['rastelli'] == 0
    condition11 = df1['good biventricular size'] == 0
    condition12 = df1['1.5 ventricle repair'] == 0
    condition13 = df1['biventricle repair'] == 0
    df11 = df1[condition1 ]
    df12 = df1[condition2 & condition3 &( condition4| condition6|condition7| condition8|condition9 )& condition10 & condition11 & condition12 & condition13]
    return df11, df12 

def groupby_impression():
    path1 = r'U:\HangXu\SVP\data_analysis\Data_analysis_1020\Nguyen_22_17_000032\Imaging_Impressions.xlsx'
    df1 = pd.read_excel(path1, header= 0)
    pd.set_option('display.max_colwidth', None)
    df2 = df1.groupby('ip_order_proc_id')['impression'].apply(lambda x: ''.join(x.to_string(index=False))).str.replace('\n', ' ').str.replace('\t', '').str.replace('      ', ' ').str.strip().reset_index()
    df2.to_excel(r"U:\HangXu\SVP\data_analysis\Data_analysis_1020\data\Phenotype_algorithm_v3\MRI_CT_ECHO_CARDIO\imaging_impression\merged_imaging_impressions.xlsx")        
    df_echo, df_mri, df_ct = separate_impression(df2)
    df_car_con = cardiology_consultation()
    return df_echo, df_mri, df_ct, df_car_con 

def cardiology_consultation():
    path = r"U:\HangXu\SVP\data_analysis\Data_analysis_1020\Nguyen_22_17_000032\Provider_Notes.xlsx"
    df = pd.read_excel(path, header= 0)
    df1 = df[df['note_text'].str.contains('cardiology consultation', na=False, case=False)]
    df1 = df1.dropna(subset=['note_text'])
    df1 =df1[['ip_patient_id', 'create_datetime','note_text']]
    df1 = df1.rename(columns={'create_datetime': 'result_time', 'note_text': 'impression'})
    df1.to_excel(r"U:\HangXu\SVP\data_analysis\Data_analysis_1020\data\Phenotype_algorithm_v3\MRI_CT_ECHO_CARDIO\impressions\cardiology_consultation_impressions.xlsx")        
    return df1

def separate_impression(df1):
    path = r'U:\HangXu\SVP\data_analysis\Data_analysis_1020\Nguyen_22_17_000032\Imaging.xlsx'
    df = pd.read_excel(path, header= 0)
    df0 = df[df['procedure_name'].astype(str).str.contains('ECHO', na=False, case=False)].reset_index()
    df_echo = df0.merge(df1, on = 'ip_order_proc_id', how = 'left')
    df_echo = df_echo.dropna(subset=['impression'])
    #df_echo = df_echo[['ip_patient_id', 'ip_order_proc_id','impression']]
    df_echo.to_excel(r"U:\HangXu\SVP\data_analysis\Data_analysis_1020\data\Phenotype_algorithm_v3\MRI_CT_ECHO_CARDIO\impressions\ECHO_impressions.xlsx")        

    df0 = df[df['procedure_name'].astype(str).str.contains('MR', na=False, case=False)].reset_index()
    df_mri = df0.merge(df1, on = 'ip_order_proc_id', how = 'left')
    df_mri = df_mri.dropna(subset=['impression'])
    #df_mri = df_mri[['ip_patient_id', 'ip_order_proc_id','impression']]
    df_mri.to_excel(r"U:\HangXu\SVP\data_analysis\Data_analysis_1020\data\Phenotype_algorithm_v3\MRI_CT_ECHO_CARDIO\impressions\MRI_impressions.xlsx")        

    df0 = df[df['procedure_name'].astype(str).str.contains('CT CHEST', na=False, case=False)].reset_index()
    df_ct = df0.merge(df1, on = 'ip_order_proc_id', how = 'left') 
    df_ct = df_ct.dropna(subset=['impression'])
    #df_ct = df_ct[['ip_patient_id','ip_order_proc_id', 'impression']]
    df_ct.to_excel(r"U:\HangXu\SVP\data_analysis\Data_analysis_1020\data\Phenotype_algorithm_v3\MRI_CT_ECHO_CARDIO\impressions\CT_impressions.xlsx")        
    return df_echo, df_mri, df_ct

if __name__ == "__main__":
    df_echo, df_mri, df_ct, df_car_con = groupby_impression()
    df_echo = impression2features(df_echo, topic= 'echo')
    df_mri = impression2features(df_mri, topic= 'mri')
    df_ct = impression2features(df_ct, topic= 'ct')
    df_car_con = impression2features(df_car_con, topic= 'cardiology consultation')
    
    merged_df1 = impression_merging(df_echo,df_mri)
    merged_df2 = impression_merging(df_ct,df_car_con)
    merged_df = impression_merging(merged_df1,merged_df2)
    new_order = ['ip_patient_id','mrn','age','fontan','single ventricle', 'hypoplastic left ventricle', 'tricuspid atresia', 'double inlet ventricle','hypoplastic left heart syndrome',
                 'norwood','good biventricular size', 'rastelli', '1.5 ventricle repair', 'biventricle repair']
    df = merged_df[new_order]
    df.to_excel(r'U:\HangXu\SVP\data_analysis\Data_analysis_1020\data\Phenotype_algorithm_v3\MRI_CT_ECHO_CARDIO\imaging_impression\echo_mri_ct_cardiology_impressions.xlsx', index =False) 
    
    path1 = r'U:\HangXu\SVP\data_analysis\Data_analysis_1020\data\Phenotype_algorithm_v3\ICD_Table123\svp_t1_icd_mrn_1020.xlsx'
    df_t1 = icd123(df,path1, topic= 'icd_t1')
    path2 = r'U:\HangXu\SVP\data_analysis\Data_analysis_1020\data\Phenotype_algorithm_v3\ICD_Table123\svp_t2_icd_mrn_1020.xlsx'
    df_t2 = icd123(df,path2, topic= 'icd_t2')
    path3 = r'U:\HangXu\SVP\data_analysis\Data_analysis_1020\data\Phenotype_algorithm_v3\ICD_Table123\svp_t3_icd_mrn_1020.xlsx'
    df_t3 = icd123(df,path3, topic= 'icd_t3')
        
    df11, df12 = filtering(df_t1)
    df21, df22 = filtering(df_t2)
    df31, df32 = filtering(df_t3)
    df = pd.concat([df11, df12, df21, df22, df31, df32], axis=0)
    df.to_excel(r"U:\HangXu\SVP\data_analysis\Data_analysis_1020\data\Phenotype_algorithm_v3\MRI_CT_ECHO_CARDIO\result\phenotyping_algorithms_v4_result.xlsx", index=False)
    
   