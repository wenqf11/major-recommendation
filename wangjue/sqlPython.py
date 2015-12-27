#coding=utf-8
import MySQLdb

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
    

#先讲major的salary获取
#SQLSalary() 
#将有salary的school平均值计算 
#SQLAvgSalary()
#根据Rank将没有Salary的学校计算
#SQLMakeAvgSalary()

#SQLAvgComment()
#SQLMakeAvgComment()
SQLAvgMajorSalaryAndComment()