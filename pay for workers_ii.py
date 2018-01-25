# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 06:42:26 2018

@author: jlhobson
"""

#Import everything
import numpy as np
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import os
import math
pd.set_option('display.max_rows', 2000)
pd.set_option('display.max_columns', 300)
# <codecell>

# Import
df1 = pd.read_excel(
'C:\\Users\\jlhobson\\Documents\\_Research\\Endogenous Persuasion\\Payment (Word Scramble 201 202  301).xlsx')
df2 = pd.read_csv(
'C:\\Users\\jlhobson\\Documents\\_Research\\Endogenous Persuasion\\Data_EndPer\\roster_download_EndPer1-SP1.csv')
df3 = pd.read_csv(
'C:\\Users\\jlhobson\\Documents\\_Research\\Endogenous Persuasion\\Data_EndPer\\roster_download_EndPer2-SP2.csv')
# <codecell>

# Merge
    #prep merge
df1 = df1.rename(index=str, columns={'ID': 'id_code',})
    #concatenate the two participant ones
df23 = pd.concat([df2, df3])
    #merge
dfc1 = pd.merge(df1, df23, how='left', on=['id_code'])
    #delete duplicate
dfc1.drop_duplicates(subset='email', keep='last', inplace=True)
# <codecell>

# Calculate payment
    #Payment for total got correct so that the rate is about $12 an hour
    #average time was about 45 minutes, so average payment of $12, just round up to an hour, so $12 an hour
    #average score was 323, so payment rate should be 26.92 (323/12) correct per dollar
dfc1['final_payment'] = dfc1['Sum of TOTAL SCORE'] * 12/323 

dfc1['final_cash'] = (np.ceil(dfc1['final_payment'] / float(0.25)) * 0.25)

dfc1['tens'] = dfc1['final_cash'] // 10
dfc1['decimal'] = dfc1['final_cash'] % 1
dfc1['ones'] = dfc1['final_cash'] % 10 -dfc1['decimal'] 

dfc1['num_twenties'] = np.where(dfc1['tens'] >=2, (dfc1['tens'] / 2) - (dfc1['tens'] % 2), 0)
dfc1['num_tens'] =  dfc1['tens'] % 2
dfc1['num_fives'] = np.where(dfc1['ones'] >= 5, 1, 0)
dfc1['num_ones'] = np.where(dfc1['ones'] >= 5, dfc1['ones'] - 5, dfc1['ones'])
dfc1['num_quarters'] = dfc1['decimal'] / 0.25
# <codecell>

#export payment file
dfexport = dfc1[[
        'first_name',
        'last_name',
        'email',
        'Sum of TOTAL SCORE',
        'final_payment',
        'final_cash',
        'num_twenties',
        'num_tens',
        'num_fives',
        'num_ones',
        'num_quarters'
        ]]
dfexport = dfexport.sort_values(['last_name', 'first_name'], ascending = [True, True])
#export no-payment list
dfexport2 = df23[['email']] 
#One excel file
writer = pd.ExcelWriter(
'C:\\Users\\jlhobson\\Documents\\_Research\\Endogenous Persuasion\\Final Payment File Fall2017.xlsx', 
        engine='xlsxwriter')
dfexport.to_excel(writer, sheet_name='Paid')
dfexport2.to_excel(writer, sheet_name='Everyone') 
writer.save() 
