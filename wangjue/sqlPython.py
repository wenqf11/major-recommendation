#coding=utf-8
import MySQLdb
import xlrd
import sys
import os
from models import *

reload(sys)
sys.setdefaultencoding('utf8')



class Major:
    def __init__(self,majorId,majorName):
        self.majorId = majorId
        self.majorName = majorName
        self.comments = []
        self.salary = 0;

class Comment:

    def __init__(self,majorId,comprehensiveScore,teachingScore,dealScore,workScore):
        self.majorId = majorId
        self.comprehensiveScore = comprehensiveScore
        self.teachingScore = teachingScore
        self.dealScore = dealScore
        self.workScore = workScore

class School:
    def __init__(self,Id,schoolName):
        self.majors = []
        self.score = 0.0
        self.schoolId = Id
        self.schoolAvgCommentScore = 0
        self.schoolAvgSalary = 0
        self.schoolName= schoolName
    
#获取数据库连接
def getCurAndConn():

    try:
        conn=MySQLdb.connect(host='localhost',user='root',passwd='919294',db='bigdatasystem',port=3306)
        cur=conn.cursor()
        return [cur,conn]
    except MySQLdb.Error,e:
         print "Mysql Error %d: %s" % (e.args[0], e.args[1])

#SQL 处理Rank
def SQLRank():
    
    connObject = getCurAndConn()
    cur = connObject[0]
    conn = connObject[1]
    sqlStr = "select * from school"
    cur.execute(sqlStr)
    schoolResults = cur.fetchall()
    
    #获取每个学校的Score
    for schoolRow in schoolResults:

        schoolId = schoolRow[0]
        sqlStr = "select score from Rank where SchoolId = %d" % ( schoolId)
        cur.execute(sqlStr)
        scoreResult = cur.fetchall()
        for score in scoreResult:
            sqlStr = "update school set rank=%s where schoolId = %s;" % (score[0],schoolId)
            print sqlStr
            cur.execute(sqlStr)
    cur.close()
    conn.commit()
    conn.close()
    
#SQL 处理salary
def SQLSalary():
    
    connObject = getCurAndConn()
    cur = connObject[0]
    conn = connObject[1]
    sqlStr = "update major set salary = 0"
    cur.execute(sqlStr)
    sqlStr = "select * from major"
    cur.execute(sqlStr)
    majorResults = cur.fetchall()
    
    #获取每个学校的Score
    for majorRow in majorResults:

        majorId = majorRow[0]
        sqlStr = "select * from salary where majorId = %d" % ( majorId)
        cur.execute(sqlStr)
        scoreResult = cur.fetchall()
        for score in scoreResult:
            sqlStr = "update major set salary=%s where majorId = %s;" % (score[1],majorId)
            print sqlStr
            cur.execute(sqlStr)
    cur.close()
    conn.commit()
    conn.close()

#SQL 处理salary
def SQLComment():
    
    connObject = getCurAndConn()
    cur = connObject[0]
    conn = connObject[1]
    sqlStr = "select * from major"
    cur.execute(sqlStr)
    majorResults = cur.fetchall()
    
    #获取每个学校的Score
    for majorRow in majorResults:

        majorId = majorRow[0]
        sqlStr = "select * from comment where majorId = %d" % ( majorId)
        #print sqlStr
        cur.execute(sqlStr)
        results = cur.fetchall()
        for row in results:
            comment = row[1]/20+row[2]/20 + row[3]/20 + row[4]/20
            sqlStr = "update major set commentScore = %f where majorId=%d " % (comment,majorId)
            if comment > 0:
                print sqlStr
            cur.execute(sqlStr)
    cur.close()
    conn.commit()
    conn.close()
    
