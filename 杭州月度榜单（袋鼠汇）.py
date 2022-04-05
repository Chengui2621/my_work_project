#!/usr/bin/env python
# coding: utf-8

# # 导包

# In[ ]:


import re
import numpy as np
import pandas as pd
import os
import xlwt
import xlrd
import openpyxl
import xlsxwriter
import datetime
from xlutils import copy
from openpyxl import load_workbook
from xlrd import open_workbook


# In[ ]:


from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = 'all'


# # 参数设置

# In[ ]:


date = datetime.date.today()
month = str(date.month) + '月'
month


# <b><font size=1 color=green>特殊时间段：</font></b>

# In[ ]:


month = '一季度'


# # 导入数据

# In[ ]:


block_dir = '原始数据/' + month + '/'
block_data_file_path = os.listdir(block_dir)


# In[ ]:


for file in os.listdir(block_dir):
    if '新房' in file:
        new_house_data = pd.read_excel(block_dir + file, dtype=object)
    if '住宅' in file and '非' not in file:
        house_data = pd.read_excel(block_dir + file, dtype=object)
    if '非住宅' in file:
        non_house_data = pd.read_excel(block_dir + file, dtype=object)
    if '全市' in file:
        all_data = pd.read_excel(block_dir + file, dtype=object)


# ## 楼市排行榜

# ### 计算排行

# In[ ]:


new_house_data = new_house_data.drop(0)[['项目名称', '城区', '成交套数', '成交面积(㎡)', '预测成交总价(万元)', '预测成交均价(元/㎡)']]
new_house_data.columns = ['项目名称', '所属区域', '签约套数', '签约面积（㎡）', '签约金额（万元）', '签约均价（元/㎡）']

new_house_data= new_house_data.replace({'祥生云湖城':'祥生银湖宸语'})
calc_data_new_house = new_house_data.copy()
new_house_data.head()


# In[ ]:


merge_data = calc_data_new_house.groupby(['所属区域', '项目名称'])[['签约套数', '签约面积（㎡）', '签约金额（万元）']].sum()
merge_data.loc[:, '均价'] = merge_data.loc[:, '签约金额（万元）']*10000/merge_data.loc[:, '签约面积（㎡）']
merge_data.loc[:, ['签约面积（㎡）', '均价', '签约金额（万元）']] = round(merge_data.loc[:, ['签约面积（㎡）', '均价', '签约金额（万元）']], 0).astype(int)
merge_data = merge_data.reset_index()
merge_data.rename(columns={'均价':'签约均价（元/㎡）'},inplace=True) 
merge_data=merge_data[['项目名称', '所属区域', '签约套数', '签约面积（㎡）', '签约金额（万元）', '签约均价（元/㎡）']]
merge_data


# In[ ]:


merge_data[merge_data['签约均价（元/㎡）']<0]


# In[ ]:


# 主城区套数
main_city = ['上城区', '下城区', '江干区', '拱墅区', '西湖区', '滨江区', '钱塘新区']
main_city_quantity = merge_data[merge_data['所属区域'].isin(main_city)].sort_values(by=['签约套数', '签约面积（㎡）'], ascending=False).head(11)
main_city_quantity.insert(0, '排名', list(range(1,12,1)))
main_city_quantity


# In[ ]:


# 主城区面积
main_city_area = merge_data[merge_data['所属区域'].isin(main_city)].sort_values('签约面积（㎡）', ascending=False).head(11)
main_city_area.insert(0, '排名', list(range(1,12,1)))
main_city_area


# In[ ]:


# 萧山
xiaoshan_quantity = merge_data[merge_data['所属区域'] =='萧山区'].sort_values(by=['签约套数', '签约面积（㎡）'], ascending=False).head(11)
xiaoshan_quantity.insert(0, '排名', list(range(1,12,1)))
xiaoshan_quantity


# In[ ]:


yuhang_quantity = merge_data[merge_data['所属区域'] =='余杭区'].sort_values(by=['签约套数', '签约面积（㎡）'], ascending=False).head(11)
yuhang_quantity.insert(0, '排名', list(range(1,12,1)))
yuhang_quantity


# In[ ]:


fuyang_quantity = merge_data[merge_data['所属区域'] =='富阳区'].sort_values(by=['签约套数', '签约面积（㎡）'], ascending=False).head(11)
fuyang_quantity.insert(0, '排名', list(range(1,12,1)))
fuyang_quantity


# In[ ]:


linan_quantity = merge_data[merge_data['所属区域'] =='临安区'].sort_values(by=['签约套数', '签约面积（㎡）'], ascending=False).head(11)
linan_quantity.insert(0, '排名', list(range(1,12,1)))
linan_quantity


# ### 导出数据

# In[ ]:


file_path1 = '排行结果/' + month + '/'
if not os.path.exists(file_path1):
    os.mkdir(file_path1)
