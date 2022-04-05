import pymysql
import xlwt
import pandas as pd
import os
import datetime


database_list = ['hzzf_dsp_huz', 'hzzf_dsp_jx', 'hzzf_dsp_qz', 'hzzf_dsp_st', 'hzzf_dsp_sx', 'hzzf_dsp_tz']
date = datetime.date.today()
DATE = '{}-{}-{}'.format(date.year, date.month, date.day)
out_file_dir = 'H:/code/新增二手房清洗/' + DATE + '/原始数据/'
final_file_dir = 'H:/code/新增二手房清洗/' + DATE + '/清洗结果/'
DIRS = [out_file_dir, final_file_dir]


# 连接数据库
def connect_sql(db_name):
    db = pymysql.connect(host='47.114.98.123',
                         port=3306,
                         user='yangyang',
                         password='Yangyang@123',
                         database=db_name,
                         charset='utf8')
    return db


# 导出数据
def export_data():
    create_dir()
    for database in database_list:
        print('开始连接数据库：' + database)
        connect = connect_sql(database)
        print('连接数据库成功！')
        cursor = connect.cursor()
        cursor.execute('show tables')
        table_tuple = cursor.fetchall()
        for i, table in enumerate(table_tuple):
            table_name = table[0]
            if 'import' not in table_name:
                print('开始导出：' + table_name)
                cursor.execute("select * from " + table_name)
                data = cursor.fetchall()
                export_excel(data, table_name)
                print('导出成功：' + table_name)
        connect.close()


# 批量创建文件夹
def create_dir():
    for output_dir in DIRS:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)


# 写入文件
def export_excel(data, name):
    workbook = xlwt.Workbook(encoding='utf-8')
    # 创建一个worksheet
    worksheet = workbook.add_sheet('sheet1')
    # 写入excel 参数对应 行, 列, 值
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] is None:
                worksheet.write(i, j, '')
                continue
            worksheet.write(i, j, '%s' % data[i][j])
    workbook.save(out_file_dir + name + '-' + DATE + '.xlsx')


# 更改字段格式
def transform_type():
    contract_data_list = []
    house_data_list = []
    for file in os.listdir(out_file_dir):
        if 'contract' in file:
            contract_data_list.append(file)
        else:
            house_data_list.append(file)
    # 合同数据
    for data in contract_data_list:
        print('文件名：', data)
        data_name = data
        data = pd.read_excel(out_file_dir + data, dtype=object)
        data = data.reset_index(drop=True)
        data.index = range(len(data))
        data.iloc[:, 17] = data.iloc[:, 17].astype(int)  # flag
        data.iloc[:, 18] = data.iloc[:, 18].astype('datetime64[ns]')  # statistic_time
        data.iloc[:, 19] = data.iloc[:, 19].astype('datetime64[ns]')  # create_time
        data.iloc[:, 20] = data.iloc[:, 20].astype('datetime64[ns]')  # insert_data_time
        data.to_excel(out_file_dir + data_name, header=None, index=False)
    # 房屋数据
    for data in house_data_list:
        print('文件名：', data)
        data_name = data
        data = pd.read_excel(out_file_dir + data, dtype=object)
        data = data.reset_index(drop=True)
        data.index = range(len(data))
        data.iloc[:, 40] = data.iloc[:, 40].astype(int)  # flag
        data.iloc[:, 41] = data.iloc[:, 41].astype('datetime64[ns]')  # statistic_time
        data.iloc[:, 42] = data.iloc[:, 42].astype('datetime64[ns]')  # insert_data_time
        data.to_excel(out_file_dir + data_name, header=None, index=False)


if __name__ == '__main__':
    export_data()
    transform_type()

