# -*- coding: utf-8 -*-
"""
Created on Thu Jun 12 17:01:56 2025

@author: HangXu
"""
import pandas as pd
def impression_merging(df1, df2):
    '''
    df1 (pd.DataFrame): dataframe1 to be merged  
    df2 (pd.DataFrame): dataframe2 to be merged
    '''
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