file_name1 = month + '杭州楼市成交排行榜.xlsx'
writer = pd.ExcelWriter(file_path1 + file_name1)
data_list = [
    main_city_quantity, main_city_area, xiaoshan_quantity, yuhang_quantity,
    linan_quantity, fuyang_quantity
]
row = 2
for d in data_list:
    d.to_excel(writer, startrow=row, sheet_name="新房排行", index=False)
    row += 15

# 保存
writer.save()
writer.close()

rb = xlrd.open_workbook(file_path1+file_name1)   
# rb = openpyxl.load_workbook(file_path1+file_name1)   
wb = copy.copy(rb) 
# sheets = wb.worksheets
ws = wb.get_sheet(0)    
ws.write(1, 0, '主城套数') 
ws.write(16, 0, '主城面积') 
ws.write(31, 0, '萧山套数') 
ws.write(46, 0, '余杭套数') 
ws.write(61, 0, '临安套数') 
ws.write(76, 0, '富阳套数') 
wb.save(file_path1+file_name1)  


# ## 住宅非住宅成交榜

# ### 计算排行

# In[ ]:


house_data = house_data.drop(0)[['项目名称', '城区', '成交套数', '成交面积(㎡)', '预测成交总价(万元)', '预测成交均价(元/㎡)']]
house_data.columns = ['项目名称', '所属区域', '签约套数', '签约面积（㎡）', '签约金额（万元）', '签约均价（元/㎡）']

house_data= house_data.replace({'祥生云湖城':'祥生银湖宸语'})
calc_data_house = house_data.copy()
house_data.head()


# In[ ]:


non_house_data = non_house_data.drop(0)[['项目名称', '城区', '成交套数', '成交面积(㎡)', '预测成交总价(万元)', '预测成交均价(元/㎡)']]
non_house_data.columns = ['项目名称', '所属区域', '签约套数', '签约面积（㎡）', '签约金额（万元）', '签约均价（元/㎡）']
calc_data_non_house = non_house_data.copy()
non_house_data.head()


# In[ ]:


# 住宅数据排行
merge_data_house = calc_data_house.groupby(
    ['所属区域', '项目名称'])[['签约套数', '签约面积（㎡）', '签约金额（万元）']].sum()
merge_data_house.loc[:, ['签约面积（㎡）', '签约金额（万元）']] = round(merge_data_house.loc[:, ['签约面积（㎡）', '签约金额（万元）']], 0)
merge_data_house.loc[:, '签约均价'] =(merge_data_house.loc[:, '签约金额（万元）']*10000/merge_data_house.loc[:, '签约面积（㎡）']).round().astype(int)
merge_data_house.loc[:, '均价'] = round(merge_data_house.loc[:, '签约均价'], -2)
merge_data_house = merge_data_house.reset_index()
merge_data_house.rename(columns={'签约均价': '签约均价（元/㎡）'}, inplace=True)
merge_data_house = merge_data_house[['项目名称', '所属区域', '签约套数', '签约面积（㎡）', '签约金额（万元）', '签约均价（元/㎡）', '均价']]
merge_data_house.columns = ['楼盘名称', '城区', '套数', '签约面积', '签约金额', '签约均价', '均价']
merge_data_house


# In[ ]:


merge_data_house[merge_data_house['均价']<0]


# In[ ]:


# 住宅成交榜
house_rank = merge_data_house.sort_values('套数', ascending=False).head(10)
house_rank = house_rank[['楼盘名称', '城区', '套数', '均价']]
house_rank


# In[ ]:


# 住宅均价35000以上
house_rank1 = merge_data_house[merge_data_house['签约均价']>35000].sort_values('套数', ascending=False).head(10)
house_rank1 = house_rank1[['楼盘名称', '城区', '套数', '均价']]
house_rank1


# In[ ]:


# 住宅均价20000以上35000以下
house_rank2 = merge_data_house[(merge_data_house['签约均价'] > 20000) & (
    merge_data_house['签约均价'] <= 35000)].sort_values('套数', ascending=False).head(10)
house_rank2 = house_rank2[['楼盘名称', '城区', '套数', '均价']]
house_rank2


# In[ ]:


# 住宅均价20000以下
house_rank3 = merge_data_house[merge_data_house['签约均价']<=20000].sort_values('套数', ascending=False).head(10)
house_rank3 = house_rank3[['楼盘名称', '城区', '套数', '均价']]
house_rank3


# In[ ]:


#非住宅数据排行
merge_data_non_house = calc_data_non_house.groupby(
    ['所属区域', '项目名称'])[['签约套数', '签约面积（㎡）', '签约金额（万元）']].sum()
merge_data_non_house.loc[:, ['签约面积（㎡）', '签约金额（万元）']] = merge_data_non_house.loc[:, ['签约面积（㎡）', '签约金额（万元）']].round()
merge_data_non_house.loc[:, '签约均价'] = (merge_data_non_house.loc[:,
                                                     '签约金额（万元）']*10000/merge_data_non_house.loc[:, '签约面积（㎡）']).astype(int)
