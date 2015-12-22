#coding=utf-8
import MySQLdb

class Major:
    def __init__(self,majorId,majorName):
        self.majorId = majorId
        self.majorName = majorName
        self.comments = []

class Comment:

    def __init__(self,commentId,comprehensiveScore,teachingScore,dealScore,workScore):
        self.commentId = commentId
        self.comprehensiveScore = comprehensiveScore
        self.teachingScore = teachingScore
        self.dealScore = dealScore
        self.workScore = workScore

class School:
    def __init__(self,Id,schoolName):
        self.majors = []
        self.score = 0
        self.schoolId = Id
        self.schoolName= schoolName
    
#获取数据库连接
def getCurAndConn():

    try:
        conn=MySQLdb.connect(host='localhost',user='root',passwd='919294',db='bigdatasystem',port=3306)
        cur=conn.cursor()
        return [cur,conn]
    except MySQLdb.Error,e:
         print "Mysql Error %d: %s" % (e.args[0], e.args[1])

#获取专业评价
def getComments(schools):

    connObject = getCurAndConn()
    cur = connObject[0]
    conn = connObject[1]
    
    cur.execute('set names utf8')

    for school in schools:

        #求出学校的平均水平
        sqlStr = "select * from comment where schoolId=%d" % (school.schoolId)
        cur.execute(sqlStr)
        results = cur.fetchall()
        avgScore = 0.0
        
        for row in results:
            avgScore += row[3] + row[4] + row[5] + row[6]
        avgScore /= (len(results)*4);
        #求每个major的评价
        for major in school.majors:
            sqlStr = "select * from comment where majorId=%d and schoolId=%d" % \
                    (major.majorId,school.schoolId)
            cur.execute(sqlStr)
            results = cur.fetchall()
            #如果数据库没有记录则设置平均值为打分
            if len(results) == 0:
                comment = Comment(0,avgScore,avgScore,avgScore,avgScore)
            else:
                for row in results:
                    comment = Comment(row[0],row[3],row[4],row[5],row[6])
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

majorLists = []

#计算专业评价
for school in schools:
    for major in school.majors:
        comment = major.comments[0]
        major.finalScore = comment.comprehensiveScore + comment.teachingScore + comment.dealScore + comment.workScore
        major.finalScore = major.finalScore/20.0
        major.schoolName = school.schoolName
        majorLists.append(major)


    
majorLists.sort(key=lambda obj:obj.finalScore, reverse=True)

for major in majorLists:
    print 'school name is %s , major is %s, the score is %f' %\
            (major.schoolName,major.majorName,major.finalScore)
