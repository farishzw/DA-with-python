# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 16:46:43 2023

@author: wz
"""

#import os
import pandas as pd 
#import numpy as np
    
#%% load data function
class data_processing:
    
    def __init__(self, filetuple):
        self.filetuple = filetuple
        
    def batch_read_xlsx_files(self):
        """
    
        Parameters
        ----------
        filenames : String
            文件路径元组.
    
        Returns
        -------
        merged df 合并的数据框.
    
        """
        #逐个读取文件内容并合并为一个Dataframe
        dataframes = []
        for file in self.filetuple:
            #读取excel，第7行作为列名
            df = pd.read_excel(file,header = 6)
            #合计行以下的数据行删掉
            index_to_stop = df[df['渠道']=='合计：'].index[0]
            df = df.iloc[:index_to_stop]
            #将数据列的类型统一成float64
            for col in df.columns[1:]:
                df[col] = pd.to_numeric(df[col],errors ='coerce')#无法转换为数值转为缺失值
            df = df.iloc[:,:12]
            #获取城市名
            city_name = file.split('）')[-1].replace('.xlsx','')
            #添加城市字段
            df['城市'] = city_name
            dataframes.append(df)
        #将多个Dataframe合并成一个Dataframe
        merged_df = pd.concat(dataframes,ignore_index=True)
        return merged_df
   # #%% load data
   # folder_path = 'C:/Users/wz/Desktop'
   # result_df = batch_read_xlsx_files(folder_path)
    #根据城市计算交易信息
    def compute(self):
        result_df=self.batch_read_xlsx_files()
        summary_df = result_df.groupby('城市').sum(numeric_only = True)
    #电子自助渠道识别
        electronic_channels = ['手机银行','移动柜台','网上银行']
        result_df['电子渠道'] = result_df['渠道'].isin(electronic_channels)
        summary_df_elec = result_df.groupby(['城市','电子渠道']).sum(numeric_only=True)
        output_df = summary_df.copy()/10000
        output_df['个人结售汇收入本期余额（万元）'] = output_df['购汇收入（元）']+output_df['结汇收入（元）']
        output_df['个人结售汇交易量（万笔）'] = output_df['结汇笔数']+output_df['购汇笔数']
        output_df['个人结售汇交易金额（万美元）']= output_df['购汇金额折美元']+output_df['结汇金额折美元']
        output_df['电子自助渠道交易额'] = list((summary_df_elec.loc[pd.IndexSlice[:, True],'购汇金额折美元']+summary_df_elec.loc[pd.IndexSlice[:, True],'结汇金额折美元'])/10000)
        output_df['电子自助渠道结售汇收入'] = list((summary_df_elec.loc[pd.IndexSlice[:, True],'购汇收入（元）']+summary_df_elec.loc[pd.IndexSlice[:, True],'结汇收入（元）'])/10000)
        output_df=output_df.drop(['购汇金额（元）','结汇金额（元）','合计笔数','合计金额（元）','合计收入（元）'],axis=1)
        output_df.rename(columns={'购汇笔数':'购汇交易量（万笔）','购汇金额折美元':'购汇交易金额（万美元）','购汇收入（元）':'购汇收入','结汇笔数':'结汇交易量（万笔）',
                          '结汇金额折美元':'结汇交易金额（万美元）','结汇收入（元）':'结汇收入'},inplace=True)
        output_df.rename(index={'jx':'江西','nc':'洪都','jdz':'景德镇','px':'萍乡',
                                'jj':'九江','xy':'新余','yt':'鹰潭','gz':'赣州',
                                'yc':'宜春','sr':'上饶','ja':'吉安','fz':'抚州'},inplace=True)
        output_df.loc['江西(汇总)'] =output_df.sum(axis=0) 
        col_order = ['个人结售汇收入本期余额（万元）','个人结售汇交易量（万笔）','个人结售汇交易金额（万美元）',
                     '购汇交易量（万笔）','购汇交易金额（万美元）','购汇收入',
                     '结汇交易量（万笔）','结汇交易金额（万美元）','结汇收入',
                     '电子自助渠道交易额','电子自助渠道结售汇收入']
        output_df=output_df[col_order]
        
        indexorder=['江西(汇总)','洪都','景德镇','萍乡','九江',
                    '新余','鹰潭','赣州','宜春','上饶','吉安','抚州']
        sorted_index = sorted(output_df.index,key = lambda name:indexorder.index(name))
        output_df = output_df.reindex(sorted_index)
        folder_path = '/'.join(self.filetuple[0].split('/')[:-1])
        output_df.to_excel(f"{folder_path}/output.xlsx", index=True)

