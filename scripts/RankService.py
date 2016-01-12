#coding=utf-8
import MySQLdb

class Major:
    def __init__(self,majorId,majorName):
        self.majorId = majorId
        self.majorName = majorName
        self.commentScore = 0;
        self.salary = 0
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
        self.rank = 0
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

def getMarjorRank(school):
    
    connObject = getCurAndConn()
    cur = connObject[0]
    conn = connObject[1]
    
    cur.execute('set names utf8')
    majorLists = []
    for school in schools:

        #求出学校的平均水平
        sqlStr = "select rank from school where schoolId=%d" % (school.schoolId)
        cur.execute(sqlStr)
        schoolResult = cur.fetchall()
        school.rank = schoolResult[0][0]
        sqlStr = "select * from major where schoolId=%d" % (school.schoolId)
        cur.execute(sqlStr)
        results = cur.fetchall()
        #求每个major的评价
        for major in school.majors:
            sqlStr = "select commentScore,salary from major where majorId=%d" % \
                    (major.majorId)
            cur.execute(sqlStr)
            majorResult = cur.fetchall()
            commentScore = majorResult[0][0];
            salary = majorResult[0][1];
            major.finalScore = (commentScore + school.rank + salary)/3
            major.schoolName = school.schoolName
            majorLists.append(major)
            
    cur.close()
    conn.close()
    majorLists.sort(key=lambda obj:obj.finalScore, reverse=True)
    return majorLists

#测试用例
school = School(199,'中国人民大学')
major = Major(659,'法学')
major2 = Major(660,'人力资源')
school.majors.append(major)
school.majors.append(major2)
schools = []
schools.append(school)


majorLists =  getMarjorRank(schools)

for major in majorLists:
    print 'school name is %s , major is %s, the score is %f' %\
            (major.schoolName,major.majorName,major.finalScore)

