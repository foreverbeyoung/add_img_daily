import xlrd
import requests
import xlsxwriter
# import cv2
from PIL import Image

# 只要修改这个需要处理的excel文件名即可，请使用.xls后缀的excel文件！
excel_url_file = '图片url.xls'  # 设置单元格带有图片或附件url的excel文件名

a = xlrd.open_workbook(excel_url_file, 'r')  # 打开.xlsx文件
sht = a.sheets()[0]  # 打开表格中第一个sheet
nrows = sht.nrows;
# 列与列名的对照表
indexToRow = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
              'V', 'W', 'X', 'Y', 'Z', 'AA', 'AB']

workbook2 = xlsxwriter.Workbook(r'结果.xlsx')
worksheet2 = workbook2.add_worksheet()

start = 0;  # 开始行 1表示第二行开始， 0表示第一行开始
columon_find = 25;  # 最多找到第26列
cell_width = 50  # 设置图片单元格的列宽
cell_height = 100  # 设置图片单元格的行高

for i in range(start, nrows):  # 从开始行到结束行
    # url = sht.cell(i, 5).value  # 依次读取每行第6列(0-5)的数据，也就是 URL

    for j in range(0, columon_find):  # 从每行的第0列到第N列
        rownow = indexToRow[j] + str(i + 1)  # 注意是从A1单元格开始的！！
        # worksheet2.write('A2', '插入第一张图片：')
        # print('jjjjj'+str(j))
        try:
            print('正在复制： ' + rownow + ' = ' + str(sht.cell(i, j).value))
            rowValue = sht.cell(i, j).value
            worksheet2.write(rownow, rowValue)  # 直接讲读取到的值复制到新的excel中

            try:
                if rowValue:
                    f = requests.get(rowValue)
                    ii = rownow + "_file"  # 按照单元格构造文件名
                    url2 = rowValue[-3:]  # 根据链接地址获取文件后缀，后缀有.jpg 和 .gif 两种
                    filedir = ii + "." + url2  # 构造完整文件名称
                    with open(filedir, "wb") as code:
                        code.write(f.content)  # 保存文件
                    print('已下载： ' + rowValue)  # 打印当前的 URL

                    # 使用pillow读取图片，获取图片的宽和高
                    try:
                        img_pillow = Image.open(filedir)
                        img_width = img_pillow.width  # 图片宽度
                        img_height = img_pillow.height  # 图片高度
                        # print("width -> {}, height -> {}".format(img_width, img_height))
                        # cell_width = 50
                        # cell_height = 100
                        worksheet2.set_column(j, j, cell_width + 4)  # 设置带图片单元格列宽
                        worksheet2.set_row(i, cell_height + 4)  # 设置带图片单元格行高

                        x_scale = cell_width / img_width
                        y_scale = cell_height / img_height
                        if img_width / img_height < cell_width / cell_height:  # 让图片 大小适应调整
                            y_scale = x_scale
                        else:
                            x_scale = y_scale

                        # worksheet2.insert_image(rownow, filedir, {'x_offset': 2,'y_offset':2,'x_scale': 100/img_width, 'y_scale': 100/img_height})
                        worksheet2.insert_image(rownow, filedir,
                                                {'x_offset': 2, 'y_offset': 2, 'x_scale': x_scale, 'y_scale': y_scale})
                    except:
                        print('')

            except:
                print('普通单元格')


        except:
            break

try:
    workbook2.close()
    print('excel文件【结果.xlsx】保存成功')
except:
    print('文件可能被占用，保存失败！！！')