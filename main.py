# -*- coding: utf-8 -*-
"""
Created on Thu Jun 12 17:01:47 2025

@author: HangXu
"""
import pandas as pd
import os
import argparse
from utils.merging_impression_narrative import groupby_impression_narrative
from utils import impression2features, impression_merging, normalized_lvedv
from utils.icd_chart_categorize import filtering, icd_chart

def argParser():
    parser = ArgumentParser()

    # data paths
    parser.add_argument(
        "--data_dir",
        help="data directory",
        default="Data",
        type=str,
    )
    parser.add_argument(
        "--save_dir",
        help="save directory",
        default="Save",
        type=str,
    )

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    # argparse arguments
    args = argParser()

    # mering the notes from MRI, CT, ECHO and cardiology consultation reports 
    df_echo, df_mri, df_ct, df_car_con, df_merge_img_nar, df_imaging = groupby_impression_narrative(args.data_dir)
    
    # extract the features from the notes
    df_echo = impression2features(df_echo, 'echo', args.data_dir)
    df_mri = impression2features(df_mri, 'mri', args.data_dir)
    df_ct = impression2features(df_ct, 'ct', args.data_dir)
    df_car_con = impression2features(df_car_con, 'cardiology consultation', args.data_dir)
    
    # merging the features from ECHO, MRI, CT and cardiology reports
    merged_df1 = impression_merging(df_echo,df_mri)
    merged_df2 = impression_merging(df_ct,df_ct)
    merged_df = impression_merging(merged_df1,merged_df2)
    merged_df = normalized_lvedv(merged_df, df_merge_img_nar, df_imaging)
    new_order = ['ip_patient_id','mrn','age','fontan','single ventricle', 'hypoplastic left ventricle', 'tricuspid atresia', 'double inlet ventricle','hypoplastic left heart syndrome',
                 'norwood','good biventricular size', 'rastelli', '1.5 ventricle repair', 'biventricle repair','Normalized_LVEDV']
    df = merged_df[new_order]
    df.to_excel(os.path.join(args.save_dir, 'echo_mri_ct_cardiology_impressions.xlsx'), index=False)

    df_t1, df_t2, df_t3 = icd_chart(args.data_dir)
            
    df11, df12 = filtering(df_t1)
    df21, df22 = filtering(df_t2)
    df31, df32 = filtering(df_t3)
    df = pd.concat([df11, df12, df21, df22, df31, df32], axis=0)
    df = df.drop_duplicates()
    df.to_excel(os.path.join(args.save_dir, 'SVP_list_mrn_icd_features.xlsx', index=False)
