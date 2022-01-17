# -*- coding:utf-8 -*-
import os
import xlsxwriter
import requests
from openpyxl import Workbook,load_workbook

from openpyxl.drawing.image import Image
from hashlib import md5
import pandas as pd
from openpyxl.utils import get_column_letter, column_index_from_string
import openpyxl
IMG_COL = 'A'

def seed_get():
    # return os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, "demo.xlsx"))
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "demo.xlsx"))

def file_name_encrypt(url):
    md5_inst = md5()
    md5_inst.update(url.encode())
    return md5_inst.hexdigest()

def save_org_img(url,dir_position):
    if not os.path.exists(dir_position):
        os.mkdir(dir_position)
    res = requests.get(url)
    file_name = file_name_encrypt(url)
    img_fp= res.content
    with open(os.path.join(dir_position,file_name)+'.jpg', 'wb') as f:
        print(os.path.join(dir_position,file_name))
         # for data in res.iter_content(128):
         #    f.write(data)
        f.write(img_fp)
    # yield dir_position+file_name
    return os.path.join(dir_position,file_name)

def img_position_join(x,y):
    if isinstance(y,int):
        y = get_column_letter(y)
    return y+str(x)


def insert_img(sh, line, fp,):
    sh.row_dimensions[line].height=50
    img = Image(fp)
    print(img.width,img.height,img.format)
    img.width, img.height=img.width/10,img.height/10
    sh.add_image(img, 'A1')

def pd_read_excel():
    wb = Workbook()
    sh = wb.active
    df = pd.read_excel('demo.xlsx', sheet_name=0)
    col_name = df.columns.values.tolist()
    print(col_name)
    img_url_col_num = col_name.index('main_img_url') #返回img的列数
    max_column = len(col_name) #本表最大列数
    print(max_column)
    for idx, row in df.iterrows():
        print(row['main_img_url'])

        # d_row = {}
        # for column in col_name:
        #     d_row[column] = row[column]
        #     if column == 'output_date':
        #         s = str(row[column])
        #         d_row[column] = s[:4] + '-' + s[4:6] + '-' + s[6:]
        #     else:
        #         d_row[column] = row[column]
# pd_read_excel()

    #
if __name__ == "__main__":
    # wb = Workbook()
    # sh = wb.active
    wb = load_workbook(seed_get())
    ws = wb['Sheet1']
    print(ws.max_row)
    for fv in ws[2:ws.max_row]:
        # for sv in fv:
#         #     print(sv.value)
        print(fv[1].value)
        save_org_img(fv[1].value,r'test_img')

    # # sh.column_dimensions[IMG_COL].width= 10
    # sh.column_dimensions['AI'].width= 10
    # url = 'https://m.media-amazon.com/images/I/51tAycNDRfL._AC_SX679_.jpg'
    # file_name = save_org_img(url,r'F:/图片收集/')
    # insert_img(sh, 1, file_name)
    # wb.save('demo.xlsx')

# wb = openpyxl.load_workbook('demo.xlsx')
# # sheet = wb.get_sheet_by_name('Sheet')
# sheet = wb['Sheet']
# print(sheet.max_row)
# print(get_column_letter(sheet.max_column))
# print(sheet.max_column)

# def run():
#     df = pd.read_excel('demo.xlsx',sheet_name=0)
#     col_name = df.columns.values.tolist()
#     img_url_col_num = col_name.index('main_img_url') #返回img的列数
#     max_column = len(col_name) #本表最大列数
#     # print(max_column)
#     for idx, row in df.iterrows():
#         d_row = {}
#         for column in col_name:
#             d_row[column] = row[column]
#             if column == 'output_date':
#                 s = str(row[column])
#                 d_row[column] = s[:4] + '-' + s[4:6] + '-' + s[6:]
#             else:
#                 d_row[column] = row[column]
#
#
# run()