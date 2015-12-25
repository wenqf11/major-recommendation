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

#获取专业薪水
def getSalary(schools):

    connObject = getCurAndConn()
    cur = connObject[0]
    conn = connObject[1]
    
    cur.execute('set names utf8')

    sqlStr = "select max(money) from salary"
    cur.execute(sqlStr)
    results = cur.fetchall()
    maxSalary = 0.0;
    for row in results:
        maxSalary = row[0];

    for school in schools:

        #求出学校的平均水平
        sqlStr = "select * from major where schoolId=%d" % (school.schoolId)
        cur.execute(sqlStr)
        results = cur.fetchall()
        avgSalary = 0.0
        for row in results:
            sqlStr = "select * from salary where majorId=%d" % (row[0])
            cur.execute(sqlStr)
            salaryResults = cur.fetchall()
            salary = 0
            for salaryRow in salaryResults:
                salary = salaryRow[1]
            avgSalary += salary
            
        avgSalary /= (len(results))

        
        #求每个major的薪水
        for major in school.majors:
            sqlStr = "select * from salary where majorId=%d" % \
                    (major.majorId)
            cur.execute(sqlStr)
            results = cur.fetchall()
            
            #如果数据库没有记录则设置平均值为打分
            if len(results) == 0:
                major.salary= avgSalary/maxSalary;
            else:
                for row in results:
                    major.salary  = row[1]
    cur.close()
    conn.close()
    return schools


#获取学校排名
def getRank(schools):

    connObject = getCurAndConn()
    cur = connObject[0]
    conn = connObject[1]
    
    cur.execute('set names utf8')

    #获取score最大值
    sqlStr = "select max(score) from Rank";
    cur.execute(sqlStr);
    results = cur.fetchall()
    maxScore = 0;
    for row in results:
        maxScore = row[0]
    
    #获取每个学校的Score
    for school in schools:

        sqlStr = "select * from rank where schoolId=%d" % (school.schoolId)
        cur.execute(sqlStr)
        rankResults = cur.fetchall()
        #设置Score并进行归一化   
        for row in rankResults:
            maxScore = maxScore + 0.0
            school.score = row[0]/maxScore

    return schools


#select max(totalScore) from (select (workScore+comprehensiveScore+teachingScore+dealScore)/4 totalScore  from comment) a ;
#获取专业评价
def getComments(schools):

    connObject = getCurAndConn()
    cur = connObject[0]
    conn = connObject[1]
    
    cur.execute('set names utf8')

    for school in schools:

        #求出学校的平均水平
        sqlStr = "select * from major where schoolId=%d" % (school.schoolId)
        cur.execute(sqlStr)
        results = cur.fetchall()
        avgScore = 0.0
        for row in results:
            sqlStr = "select * from comment where majorId=%d" % (row[0])
            cur.execute(sqlStr)
            commentResults = cur.fetchall()
            majorAvgScore = 0.0
            for commentRow in commentResults:
                majorAvgScore += commentRow[1] + commentRow[2] + commentRow[3] + commentRow[4]
            majorAvgScore /= (len(commentRow))
            avgScore += majorAvgScore
        avgScore /= (len(results)*4)
        
        #求每个major的评价
        for major in school.majors:
            sqlStr = "select * from comment where majorId=%d" % \
                    (major.majorId)
            cur.execute(sqlStr)
            results = cur.fetchall()
            #如果数据库没有记录则设置平均值为打分
            if len(results) == 0:
                comment = Comment(0,avgScore/5,avgScore/5,avgScore/5,avgScore/5)
            else:
                for row in results:
                    comment = Comment(row[0]/5,row[1]/5,row[2]/5,row[3]/5,row[4]/5)
                    major.comments.append(comment)  
    cur.close()
    conn.close()
    return schools

#测试用例
school = School(199,'中国人民大学')
major = Major(659,'法学')
major2 = Major(660,'人力资源')
school.majors.append(major)
school.majors.append(major2)
schools = []
schools.append(school)

#获取专业评价
schools = getComments(schools)

#获取学校排名
schools = getRank(schools)

#获取专业薪水
schools = getSalary(schools)


majorLists = []

#计算专业评价
for school in schools:
    for major in school.majors:
        comment = major.comments[0]
        commentScore = (comment.comprehensiveScore + comment.teachingScore + comment.dealScore + comment.workScore)/4.0
        rankScore = school.score;
        salaryScore = major.salary;
        major.finalScore = (commentScore + rankScore + salaryScore)/3
        major.schoolName = school.schoolName
        majorLists.append(major)


    
majorLists.sort(key=lambda obj:obj.finalScore, reverse=True)

for major in majorLists:
    print 'school name is %s , major is %s, the score is %f' %\
            (major.schoolName,major.majorName,major.finalScore)

