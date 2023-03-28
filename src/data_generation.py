import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
import random
import matplotlib.cm as cm
import seaborn as sns
import math


def data_generator(num):
    filePath = 'CAP_and_LIS_Case_Views.xlsx'
    # read excel file into DataFrame form 
    rawDF=pd.read_excel(filePath, sheet_name='vwEccProperties_ListItem',header=0, skiprows =range(1,672), nrows=83)


    # extract all unqie col C
    questionText = rawDF['ListItemQuestionText'].unique().tolist()
    # print(len(questionText))

    # generate a dictionary for storing datatype, categorical or numerical 
    map_of_features  = {}
    # numerical Col C names 
    num_C = ['Size of Largest Metastatic Deposit in Millimeters (mm)#',
            'Distance of Melanoma in situ from Closest Peripheral Margin in Millimeters (mm)', 
            'Distance of Melanoma in situ from Deep Margin in Millimeters (mm)', 
            'Distance of Invasive Melanoma from Closest Peripheral Margin in Millimeters (mm)',
            'Distance of Invasive Melanoma from Deep Margin in Millimeters (mm)', 
            'Number of Lymph Nodes with Tumor', 'Tumor Size']
    for i in num_C:
        map_of_features[i] = "N"
    # generate categorical list based on the numerical list 
    # cat_C = list(set(num_C).symmetric_difference(set(questionText)))
    # cat_C = list(set(questionText) - set(num_C))
    cat_C = [i for i in questionText if i not in num_C]
    # print(len(cat_C))
    print(cat_C)
    for i in cat_C:
        map_of_features[i] = "C"

    # Assign numerical and categorical data with their possible solution
    map_of_selection = {}
    for i in questionText:
        query1 = "ListItemQuestionText=='"+i+"'"
        # print(query1)
        df = rawDF.query(query1)["ListItemText"]
        # print(df)
        if i == 'Size of Largest Metastatic Deposit in Millimeters (mm)#':
            map_of_selection['Size of Largest Metastatic Deposit in Millimeters (mm)'] = df
            num_C = list(map(lambda x: x.replace('Size of Largest Metastatic Deposit in Millimeters (mm)#', 'Size of Largest Metastatic Deposit in Millimeters (mm)'), num_C))
        elif i == 'Distant Metastasis (pM) (applicable for excision only)':
            map_of_selection['Distant Metastasis (pM)'] = df
            cat_C = list(map(lambda x: x.replace('Distant Metastasis (pM) (applicable for excision only)', 'Distant Metastasis (pM)'), cat_C))
        else:
            map_of_selection[i] = df
    # tailor unecessary info 
    # Size of Largest Metastatic Deposit in Millimeters (mm)
    map_of_selection['Size of Largest Metastatic Deposit in Millimeters (mm)'] = map_of_selection['Size of Largest Metastatic Deposit in Millimeters (mm)'].drop([0])
    # print(map_of_selection['Size of Largest Metastatic Deposit in Millimeters (mm)'])
    
    # Distance of Melanoma in situ from Closest Peripheral Margin in Millimeters (mm)
    map_of_selection['Distance of Melanoma in situ from Closest Peripheral Margin in Millimeters (mm)'] = map_of_selection['Distance of Melanoma in situ from Closest Peripheral Margin in Millimeters (mm)'].drop([60,61,62])
    # print(map_of_selection['Distance of Melanoma in situ from Closest Peripheral Margin in Millimeters (mm)'])
    
    # Primary Tumor (pT)
    for index in map_of_selection['Primary Tumor (pT)'].index:
        val = map_of_selection['Primary Tumor (pT)'][index]
        if ': ' in val:
            map_of_selection['Primary Tumor (pT)'][index] = (str(val).split(': '))[0]
        else:
            map_of_selection['Primary Tumor (pT)'] = map_of_selection['Primary Tumor (pT)'].drop([index])
    # print(map_of_selection['Primary Tumor (pT)'])

    # Regional Lymph Nodes (pN)
    map_of_selection['Regional Lymph Nodes (pN)'] = map_of_selection['Regional Lymph Nodes (pN)'].drop([34])
    for index in map_of_selection['Regional Lymph Nodes (pN)'].index:
        val = map_of_selection['Regional Lymph Nodes (pN)'][index]
        if ': ' in val:
            map_of_selection['Regional Lymph Nodes (pN)'][index] = (str(val).split(': '))[0]
        else:
            map_of_selection['Regional Lymph Nodes (pN)'] = map_of_selection['Regional Lymph Nodes (pN)'].drop([index])
    # print(map_of_selection['Regional Lymph Nodes (pN)'])

    # Distant Metastasis (pM)
    map_of_selection['Distant Metastasis (pM)'] = map_of_selection['Distant Metastasis (pM)'].drop([52])
    map_of_selection['Distant Metastasis (pM)'] = map_of_selection['Distant Metastasis (pM)'].drop([54])
    for index in map_of_selection['Distant Metastasis (pM)'].index:
        val = map_of_selection['Distant Metastasis (pM)'][index]
        if ': ' in val:
            map_of_selection['Distant Metastasis (pM)'][index] = (str(val).split(': '))[0]
        else:
            map_of_selection['Distant Metastasis (pM)'] = map_of_selection['Distant Metastasis (pM)'].drop([index])
    # print(map_of_selection['Distant Metastasis (pM)'])
        
    # Pathologic Stage Classification
    map_of_selection['TNM Descriptors'][12] = "Not applicable"
    # print(map_of_selection['TNM Descriptors'])

    # Pathologic Stage Classification
    map_of_selection['Pathologic Stage Classification'] = map_of_selection['Pathologic Stage Classification'].drop([10])
    

    data = []
    data_header = ['patient']
    data_header = data_header + num_C + cat_C + ['age']
    # print(map_of_selection['Status of Melanoma In Situ at Peripheral Margins'])
    # numerical data requires 2 levels of generating data, 1st is the number
    # second is the option, such as "Specify in Millimeters (mm)","At least in Millimeters (mm)","Cannot be determined (explain)"
    for i in range(1,(num+1)):
        patient_name = "patient " + str(i)
        temp_list = [patient_name]
        for j in num_C:
            # random generated numerical value range 0-15 
            r1 = random.randint(0, 15)
            # select from the values of map_of_selection map 
            random_selection = map_of_selection[j].sample()
            temp_val = ((str(random_selection).split('  ')[2]).split('\n')[0]) + " - " + str(r1)
            if 'Cannot be determined' in temp_val:
                temp_list.append(str('Cannot be determined'))
            else:
                temp_list.append(temp_val)
            # # if only want numbers 
            # temp_list.append(r1)
        # print(temp_list)
        for k in cat_C:
            # select from the values of map_of_selection map 
            random_selection = map_of_selection[k].sample()
            temp_val = ((str(random_selection).split('  ')[2]).split('\n')[0])
            if '?Not applicable' in temp_val:
                temp_list.append(str('Not applicable'))
            elif ': ' in temp_val:
                temp_list.append(str(temp_val).split(': ')[0])
                # print("FOUNDIT")
            elif ' (' in temp_val:
                temp_list.append(str(temp_val).split(' (')[0])
            else:
                temp_list.append(temp_val)
        temp_list.append(random.randint(0,90))
        # print(temp_list)
        data.append(temp_list)
    # print(data)

    # # generate dataframe based on the list 
    patient_df = pd.DataFrame(data, columns=data_header)
    return patient_df
def main():
    # 100 patients data generation
    fake_data = data_generator(100)
    # turn to csv file 
    fake_data.to_csv('fake_data.csv', index=False)
if __name__ == "__main__":
    main()