merge_data_non_house.loc[:, '均价'] = round(merge_data_non_house.loc[:, '签约均价'], -2)
merge_data_non_house = merge_data_non_house.reset_index()
merge_data_non_house.rename(columns={'签约均价': '签约均价（元/㎡）'}, inplace=True)
merge_data_non_house = merge_data_non_house[[
    '项目名称', '所属区域', '签约套数', '签约面积（㎡）', '签约金额（万元）', '签约均价（元/㎡）', '均价']]
merge_data_non_house.columns = ['楼盘名称', '城区', '套数', '签约面积', '签约金额', '签约均价', '均价']
merge_data_non_house


# In[ ]:


merge_data_non_house[merge_data_non_house.loc[:, '均价']<0]


# In[ ]:


# 非住宅成交榜
non_house_rank = merge_data_non_house.sort_values('套数', ascending=False).head(10)
non_house_rank = non_house_rank[['楼盘名称', '城区', '套数', '均价']]
non_house_rank


# ### 导出数据

# In[ ]:


file_path2 = './排行结果/' + month + '/'
if not os.path.exists(file_path2):
    os.mkdir(file_path2)
file_name2 = month + '杭州新房成交榜(住宅非住宅均价).xlsx'
writer = pd.ExcelWriter(file_path2 + file_name2)

house_rank.to_excel(writer, startrow=1, startcol=0, sheet_name='Sheet1', index=False)
non_house_rank.to_excel(writer, startrow=1, startcol=5, index=False)
house_rank1.to_excel(writer, startrow=15, startcol=0, index=False)
house_rank2.to_excel(writer, startrow=15, startcol=5, index=False)
house_rank3.to_excel(writer, startrow=15, startcol=10, index=False)

# 保存
writer.save()
writer.close()

rb = xlrd.open_workbook(file_path2 + file_name2)   
wb = copy.copy(rb)                         
ws = wb.get_sheet(0)                 
ws.write(0, 0, month + '杭州市区住宅成交排名前十数据') 
ws.write(0, 5, month + '杭州市区非住宅项目成交排名前十数据') 
ws.write(14, 0, month + '杭州市区住宅均价在35000元/㎡以上成交排名前十数据') 
ws.write(14, 5, month + '杭州市区住宅均价在20000-35000元/㎡成交排名前十数据') 
ws.write(14, 10, month + '杭州市区住宅均价在20000元/㎡以下成交排名前十数据') 
wb.save(file_path2 + file_name2)  


# In[ ]:





# ## 房企排行榜

# In[ ]:


all_data = all_data.drop(0)[['项目名称', '城区', '成交套数', '成交面积(㎡)', '预测成交总价(万元)', '预测成交均价(元/㎡)']]
all_data.columns = ['楼盘名称', '所属区域', '签约套数', '签约面积（㎡）', '销售金额', '签约均价（元/㎡）']
calc_data_all = all_data.copy()
all_data.head()


# In[ ]:


file_path3 = '排行结果/' + month + '/'
if not os.path.exists(file_path3):
    os.mkdir(file_path3)


# In[ ]:


for file in os.listdir(block_dir):
    if '房企' in file:
        print(file)
        group_data_file_path = block_dir + file


# In[ ]:


table=open_workbook(group_data_file_path)   #打开文件
get_sheets = table.sheet_names()    #获取excel的sheet页的名称，全部打印出来
group_list = [[] for _ in range(len(get_sheets))]
df_list = [pd.DataFrame() for _ in range(len(get_sheets))]
for i in get_sheets:
    get_each_sheet = table.sheet_by_name(i)  #获取到每个sheet页的名称，单独打印
    print(get_each_sheet.name)
    count_rows = get_each_sheet.nrows   
    for j in range(count_rows):  
        col_values = get_each_sheet.row_values(j, start_colx=0, end_colx=None)
        group_list[get_sheets.index(i)].append(col_values)
    df_list[get_sheets.index(i)] = pd.DataFrame(group_list[get_sheets.index(i)])
    df_list[get_sheets.index(i)].columns = ['楼盘名称', '销售金额']
    df_list[get_sheets.index(i)].drop(index = 0, inplace=True)
    df_list[get_sheets.index(i)].drop('销售金额', axis=1, inplace=True)
    print(df_list[get_sheets.index(i)], '\n')


# In[ ]:


writer = pd.ExcelWriter(file_path3 + '房企榜单数据需求.xlsx')


# In[ ]:


a=0
for i in range(len(df_list)):
    df_list[i] = pd.merge(df_list[i], calc_data_all, on='楼盘名称', how='left')
    df_list[i] = df_list[i][['楼盘名称', '销售金额']]
    print(get_sheets[i])
    df_list[i].to_excel(writer, get_sheets[a], index=False)
    a = a+1
#     print(df)


# In[ ]:


writer.save()
writer.close()


# In[ ]:




