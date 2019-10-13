from flask import Flask, render_template, flash, redirect
from forms import RegisterationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '1747afcc43886f257ed0860ec3bc98fd'

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


if __name__ == '__main__':
  app.run(debug=True)