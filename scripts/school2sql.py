# -*- coding: utf-8 -*-  
import xlrd
import MySQLdb
import os


row_id = 0
def transform(file_name):
	global row_id
	data = xlrd.open_workbook(file_name)
	table = data.sheets()[0]
	for i in xrange(1, table.nrows):
		if(table.cell(i, 5).value=='2014'):
			#print(table.cell(i, 1).value, table.cell(i, 2).value, table.cell(i, 3).value, table.cell(i, 4).value,  table.cell(i, 5).value)
			conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='',db='bigdatasystem',port=3306, charset="utf8")
			cur = conn.cursor()
			cur.execute(u'select * from school where schoolName="%s"'% table.cell(i, 1).value)
			school = cur.fetchone()
			if school:
				school_id = school[0]

				cur.execute(u'select * from major where schoolId=%d and majorName="%s"' % (school_id, table.cell(i, 2).value))
				major = cur.fetchone()
				if major:
					province =  table.cell(i, 3).value
					category = table.cell(i, 4).value
					try:
						year = int(table.cell(i, 5).value)
						score = int(table.cell(i, 6).value)
					except:
						year = 0
						score = 0
					if score > 0:
						row_id += 1
						print major[0], province, category, year, score, row_id
						cur.execute(u'insert into entryscore values("%d","%s","%s","%d","%d","%d")' 
							%(major[0], province, category, year, score, row_id))
			cur.close()
			conn.commit()
			conn.close()		

if __name__ == '__main__':
	path = os.getcwd()
	files = os.listdir(path)
	i = 0
	for f in files:
		if f.find("xls")>0:
			i += 1
			print i, f
			transform(f)