# -*- coding: utf-8 -*-  
from flask import Flask, request, render_template
from flask.ext.mysqldb import MySQL
from models import *


app = Flask(__name__)
mysql = MySQL(app)
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '919294'
app.config['MYSQL_DB'] = 'bigdatasystem'
app.config['MYSQL_HOST'] = '127.0.0.1'

def getMarjorRank(schools):
    

    cur = mysql.connection.cursor()
    
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
            if(school.rank == None):
                major.finalScore = (commentScore + salary)/2
            else:
                major.finalScore = (commentScore + school.rank + salary)/3
            major.schoolName = school.schoolName
            majorLists.append(major)
            
    cur.close()

    majorLists.sort(key=lambda obj:obj.finalScore, reverse=True)
    return majorLists


def compute_major_score(schools, k):
    
	#获取专业评价

	majorLists = getMarjorRank(schools)

	
	return majorLists[:k]


def get_candidate_list(province, category, year, score):
	cur = mysql.connection.cursor()
	cur.execute(u'select * from entryscore where province="%s" and category="%s" and year=%d and score < %d'
		% (province, category, year, score))
	result = cur.fetchall()

	result_list = []
	for r in result:
		r_list = []
		for item in r:
			r_list.append(item)
		r_list.pop()
		cur.execute(u'select * from major where majorId=%d' % (r[0]))
		major = cur.fetchone()
		r_list.append(major[2])
		r_list.append(major[1])
		result_list.append(r_list)
	cur.close()

	result_list.sort(key=lambda obj:obj[5], reverse=True)


	schools = []
	cur = mysql.connection.cursor()
	previous_schoolId = -1
	for r in result_list:
		majorId = r[0]
		schoolId = r[5]
		marjorName = r[6]	
		if schoolId != previous_schoolId:
			cur.execute(u'select * from school where schoolId=%d' % (schoolId))
			schoolObj = cur.fetchone()
			if (previous_schoolId >= 0):
				schools.append(school)
			school = School(schoolId, schoolObj[1])
		major = Major(majorId, marjorName)
		school.majors.append(major)
		previous_schoolId = schoolId
	if(previous_schoolId >= 0):
		schools.append(school)
	cur.close()

	return schools


@app.route("/", methods=['GET','POST'])
def index():
	if request.method == "GET":
		return render_template("index.html")
	else:
		province = request.form['province']
		category = request.form['category']
		year = 2014
		try:
			score = int(request.form['score'])
		except Exception, e:
			return render_template("index.html", error=u"输入分数有误") 
		school_major_list = get_candidate_list(province, category, year, score)
		major_list = compute_major_score(school_major_list, 5)
		return render_template("index.html", major_list=major_list)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
