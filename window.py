# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 11:29:43 2023

@author: wz
窗口程序
"""

import tkinter as tk
from tkinter import filedialog
from autotable import data_processing


#%% output path of file
def select_file():
    filepath = filedialog.askopenfilenames()
    # 调用数据处理函数，将 filepath 传递给它
    da = data_processing(filepath)
    da.compute()
    if filepath:
        print(filepath)
        lb.config(text='\n'.join(filepath))
        
    else:
        lb.config(text = '您没有选择任何文件')
#%% 
root = tk.Tk()
root.title('报表自动化处理')
root.geometry('600x300')
button = tk.Button(root, text='请选择指定文件', command=select_file)
button.pack()
lb = tk.Label(root,text='',bg='#87CEEB')
lb.pack()
root.mainloop()