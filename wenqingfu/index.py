from flask import Flask, request, render_template
import flaskext.mysql import MySQL


app = Flask(__name__)
mysql = MySQL()
pp.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'major-data'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
cursor = mysql.get_db().cursor()


@app.route("/", methods=['GET','POST'])
def index():
    if request.method == "GET":
        return render_template("index.html")
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
