from flask import Flask, render_template, flash, redirect, request, url_for
from forms import RegisterationForm, LoginForm
import os
import secrets
from flask_sqlalchemy import SQLAlchemy

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = '1747afcc43886f257ed0860ec3bc98fd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(APP_ROOT, 'app.db')
db=SQLAlchemy(app)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_picture(picture):
	random_hex = secrets.token_hex(16)
	_, f_ext = os.path.splitext(picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(APP_ROOT, 'static/img', picture_fn)
	picture.save(picture_path)
	return picture_fn

class Pictures(db.Model):
	id=db.Column(db.Integer, primary_key=True)
	image=db.Column(db.String(30), nullable=False)

@app.route('/')
def index():
  # form = LoginForm()
  return render_template('index.html')
  # return render_template('index.html', form=form)

# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#   form = RegisterationForm()
#   if form.validate_on_submit():
#     flash(f'Account created for {form.email.data}!', 'success')
#     return redirect(url_for('/'))
#   else:
#     print('Kataa')
#   return render_template('signup.html', title='Register', form=form)

@app.route('/uploaded-images', methods=['GET','POST'])
def uploaded_images():
	if request.method=='POST':
		files=request.files.getlist("images")
		valid=1
		for file in files:
			if not allowed_file(file.filename):
				valid=0
				break
		if valid:
			images=[]
			for file in files:
				upload=Pictures()
				upload.image=save_picture(file)
				images=images+[url_for('static', filename='img/' + upload.image)]
				db.session.add(upload)
				db.session.commit()
			return render_template('pictures.html', images=images)
		else:
			flash(f'Please upload a valid image', 'danger')
	return redirect(url_for('damage'))

@app.route('/damage-detection', methods=['GET'])
def damage():
	return render_template('upload-pictures.html')

if __name__ == '__main__':
	app.run(debug=True)