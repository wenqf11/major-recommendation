# -*- coding: utf-8 -*-  
from flask import Flask, request, render_template
from flask.ext.mysqldb import MySQL


app = Flask(__name__)
mysql = MySQL(app)
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'majordb'
app.config['MYSQL_HOST'] = '127.0.0.1'


def get_candidate_majorlist(province, category, year, score):
	cur = mysql.connection.cursor()
	cur.execute(u'select * from entryscore where province="%s" and type="%s" and year=%d and score < %d'
		% (province, category, year, score))
	result = cur.fetchall()
	cur.close()
	return result


@app.route("/", methods=['GET','POST'])
def index():
	candidates = get_candidate_majorlist(u"湖南", u"理科", 2014, 588)
	if request.method == "GET":
		return render_template("index.html", candidates=candidates)
	else:
		province = request.form['province']
		category = request.form['category']
		year = 2014
		try:
			score = int(request.form['score'])
		except Exception, e:
			return render_template("index.html", error=u"输入分数有误") 
		print get_candidate_majorlist(province, category, year, score)
		return render_template("index.html", candidates=candidates)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
