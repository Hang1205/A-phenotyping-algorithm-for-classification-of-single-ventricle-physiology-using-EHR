# -*- coding: utf-8 -*-
"""
Created on Thu Jun 12 17:00:31 2025

@author: HangXu
"""
import pandas as pd
import re
def normalized_lvedv(df0, df, df1):
    '''
    df0 (pd.DataFrame): dataframe to be merged
    df (pd.DataFrame): dataframe for merged imaging narratives
    '''
    df['impression'] = df['impression'].astype(str)
    df['Normalized_LVEDV'] = df['impression'].apply(extract_normalized_lvedv)
    # Optionally drop rows with missing normalized LVEDV values
    df= df.dropna(subset=['Normalized_LVEDV'])
    # Save the updated DataFrame to a new Excel file
    #path1 = r'U:\HangXu\SVP\data_analysis\data_analysis_25000\EHR_2500_random_validation\Imaging.csv'
    #df1 = pd.read_csv(path1, header= 0)
    df1 =df1[['IP_PATIENT_ID','IP_ORDER_PROC_ID','RESULT_TIME','PROCEDURE_NAME']]
    df1 = df1.rename(columns={'IP_PATIENT_ID':'ip_patient_id', 'IP_ORDER_PROC_ID': 'ip_order_proc_id', 'RESULT_TIME': 'result_time', 'PROCEDURE_NAME':'procedure_name'})
    
    df2 = df.merge(df1, on = 'ip_order_proc_id', how = 'left')  
    df2 = df2[['ip_patient_id','Normalized_LVEDV']]
    #output_file_path = r"U:\HangXu\SVP\data_analysis\data_analysis_25000\excel_data\validation_2500\imaging_impressions\SVP_MRI_Normalized_LVEDV.xlsx"
    df3 = df0.merge(df2, on = 'ip_patient_id', how = 'left')
    #df3.to_excel(output_file_path, index=False)
    return df3

def extract_normalized_lvedv(text):
    normalized_lvedv_patterns = [
        r'Normalized\s+LVEDV\s*:\s*(\d+\.?\d*)\s*ml/m2',
        r'Normalized\s+End\s+Diastolic\s+Volume\s*:\s*(\d+\.?\d*)\s*ml/m2',
        r'Normalized\s+End\s+Diastolic\s+Volume\s*(\d+\.?\d*)\s*ml/m2',
        r'Normalized\s+LVEDV\s*=\s*(\d+\.?\d*)\s*ml/m2',
        r'LVEDV\s*normalized\s*:\s*(\d+\.?\d*)\s*ml/m2',
    ]

    lvedv_patterns = [
        r'(?:LVEDV|Left\s+Ventricle\s+End\s+Diastolic\s+Volume|Left\s+Ventricular\s+End\s+Diastolic\s+Volume)[^\d]*(\d+\.?\d*)\s*ml',
        r'(?:LVEDV|Left\s+Ventricle\s+End\s+Diastolic\s+Volume|Left\s+Ventricular\s+End\s+Diastolic\s+Volume)\s*:\s*(\d+\.?\d*)\s*ml'
    ]

    bsa_patterns = [
        r'(?:BSA|Body\s+Surface\s+Area)[^\d]*(\d+\.?\d*)\s*m2',
        r'(?:BSA|Body\s+Surface\s+Area)\s*:\s*(\d+\.?\d*)\s*m2',
        r'(?:BSA|Body\s+Surface\s+Area)\s*=\s*(\d+\.?\d*)\s*m2',
        r"BSA of (\d+\.\d+) sq m",
        r"BSA of (\d+\.\d+) m2",
        r"BSA, (\d+\.\d+) mm",
        r"BSA, (\d+\.\d+) cm"
    ]
    if not isinstance(text, str):
        return None
    for pattern in normalized_lvedv_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return float(match.group(1))
    lvedv = None
    bsa = None
    # Try matching LVEDV patterns
    for pattern in lvedv_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            lvedv = float(match.group(1))
            break
    # Try matching BSA patterns
    for pattern in bsa_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            bsa = float(match.group(1))
            break
    if lvedv is not None and bsa is not None and bsa != 0:
        return lvedv / bsa
    else:
        return None
