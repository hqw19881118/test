# coding=utf-8
import sys
import xlwt as ExcelWrite 

# 写excel
xls = ExcelWrite.Workbook(encoding = 'utf-8')
sheet = xls.add_sheet("Sheet1")
sheet.write(i, 1, "\n".join(["a", "b"])) # 单元格内换行
xls.save('text.xls')

# 读excel