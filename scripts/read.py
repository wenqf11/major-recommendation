# -*- coding: utf-8 -*-
import xlrd
import MySQLdb
import sys
import os
from models import *

reload(sys)   
sys.setdefaultencoding('utf8')



def transform(s):
	return s.split(" ")[1]

def getCharacter(file_name):

    data = xlrd.open_workbook(file_name)
    table = data.sheets()[1]
    character_map = dict()
    for i in xrange(1, table.nrows):
        if(table.cell(i, 0).value):
            key = table.cell(i, 0).value
            key.decode("utf-8")
            listScore = []
#			if table.cell(i, 1).value:
	    listScore.append(table.cell(i, 1).value)
#			if table.cell(i, 2).value:
	    listScore.append(table.cell(i, 2).value)
#			if table.cell(i, 3).value:
	    listScore.append(table.cell(i, 3).value)
#			if table.cell(i, 4).value:
	    listScore.append(table.cell(i, 4).value)
#			if table.cell(i, 5).value:
	    listScore.append(table.cell(i, 5).value)
#			if table.cell(i, 6).value:
	    listScore.append(table.cell(i, 6).value)
#			if table.cell(i, 7).value:
	    listScore.append(table.cell(i, 7).value)
#			if table.cell(i, 8).value:
	    listScore.append(table.cell(i, 8).value)
#			if table.cell(i, 9).value:
	    listScore.append(table.cell(i, 9).value)
#			if table.cell(i, 10).value:
	    listScore.append(table.cell(i, 10).value)
#			if table.cell(i, 11).value:
	    listScore.append(table.cell(i, 11).value)
#			if table.cell(i, 12).value:
	    listScore.append(table.cell(i, 12).value)
#			if table.cell(i, 13).value:
	    listScore.append(table.cell(i, 13).value)
#			if table.cell(i, 14).value:
	    listScore.append(table.cell(i, 14).value)
#			if table.cell(i, 15).value:
	    listScore.append(table.cell(i, 15).value)
#			if table.cell(i, 16).value:
	    character_map[key] = listScore
    return character_map

def get_map(file_name):
	data = xlrd.open_workbook(file_name)
	table = data.sheets()[0]
	subject_map = dict()
	for i in xrange(0, table.nrows):
		if(table.cell(i, 0).value):
			key = transform(table.cell(i, 0).value)
			if not subject_map.has_key(key):
				subject_map[key] = [key]
			if table.cell(i, 1).value:
				subject_map[key].append(transform(table.cell(i, 1).value))
	return subject_map


subject_map = get_map("subject.xlsx")
character_map = getCharacter("character0-1.xlsm")
'''
for k in subject_map.keys():
    yourSlushUStr = subject_map.get(k)
    print "\n-------"
    print k
    print "---------"
    for result in yourSlushUStr:
        print result
        decodedUnicodeStr = result.decode("utf-8")
        print decodedUnicodeStr

for k in character_map.keys():
    yourSlushUStr = character_map.get(k)
    print "\n-------"
    print k
    print "---------"
    for result in yourSlushUStr:
        print result 
'''



""""
def transform(file_name):
	global subject_map
	data = xlrd.open_workbook(file_name)
	table = data.sheets()[0]
	subject_name = table.cell(0, 2).value

	if not subject_map.get(subject_name):
		return
	conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='',db='bigdatasystem',port=3306, charset="utf8")
	cur = conn.cursor()
	cur.execute(u'select schoolId from school where schoolName="%s"' % (table.cell(2, 1).value))
	school_id = cur.fetchone()
	if school_id:
		school_id = school_id[0]
		for major_name in subject_map.get(subject_name):
			cur.execute(u'select majorId from major where schoolId=%d and majorName="%s"' % (school_id, major_name))
			major_id = cur.fetchone()
			if major_id:
				cur.execute(u'insert into academicscore values("%d","%f")'%(major_id[0], 100))
				if print table.cell(2, 1).value==u"清华大学":
					print table.cell(2, 1).value, major_name, 100

	rate = 100.0 /  table.cell(2, 2).value

	for i in xrange(3, table.nrows):
		cur.execute(u'select schoolId from school where schoolName="%s"' % (table.cell(i, 1).value))
		school_id = cur.fetchone()
		if school_id:
			school_id = school_id[0]
			scores = int(table.cell(i, 2).value) * rate
			for major_name in subject_map.get(subject_name):
				cur.execute(u'select majorId from major where schoolId=%d and majorName="%s"' % (school_id, major_name))
				major_id = cur.fetchone()
				if major_id:
					cur.execute(u'insert into academicscore values("%d","%f")'%(major_id[0], scores))
					if print table.cell(i, 1).value==u"清华大学":
						print table.cell(i, 1).value, major_name, scores

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
"""
