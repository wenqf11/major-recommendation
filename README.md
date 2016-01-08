# major-recommendation
This is a website for major recommendation

## installation

* Python 2.7
* MySQL 5.5+
* Flask 0.10.1
* Flask-MySQLdb 0.2.0

## database configuration
* import ```data/bigdatasystem.sql``` to MySQL
* configure your db setting in src/index.py

```python
app.config['MYSQL_USER'] = 'root'  your username 
app.config['MYSQL_PASSWORD'] = ''  your password
app.config['MYSQL_DB'] = 'bigdatasystem'  your db name
app.config['MYSQL_HOST'] = '127.0.0.1'
```
## Run
```python src/index.py```