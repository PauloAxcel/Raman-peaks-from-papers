import slate3k as slate
import os
from tqdm import tqdm
from PyPDF2 import PdfFileReader
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
from PIL import Image
import pytesseract
import argparse
import cv2
import os
from pdf2image import convert_from_path

pdf_files = []

os.chdir(r"C:\Users\paulo\OneDrive - University of Birmingham\Desktop\birmingham_02\saliva\GUI for raman analysis\reading raman values from papers\saliva\test")

for file in os.listdir():
    if file.split('.')[-1] == 'pdf':
        pdf_files.append(file)


pytesseract.pytesseract.tesseract_cmd =  r'C:\Program Files\Tesseract-OCR\tesseract.exe'
poppler_path = r'C:\Users\paulo\OneDrive - University of Birmingham\Desktop\birmingham_02\articles\saliva\poppler-21.03.0\Library\bin'


for f in pdf_files:
    all_string = []

    new_string = [] 

    pages = convert_from_path(f,poppler_path=poppler_path)   
    for p in pages:
        text = pytesseract.image_to_string(p)
        string = list(filter(None,text.split('\n')))
        for s in string:
            new_string.append(list(filter(None,s.split('\x00'))))
        flat_s = [item for sublist in new_string for item in sublist]
#            string = ''.join(string).split('.')
        b_string = ' '.join(flat_s).split('. ')
#            numbers =  re.findall(r"[-+]?\d*\.\d+|\d+",b_string)
#            print(b_string)
#            print('\n')
        all_string.append(b_string)

    
    
    all_string = pd.DataFrame(all_string).T
    all_string.columns = list(range(len(pages)))
    
    info_to_obtain = 'cm'
    info = []
    numbers = []
    
    for m in range(len(pages)):
        all_string_clean = all_string.iloc[:,m].replace(to_replace='None', value=np.nan).dropna()
        info.append(all_string_clean[all_string_clean.str.contains(info_to_obtain)].tolist())
    
    
    flat = list(set([item for sublist in info for item in sublist]))
    
    final_num = []
    
    #range for a control check
    low = 100
    high = 3200
    
    final_df = []
    
    for t in flat:
        numbers = re.findall(r"[-+]?\d*\.\d+|\d+ "+info_to_obtain, t)
    #        if detect_special_characer(t):
    #            pass
    #        else:
        for n in numbers:
            if len(n.split(' ')) !=1:
                n = n.split(' ')[0]
            if (float(n)>low and float(n)<high):
                t = ' '.join(t.split(','))
                t = re.sub('[^a-zA-Z0-9\n\.]', ' ', t)
                final_df.append([n,t])
        
    final_df = pd.DataFrame(final_df,columns=['center','label'])
    final_df['height'] = [1]*final_df.shape[0]
    final_df['importance'] = ['major']*final_df.shape[0]
    final_df['width'] = [1]*final_df.shape[0]
    
    final_df.to_csv('peaks_'+f+'.csv',index=False,sep=';')

