# -*- coding: utf-8 -*-  
from flask import Flask, request, render_template
from flask.ext.mysqldb import MySQL
from models import *


app = Flask(__name__)
mysql = MySQL(app)
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'bigdatasystem'
app.config['MYSQL_HOST'] = '127.0.0.1'

def getMarjorRank(schools, ratio, character):
    

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
            sqlStr = "select commentScore,salary,ISTJ,INFJ,ISTP,INFP,ESTJ,ENFJ,ESTP,ENFP,ISFJ,INTJ,ISFP,INTP,ESFJ,ENTJ,ESFP,ENTP from major where majorId=%d" % \
                    (major.majorId)
            cur.execute(sqlStr)
            majorResult = cur.fetchall()
            major.commentScore = majorResult[0][0];
            major.salary = majorResult[0][1];

            char_dict = dict()
            char_dict['ISTJ'] = majorResult[0][2];
            char_dict['INFJ'] = majorResult[0][3];
            char_dict['ISTP'] = majorResult[0][4];
            char_dict['INFP'] = majorResult[0][5];
            char_dict['ESTJ'] = majorResult[0][6];
            char_dict['ENFJ'] = majorResult[0][7];
            char_dict['ESTP'] = majorResult[0][8];
            char_dict['ENFP'] = majorResult[0][9];
            char_dict['ISFJ'] = majorResult[0][10];
            char_dict['INTJ'] = majorResult[0][11];
            char_dict['ISFP'] = majorResult[0][12];
            char_dict['INTP'] = majorResult[0][13];
            char_dict['ESFJ'] = majorResult[0][14];
            char_dict['ENTJ'] = majorResult[0][15];
            char_dict['ESFP'] = majorResult[0][16];
            char_dict['ENTP'] = majorResult[0][17];
            char_dict[''] = 0

            cur.execute("select academicScore from academicscore where majorId=%d"% major.majorId)
            major.academicScore = cur.fetchone()

            if not major.academicScore:
            	major.academicScore = 0
            else:
            	major.academicScore = float(major.academicScore[0])

            if not school.rank:
            	school.rank = 0

            major.characterScore = char_dict[character] * 10
            major.schoolRank = school.rank
            major.finalScore = major.commentScore*ratio['comment-ratio']+ major.academicScore*ratio['academic-ratio'] + major.schoolRank *ratio['school-ratio'] + major.salary*ratio['job-ratio']
            major.schoolName = school.schoolName
            majorLists.append(major)
            
    cur.close()

    majorLists.sort(key=lambda obj:obj.finalScore, reverse=True)
    return majorLists


def compute_major_score(schools, ratio, character, k):
    
	#获取专业评价

	majorLists = getMarjorRank(schools, ratio, character)

	
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
		character = request.form['character']

		year = 2014
		ratio = dict()
		try:
			score = int(request.form['score'])
			k = int(request.form['topk'])
			ratio['school-ratio'] = float(request.form['school-ratio'])
			ratio['academic-ratio'] = float(request.form['academic-ratio'])
			ratio['job-ratio'] = float(request.form['job-ratio'])
			ratio['comment-ratio'] = float(request.form['comment-ratio'])
		except Exception, e:
			return render_template("index.html", error=u"输入参数有误")
		school_major_list = get_candidate_list(province, category, year, score)
		major_list = compute_major_score(school_major_list, ratio, character, k)
		input_score = score
		return render_template("index.html", major_list=major_list, ratio=ratio, topk=k, input_score=score,
			province=province, character=character, category=category)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
