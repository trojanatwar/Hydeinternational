from flask import Flask, render_template, redirect, url_for, request, Response, jsonify, json, flash, send_file
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message
from flask_sqlalchemy  import SQLAlchemy
from wtforms.validators import InputRequired, Email, Length
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, BooleanField
from werkzeug.utils import secure_filename
import sqlite3 as sqlite
import os


app = Flask(__name__)
mail= Mail(app)


UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'docx', 'doc'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.from_object('config.BaseConfig')
app.secret_key = "asdasd%#$^#^#$%$"
app.static_folder = 'static'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/user.db'


bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#-------------------------App Config END----------------------------------------#
#-------------------------Messages START----------------------------------------#

messg1 = "Created Successfully!"
login_messge = "Invalid username or password!" 


#-------------------------Messages END------------------------------------------#
#------------------------------------User Login START--------------------------------------------#


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


#------------------------------------File Upload END--------------------------------------------#

mail = Mail(app)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=['POST', 'GET'])
def home():
	return render_template("index.html")


@app.route("/about")
def about():
	return render_template("about.html")


@app.route("/services")
def services():
	return render_template("services.html")

@app.route("/snm")
def snm():
	return render_template("inter-marketing.html")

@app.route("/hr")
def hr():
	return render_template("human-r.html")

@app.route("/rnd")
def rnd():
	return render_template("RnD.html")

@app.route("/support")
def support():
	return render_template("business-s.html")

@app.route("/opportunity", methods=['POST','GET'])
def opportunity():
	data = ""
	message = ""
	file_list = []
	file_path = ""
	if request.method == 'POST':
		data = request.form
		print(data)
		fil = request.files.getlist('atta_file')
		for f in fil:
			if f and allowed_file(f.filename):
				file_path =UPLOAD_FOLDER+str(secure_filename(f.filename))
				f.save(os.path.join(file_path))
			file_list.append(os.path.join(file_path))
		# msg = Message("Opportunity Enquiry", sender = 'contact@hyde-china.com', recipients = ['contact@hyde-china.com'])
		# msg.body = "<div>" + \
		# 		   "<strong>Name: </strong>" + data['name'] + "<br>" + \
		# 		   "<strong>Email: </strong>" + data['email'] + "<br>" + \
		# 		   "<strong>Phone: </strong>" + data['phone'] + "<br>" + \
		# 		   "<strong>Industry: </strong>" + data['cata'] + "<br>" + \
		# 		   "<strong>Message: </strong>" + data['message']  + "</div>"
		# msg.html = msg.body
		# for atta_f in file_list:
		# 	with app.open_resource(atta_f) as fp:
		# 		msg.attach(atta_f, 'text/xml', fp.read())
		# mail.send(msg)
		for d_file in file_list:
			if os.path.exists(d_file):
		  		os.remove(d_file)
		return render_template("opportunity.html", message=data['submit'])
	return render_template("opportunity.html", message=None)
   
@app.route("/contact", methods=['POST', 'GET'])
def contact():
	data = None
	message = None
	if request.method == 'POST':
		data = request.form
		msg = Message("Online Enquiry", sender = 'contact@hyde-china.com', recipients = ['contact@hyde-china.com'])
		msg.body = "<div>" + \
				   "<strong>Name: </strong>" + data['name'] + "<br>" + \
				   "<strong>Email: </strong>" + data['email'] + "<br>" + \
				   "<strong>Phone: </strong>" + data['phone'] + "<br>" + \
				   "<strong>Subject: </strong>" + data['subject'] + "<br>" + \
				   "<strong>Message: </strong>" + data['message']  + "</div>"
		msg.html = msg.body
		mail.send(msg)
		return render_template("contact.html", message=data['send'])
	return render_template("contact.html")

@app.route("/privacy_policy")
def privacy_policy():
	return render_template("policy-pages/privacy-policy.html")

@app.route("/cookies_policy")
def cookies_policy():
	return render_template("policy-pages/cookies-policy.html")

@app.route("/terms_of_service")
def terms_of_service():
	return render_template("policy-pages/terms-of-service.html")

@app.route("/form", methods=['POST', 'GET'])
def form():
	message = "All good"
	if request.method == 'POST':
		return render_template("form.html", message=message)
	return render_template("form.html", message="")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        print(user)
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('admin'))
        else:   
            return render_template('login.html', form=form, msg = login_messge)    
    return render_template('login.html', form=form, msg='')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('home'))
    return render_template('signup.html', form=form)

@app.route('/admin', methods=['POST', 'GET'])
@login_required
def admin():
	if request.method == 'POST':
		password = request.form['passw']
		conn = sqlite.connect('db/password.db')
		conn.execute("INSERT INTO passw (password) VALUES (?)", (password,))
		conn.commit()
		conn.close()
		msg = "Added Successfully!"
		return render_template("admin.html", msg=msg)
	return render_template("admin.html", msg='')



if __name__ == '__main__':
	app.run(debug = False, host='0.0.0.0', port=80)



# Login Credentials 
# Username hyde_admin
# Password 0123456789