def SQLAvgComment():    
    
    connObject = getCurAndConn()
    cur = connObject[0]
    conn = connObject[1]
    
    sqlStr = "select schoolId from  school"
    cur.execute(sqlStr)
    schoolIdResult = cur.fetchall()
    for schoolIds in schoolIdResult:
        #求出学校的平均水平
        schoolId = schoolIds[0]
        sqlStr = "select * from major where schoolId=%d" % (schoolId)
        cur.execute(sqlStr)
        results = cur.fetchall()
        avgComment = 0.0
        existsMajor = 0;
        for row in results:
            sqlStr = "select * from comment where majorId=%d" % (row[0])
            cur.execute(sqlStr)
            commentResults = cur.fetchall()
            comment = 0
            for row in commentResults:
                comment = row[1]/20+row[2]/20 + row[3]/20 + row[4]/20
            if comment != 0 :
                avgComment += comment
                existsMajor+=1
        
        if existsMajor:
            print"-----------"
            print "avgComment %f" % (avgComment)
            avgComment /= (existsMajor + 0.0)
            print "avgComment deal %f" % (avgComment)
            
            sqlStr = "update major set commentScore=%f where schoolId = %d and commentScore=0" % (avgComment,schoolId)
            print sqlStr
            cur.execute(sqlStr)
            sqlStr = "update school set avgComment=%f where schoolId = %d" % (avgComment,schoolId)
            cur.execute(sqlStr)
    cur.close()
    conn.commit()
    conn.close()

#需要多次迭代
def SQLMakeAvgComment():    
    
    connObject = getCurAndConn()
    cur = connObject[0]
    conn = connObject[1]
    
    sqlStr = "select * from school order by Rank desc";
    
    cur.execute(sqlStr)
    schoolResult = cur.fetchall()

    for i in range(0,len(schoolResult)-1):
        if schoolResult[i][4]==0 and schoolResult[i-1][4]!=0 and schoolResult[i+1][4] !=0:
            schoolSalary = (schoolResult[i-1][4] + schoolResult[i+1][4])/2.0
            print "i %d" % (i)
            sqlStr = "update school set avgComment=%f where schoolId = %d" %(schoolSalary,schoolResult[i][0])
            cur.execute(sqlStr)
        else:
            if schoolResult[i][4]==0 and schoolResult[i-1][4]!=0:
                print "-------"
                print "i %d" %(i)
                print "-----"
                sqlStr = "update school set avgComment=%f where schoolId = %d" %(schoolResult[i-1][4],schoolResult[i][0])
                cur.execute(sqlStr)
    cur.close()
    conn.commit()
    conn.close()


    
def SQLAvgSalary():    
    
    connObject = getCurAndConn()
    cur = connObject[0]
    conn = connObject[1]
    
    sqlStr = "select schoolId from  school"
    cur.execute(sqlStr)
    schoolIdResult = cur.fetchall()
    for schoolIds in schoolIdResult:
        #求出学校的平均水平
        schoolId = schoolIds[0]
        sqlStr = "select * from major where schoolId=%d" % (schoolId)
        cur.execute(sqlStr)
        results = cur.fetchall()
        avgSalary = 0.0
        existsMajor = 0;
        for row in results:
            sqlStr = "select * from salary where majorId=%d" % (row[0])
            cur.execute(sqlStr)
            salaryResults = cur.fetchall()
            salary = 0
            for salaryRow in salaryResults:
                salary = salaryRow[1]    
            if salary != 0 :
                avgSalary += salary
                existsMajor+=1
        
        if existsMajor:
            print"-----------"
            print "avgSalary %f" % (avgSalary)
            avgSalary /= (existsMajor + 0.0)
            print "avgSalary deal %f" % (avgSalary)
            
            sqlStr = "update major set salary=%f where schoolId = %d and salary=0" % (avgSalary,schoolId)
            print sqlStr
            cur.execute(sqlStr)
            sqlStr = "update school set avgSalary=%f where schoolId = %d" % (avgSalary,schoolId)
            cur.execute(sqlStr)
    cur.close()
    conn.commit()
    conn.close()

