#-*-coding:utf-8-*-
import pandas as pd  


# xls = pd.ExcelFile("2016宁夏大学学生总体分年级、性别的各项目成绩样本数、平均值、标准差综合统计表2016.xlsx")
data=['dayi-nan', 'dayi-nv', 'daer-nan', 'daer-nv']  #进行每个项目的区分

value={ 'grade1-man': [1755, 7.30, 0.60],   #生成相应检测的值，包括各个项目均值、方差，按照男女区分
		'grade1-women' : [2707, 9.10, 0.70]
	}
for grade in data:  #第一次遍历整个excel表格
	for grade2 in data: #第二次遍历excel表格，相当于做笛卡儿积
		print ("test: %s-%s" % (grade, grade2))  #检测是否将值传进来

		t, p = ttest_ind(value['dayi-nan'], value['dayi-nv'])  #很关键的一步，进行男女间T检验，真正用到笛卡儿积，输出数据类型未Dataframe类型
		print ("write data in a line")
		pass
	print ("write \\n")  # 按行读取存储

	pass

"""T检验思路"""
"""" 1、读取excel文本
	2、读取大一~~大四学生，选取每个项目的平均值、方差
	3、进行男女项目的T检验（ttest_ind）
	4、年级T检验，男女项目进行T检验
	5、不同年级男女之间的T检验，比如大一男生和大二男生T检验
	6、根据检验结果输出CSV文件"""