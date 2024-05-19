from flask import render_template, redirect, url_for, flash, session
from app import app, db, bcrypt
from forms import RegistrationForm, LoginForm

class User(db.Model):
    __tablename__ = 'User'
    email = db.Column(db.String(120), primary_key=True)
    nome = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"User('{self.nome}', '{self.email}')"

# Rota da Página Inicial
@app.route('/')
def home():
    user = session.get('user')
    return render_template('home.html', title='Home', user=user)

# Rota de Registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(nome=form.nome.data, email=form.email.data, password=hashed_password, role=form.role.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# Rota de Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['user'] = {'nome': user.nome, 'email': user.email, 'role': user.role}
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

# Rota de Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))