#需要多次迭代
def SQLMakeAvgSalary():    
    
    connObject = getCurAndConn()
    cur = connObject[0]
    conn = connObject[1]
    
    sqlStr = "select * from school order by Rank desc";
    
    cur.execute(sqlStr)
    schoolResult = cur.fetchall()

    for i in range(0,len(schoolResult)-2):
        if schoolResult[i][3]==0 and schoolResult[i-1][3]!=0 and schoolResult[i+1][3] !=0:
            schoolSalary = (schoolResult[i-1][3] + schoolResult[i+1][3])/2.0
            print "i %d" % (i)
            sqlStr = "update school set avgSalary=%f where schoolId = %d" %(schoolSalary,schoolResult[i][0])
            cur.execute(sqlStr)
        else:
            if schoolResult[i][3]==0 and schoolResult[i-1][3]!=0:
                print "-------"
                print "i %d" %(i)
                print "-----"
                sqlStr = "update school set avgSalary=%f where schoolId = %d" %(schoolResult[i-1][3],schoolResult[i][0])
                cur.execute(sqlStr)
    cur.close()
    conn.commit()
    conn.close()

#根据学校的平均值将所有没有salary和comment的专业填满
def SQLAvgMajorSalaryAndComment():    
    
    connObject = getCurAndConn()
    cur = connObject[0]
    conn = connObject[1]
    
    sqlStr = "select schoolId, avgSalary, avgComment from  school"
    cur.execute(sqlStr)
    schoolIdResult = cur.fetchall()
    for schoolIds in schoolIdResult:

        schoolId = schoolIds[0]
        print "result %f %f %f" %(schoolIds[0],schoolIds[1],schoolIds[2])
        sqlStr = "select * from major where schoolId=%d" % (schoolId)
        cur.execute(sqlStr)
        results = cur.fetchall()
        
        for row in results:
            sqlStr = "update major set salary=%f where majorId=%d and salary=0" % (schoolIds[1],row[0])
            cur.execute(sqlStr)
            sqlStr = "update major set commentScore=%f where majorId=%d and commentScore=0" % (schoolIds[2],row[0])
            cur.execute(sqlStr)
            
    cur.close()
    conn.commit()
    conn.close()
    
def lookForTsinghua():
    
    connObject = getCurAndConn()
    cur = connObject[0]
    conn = connObject[1]
    cur.execute('set names utf8')
    sqlStr = "select majorId from major where schoolId = 200"
    cur.execute(sqlStr)
    schoolIdResult = cur.fetchall()
    for schoolIds in schoolIdResult:

        schoolId = schoolIds[0]
        sqlStr = "select * from entryscore where majorId=%d" % (schoolId)
        cur.execute(sqlStr)
        results = cur.fetchall()
        
        for row in results:
                
                print "%s %s %s %s %s %s" % (row[0],row[1],row[2],row[3],row[4],row[5])
    cur.close()
    conn.commit()
    conn.close()

# -*- coding: utf-8 -*-

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
            listScore.append(table.cell(i, 16).value)
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

def dealCharacterSQL(subject_map,character_map):

    for k in character_map.keys():
        listScore = character_map.get(k)
        #print k;
        listMajor = subject_map.get(k)
        if listMajor != None :
            for major in subject_map.get(k):  
                connObject = getCurAndConn()
                cur = connObject[0]
                conn = connObject[1]
                cur.execute('set names utf8')
                #print len(listScore)
                sqlStr = "update major set ISTJ=%f,INFJ=%f,ISTP=%f,INFP=%f,ESTJ=%f,ENFJ=%f,ESTP=%f,ENFP=%f,ISFJ=%f,INTJ=%f,ISFP=%f,INTP=%f,ESFJ=%f,ENTJ=%f,ESFP=%f,ENTP=%f where majorName='%s'"\
                         % (listScore[0],listScore[1],listScore[2],listScore[3],listScore[4],listScore[5],listScore[6],listScore[7],\
                         listScore[8],listScore[9],listScore[10],listScore[11],listScore[12],listScore[13],listScore[14],\
                         listScore[15],k.decode("utf-8"))
                cur.execute(sqlStr)
                cur.close()
                conn.commit()
                conn.close()
subject_map = get_map("subject.xlsx")
character_map = getCharacter("character0-1.xlsm")

dealCharacterSQL(subject_map,character_map)
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
"""
#先讲major的salary获取
#SQLSalary() 
#将有salary的school平均值计算 
#SQLAvgSalary()
#根据Rank将没有Salary的学校计算
#SQLMakeAvgSalary()

#SQLAvgComment()
#SQLMakeAvgComment()
#SQLAvgMajorSalaryAndComment()

#lookForTsinghua()
