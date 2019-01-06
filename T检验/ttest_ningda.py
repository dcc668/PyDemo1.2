#-*-coding:utf-8-*-
import pandas as pd  
from scipy.stats import ttest_ind
import  numpy

#pandas 读取excel
def read_excel(path):
	xls_file=pd.ExcelFile(path)
	for name in xls_file.sheet_names:#显示出读入excel文件中的表名字
		print('+++++++++++++++++++++++++++++sheet name:'+name+'+++++++++++++++++++++++++++++')
		sheet1=xls_file.parse(name)
		colss=[]
		print(sheet1.keys())
		for col_name in sheet1.keys():#样本数	平均值	标准差
			# if i%2==0:
			print(col_name)
			col_vals=[]
			values=sheet1.pop(col_name);
			leng=len(values)
			for j in range(3,leng):
				if j%2==0:
					continue;
				col_vals.append(values[j])
			print(col_vals)
			colss.append(col_vals)
		lines=[]
		for i in range(0,9):#9行数据
			line=[]
			for col in colss:#遍历每一列,获取第i个数据
				if not col[i]:
					line.append(0)
				else:
					line.append(col[i]);
			lines.append(line);
		df=pd.DataFrame(lines);
		df.fillna(0,inplace=True)
		return df.values
path="2017.xlsx"
students=read_excel(path);
#样本数
lines_counts=[]
#平均值
lines_avgs=[]
#标准差
lines_stds=[]
for stu in students:
	print(stu)
	line_counts=[]
	line_avgs=[]
	line_stds=[]
	for i in range(0,len(stu)):
		if i%3==0:
			line_counts.append(stu[i]);
		if i%3==1:
			line_avgs.append(stu[i]);
		if i%3==2:
			line_stds.append(stu[i]);
	lines_counts.append(line_counts)
	lines_avgs.append(line_avgs)
	lines_stds.append(line_stds)

#冒泡调用
print("--------------------冒泡调用-----------------------")
print(str(len(lines_counts)))
idx=0;
for i in range(0,len(lines_counts)-1):
	for j in range(i+1,len(lines_counts)):
		a=lines_counts[i]
		b=lines_counts[j]
		t, p = ttest_ind(a, b)  #很关键的一步，进行男女间T检验，真正用到笛卡儿积，输出数据类型未Dataframe类型
		idx=idx+1
		print ("调用次数："+str(idx))
		print ("t："+str(t))
		print ("p："+str(p))