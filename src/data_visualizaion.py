import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
import random
import matplotlib.cm as cm
import seaborn as sns
import math

    
# split fake_data according to column name 
def split_df(path, header):
    # # import data 
    patient_df = pd.read_csv(path)    
    # clean data to be desired format 
    temp_df = patient_df[header].copy()
    for j in temp_df.index:
        val = temp_df[j]
        if (' - ' in val) :
            temp_df[j] = str(val).split(' - ')[-1]
        elif val == 'int64':
            temp_df[j] = val
    temp_df = pd.concat([temp_df, patient_df['age']], axis=1)
    fileName = header.replace(" ", "_")
    # print(fileName+".csv")
    temp_df.to_csv((fileName+".csv"), index=False)


# numerical data preparation 
def prep_singular_data(path, header):
    hist_df = pd.read_csv(path, header=0)    

    label = []
    # group df vales into 4 groups, 0-5, 5-10, 10-15, not determined 
    for i in hist_df.index:
        # print(i,header)
        val = hist_df.loc[i,header]
        # print(val)
        if str(val) != 'Cannot be determined':
            val = int(val)
            if 0 <= val < 5:
                label.append(1)
            elif 5 <= val < 10:
                label.append(2)
            else:
                label.append(3)
        else:
            label.append(4)
    # add group labelling to df 
    hist_df['Label']= label
    return hist_df

# categorical data preparation
def pre_cat_data(path, header):
    hist_df = pd.read_csv(path, header=0)
    # group df vales into their appropriate groups
    unique_list = hist_df[header].unique()
    temp_occur = []
    data = dict.fromkeys(unique_list)
    for i in unique_list:
        temp_occur = []
        for k in range(0,100,10):
            # loop thru 10 age group, 0-10, 10-20 etc.. 
            temp_df = hist_df.loc[(hist_df['age'] >= k) & (hist_df['age'] < k+10)]
            # occurance of each group member 
            occurance = len(temp_df[temp_df[header] == i])
            temp_occur.append(occurance)
        data[i] = temp_occur
    # print(data)
    occur = hist_df.groupby([header]).size()
    return occur

# BAR CAHRT
def bar_char(test_df,header):
    # calculate sum of points for each team
    unique_val = test_df['Label'].unique()
    # generate data dict to plot data 
    data = {}
    for i in unique_val:
        if i == 1:
            data['0-5'] = int(test_df['Label'].value_counts()[i])
        elif i == 2:
            data['5-10'] = int(test_df['Label'].value_counts()[i])
        elif i == 3:
            data['10-15'] = int(test_df['Label'].value_counts()[i])
        else:
            data['not determined'] = int(test_df['Label'].value_counts()[i])

    # create bar plot using Dictionary
    sns.set_style('darkgrid')
    bar_plot = pd.DataFrame(data.items(), columns = ['Group','Value'])

    # # sort dataframe in appropriate order 
    # bar_plot['Group'] = pd.Categorical(bar_plot['Group'], ['0-5', '5-10', '10-15', 'not determined'])
    # bar_plot = bar_plot.sort_values('Group')

    # # plot 
    # sns.barplot(data = bar_plot, x = 'Group', y = 'Value')
    # plt.title(header)
    # plt.show()
    return bar_plot


# STACKED BAR CAHRT
def stackedbar_char(df):
    # calculate sum of points for each team
    # unique_val = df['Label'].unique()
    # generate data dict to plot data 
    data = {'0-5': [], '5-10': [], '10-15': [], 'not determined': []}
    key_list = ['0-10', '10-20', '20-30', '30-40', '40-50',
                '50-60', '60-70', '70-80', '80-90', '90-100']
    for k in range(0,100,10):
        test_df = df.loc[(df['age'] >= k) & (df['age'] < k+10)]
        unique_val = [1, 2, 3, 4]
        occurance = test_df.groupby('Label')['Label'].count()
        for i in unique_val:
            if i not in occurance:
                occurance.loc[i] = 0

        for i in unique_val:
            if i == 1:
                data['0-5'].append(int(occurance.loc[i]))
            elif i == 2:
                data['5-10'].append(int(occurance.loc[i]))
            elif i == 3:
                data['10-15'].append(int(occurance.loc[i]))
            else:
                data['not determined'].append(int(occurance.loc[i]))
    # helper print function 
    for key in data.keys():
        print("      label: "+"'"+key+"',")
        if key == '0-5':
            print("      backgroundColor: '#1d7874',")
        elif key == '5-10':
            print("      backgroundColor: '#679289',")
        elif key == '10-15':
            print("      backgroundColor: '#f4c095',")
        else:
            print("      backgroundColor: '#ee2e31',")
        print("      data: {},".format(data[key]))
        print("\n")
 
    # # create bar plot 
    # bar_plot = pd.DataFrame(data,key_list)
    # bar_plot.plot (kind = 'barh', stacked = True, color = ['pink', 'salmon', 'indianred', 'darkred'])
    # plt.ylabel("Age Group")
    # plt.xlabel("Number")
    # plt.title('Age Demographics')
    # plt.show()


# SCATTER PLOT, only process numerical data
def scatter_plt(test_df1,test_df2,header1,header2):
    x = test_df1[test_df1.Label != 4]
    y = test_df2[test_df2.Label != 4]
    df2 = pd.merge(x, y, left_index=True, right_index=True)
    df2 = df2.reset_index(drop=True)
    
    # # print in front end javascript format 
    # print("'{} vs {}': {}".format(header1,header2, [df2[header1].astype('int').tolist(), df2[header2].astype('int').tolist()]))
    # print("\n")

    # # plotting part 
    # plt.title(header1 + " vs "+ header2)
    # plt.xlim([0,16])
    # plt.ylim([0,16])
    # plt.xlabel(header1)
    # plt.ylabel(header2)
    # plt.scatter(df2[header1].astype(float),df2[header2].astype(float))
    # plt.show()


