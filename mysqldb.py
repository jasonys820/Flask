__author__ = 'ys'

import MySQLdb

db = MySQLdb.connect(host='localhost',user='root',passwd='123456',db='mysql',port=3306)

cursor = db.cursor()

cursor.execute('SELECT VERSION()')

data = cursor.fetchone()
print 'Database version: %s' % data

db.close()