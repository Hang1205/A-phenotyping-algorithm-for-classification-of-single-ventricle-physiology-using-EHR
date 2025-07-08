# -*- coding: utf-8 -*-
"""
Created on Thu Jun 12 16:52:54 2025

@author: HangXu
"""
import pandas as pd
import os

def groupby_impression_narrative(data_dir, filenames=['Imaging_Impressions.csv', 'Imaging_Narratives.csv']):
    '''
    data_dir (str): data directory
    filenames (list): (default: ['Imaging_Impressions.csv', 'Imaging_Narratives.csv'])
    '''
    path1 = os.path.join(data_dir, filenames[0])
    path2 = os.path.join(data_dir, filenames[1])
    df1 = pd.read_csv(path1, header= 0)
    df1 =df1[['IP_ORDER_PROC_ID','IMPRESSION']]
    df1 = df1.rename(columns={'IP_ORDER_PROC_ID': 'ip_order_proc_id', 'IMPRESSION':'impression'})
    df2 = pd.read_csv(path2, header= 0)
    df2 =df2[['IP_ORDER_PROC_ID','NARRATIVE']]
    df2 = df2.rename(columns={'IP_ORDER_PROC_ID': 'ip_order_proc_id', 'NARRATIVE':'narrative'})
    pd.set_option('display.max_colwidth', None)
    df1 = df1.groupby('ip_order_proc_id')['impression'].apply(lambda x: ''.join(x.to_string(index=False))).str.replace('\n', ' ').str.replace('\t', '').str.replace('      ', ' ').str.strip().reset_index()
    df2 = df2.groupby('ip_order_proc_id')['narrative'].apply(lambda x: ''.join(x.to_string(index=False))).str.replace('\n', ' ').str.replace('\t', '').str.replace('      ', ' ').str.strip().reset_index()
    df2 = df2.rename(columns={'narrative': 'impression'})
    
    df= pd.concat([df1, df2], ignore_index= False)
    df_echo, df_mri, df_ct, df_imaging = separate_impression(df, data_dir)
    df_car_con = cardiology_consultation(data_dir, filename)
    return df_echo, df_mri, df_ct, df_car_con, df2, df_imaging

def separate_impression(df1, data_dir, filename='Imaging.csv'):
    '''
    df1 (pd.DataFrame): dataframe to be merged 
    data_dir (str): data directory
    filename (str): (default: 'Imaging.csv')
    '''
    path = os.path.join(data_dir, filename)
    df = pd.read_csv(path, header= 0)
    df = df[['IP_PATIENT_ID','IP_ORDER_PROC_ID','RESULT_TIME','PROCEDURE_NAME']]
    df = df.rename(columns={'IP_PATIENT_ID':'ip_patient_id', 'IP_ORDER_PROC_ID': 'ip_order_proc_id', 'RESULT_TIME': 'result_time', 'PROCEDURE_NAME':'procedure_name'})
    
    df0 = df[df['procedure_name'].astype(str).str.contains('ECHO', na=False, case=False)].reset_index()
    df_echo = df0.merge(df1, on = 'ip_order_proc_id', how = 'left')
    df_echo = df_echo.dropna(subset=['impression'])

    df0 = df[df['procedure_name'].astype(str).str.contains('MR CARDIAC', na=False, case=False)].reset_index()
    df_mri = df0.merge(df1, on = 'ip_order_proc_id', how = 'left')
    df_mri = df_mri.dropna(subset=['impression'])

    df0 = df[df['procedure_name'].astype(str).str.contains('CT CHEST', na=False, case=False)].reset_index()
    df_ct = df0.merge(df1, on = 'ip_order_proc_id', how = 'left') 
    df_ct = df_ct.dropna(subset=['impression'])
    return df_echo, df_mri, df_ct, df

def cardiology_consultation(data_dir, filename='Provider_Notes.csv'):
    '''
    data_dir (str): data directory
    filename (str): (default: 'Provider_Notes.csv')
    '''
    path = os.path.join(data_dir, filename)
    df = pd.read_csv(path, header= 0)
    df =df[['IP_PATIENT_ID','CREATE_DATETIME', 'NOTE_TEXT']]
    df = df.rename(columns={'IP_PATIENT_ID': 'ip_patient_id', 'CREATE_DATETIME': 'result_time', 'NOTE_TEXT': 'impression'})
    df1 = df[df['impression'].str.contains('cardiology consultation', na=False, case=False)]
    df1 = df1.dropna(subset=['impression'])
    return df1
