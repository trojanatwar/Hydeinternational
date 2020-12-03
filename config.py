import sqlite3 as sqlite


class BaseConfig:
	conn = sqlite.connect('db/password.db')
	cur = conn.cursor()
	cur.execute("SELECT password from passw ORDER BY pass_id DESC LIMIT 1;")
	password = cur.fetchall()
	password = password[0][0]
	conn.close()
	DEBUG = False
	TESTING = False
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	MAIL_SERVER = 'smtpw.263.com'
	MAIL_PORT = 465
	MAIL_USE_SSL = True
	MAIL_USE_TLS = False
	MAIL_USERNAME = 'contact@hyde-china.com'
	MAIL_PASSWORD = password