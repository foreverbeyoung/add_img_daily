import os

import requests
from openpyxl import load_workbook
from openpyxl.drawing.image import Image

def seed_get():
    # return os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, "demo.xlsx"))
    print(os.path.abspath(os.path.join(os.path.dirname(__file__), "demo.xlsx")))
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "demo.xlsx"))
def get_demo_img():
    with open('2.jpeg','wb') as f:
        f.write(requests.get('https://m.media-amazon.com/images/I/615CNPcAmzL._AC_SS450_.jpg').content)
    return requests.get('https://m.media-amazon.com/images/I/615CNPcAmzL._AC_SS450_.jpg').content

# wb = load_workbook(seed_get())
# # sh = wb.get_sheet_by_name('Sheet1')
# sh = wb['Sheet1']
# sh.column_dimensions['A'].width= 100
# img = Image('2.jpeg')
# sh.add_image(img, 'A22')
# wb.save('demo.xlsx')
print(os.path.dirname(__file__))
print(os.path.join(os.path.dirname(__file__), "demo.xlsx"))
print(os.getcwd())