# LINE CHART, only process numerical data
def line_char(test_df1,test_df2,test_df3,header,header1,header2,header3):
    # calculate sum of points for each team
    unique_val = []
    group_list = ['0-5', '5-10', '10-15', 'not determined']
    df = pd.DataFrame(group_list, columns = ['Group'])
    df_list = [test_df1,test_df2,test_df3]
    occurance = test_df1.groupby('Label')['Label'].count()
    unique_val1 = test_df1['Label'].unique()
    unique_val.append(unique_val1)
    unique_val2 = test_df2['Label'].unique()
    unique_val.append(unique_val2)
    unique_val3 = test_df3['Label'].unique()
    unique_val.append(unique_val3)
    unique_val = unique_val1+unique_val2+unique_val3

    # generate data dict to plot data 
    data = {}
    for k in range(len(unique_val)):
        for i in unique_val[k]:
            if k == 0:
                if i == 1:
                    data['0-5'] = [int(df_list[k]['Label'].value_counts()[i])]
                elif i == 2:
                    data['5-10'] = [int(df_list[k]['Label'].value_counts()[i])]
                elif i == 3:
                    data['10-15'] = [int(df_list[k]['Label'].value_counts()[i])]
                else:
                    data['not determined'] = [int(df_list[k]['Label'].value_counts()[i])]
            else:
                if i == 1:
                    data['0-5'].append(int(df_list[k]['Label'].value_counts()[i]))
                elif i == 2:
                    data['5-10'].append(int(df_list[k]['Label'].value_counts()[i]))
                elif i == 3:
                    data['10-15'].append(int(df_list[k]['Label'].value_counts()[i]))
                else:
                    data['not determined'].append(int(df_list[k]['Label'].value_counts()[i]))                 

    key_list = ['0-5', '5-10', '10-15', 'not determined']

    for i in range(len(data[key_list[0]])):
        temp_list = []
        for value in data.values():
            temp_list.append(value[i])
            # print(temp_list)
        plt.plot(key_list, temp_list)

    plt.title(header, fontsize=12)
    plt.xlabel('result type', fontsize=12)
    plt.ylabel('number', fontsize=12)
    plt.grid(True)
    plt.legend([header1,header2,header3])
    plt.show()



def main():
    # numerical Col C names 
    num_C = ['Size of Largest Metastatic Deposit in Millimeters (mm)',
            'Distance of Melanoma in situ from Closest Peripheral Margin in Millimeters (mm)', 
            'Distance of Melanoma in situ from Deep Margin in Millimeters (mm)', 
            'Distance of Invasive Melanoma from Closest Peripheral Margin in Millimeters (mm)',
            'Distance of Invasive Melanoma from Deep Margin in Millimeters (mm)', 
            'Number of Lymph Nodes with Tumor', 'Tumor Size']
    # categorical
    cat_C = ['Extranodal Extension', 'Matted Nodes', 
             'Number of Sentinel Nodes Examined', 
             'Pathologic Stage Classification', 'TNM Descriptors', 
             'Primary Tumor (pT)', 'Regional Lymph Nodes (pN)', 
             'Distant Metastasis (pM)', 
             'Status of Melanoma In Situ at Peripheral Margins']

    #  work on numerical data first:
    for i in range(len(num_C)):
        # print(i)
        header = num_C[i]
        # split_df('csv/fake_data.csv', header)
        fileName = header.replace(" ", "_")
        test_df = prep_singular_data(("../fake_data/csv/"+fileName+".csv"), header)
        for k in range(i+1, len(num_C)):
            # print(k)
            header_Num = num_C[k]
            # generate scatter plot data 
            fileName_Num = header_Num.replace(" ", "_")
            test_df_Num = prep_singular_data(("../fake_data/csv/"+fileName_Num+".csv"), header_Num)
            scatter_plt(test_df, test_df_Num, header, header_Num)


        # generate stacked bar chart input 
        # stackedbar_char(test_df)

        # # generate bar chart input 
        # barChart_data = bar_char(test_df,header)
        # num_list = ['not determined', '0-5', '5-10', '10-15']
        # barChart_data = barChart_data.set_index('Group').reindex(index = num_list).reset_index()
        # print("'"+header+"'"+': '+str(barChart_data['Value'].tolist())+',')
        


    # #  work on categorical data first:
    # for k in cat_C:
    #     header = k
    #     # split_df('fake_data.csv', header)
    #     fileName = header.replace(" ", "_")
    #     occur_df = pre_cat_data(("../fake_data/csv/"+fileName+".csv"), header)
    #     # print(occur_df)
    #     # barChart_data = bar_char(test_df,header)
    #     # barChart_data = barChart_data.set_index('Group')
    #     # num_list = ['not determined', '0-5', '5-10', '10-15']
    #     # barChart_data = barChart_data.set_index('Group').reindex(index = num_list).reset_index()
    #     # print(barChart_data)

    # LINE CHART, only process numerical data
    # line_char(test_df,test_df2,test_df3,"Tendency",header1,header2,header3)

    # SCATTER PLOT, only process numerical data
    # scatter_plt(test_df,test_df2,
    #             "Size of Largest Metastatic Deposit v.s. Distance of Melanoma in situ from Closest Peripheral Margin", 
    #             header1,header2)

    # BAR CAHRT
    # bar_char(test_df,header1)

    # STACKED BAR CAHRT
    # stackedbar_char(test_df)
if __name__ == "__main__":
    main()