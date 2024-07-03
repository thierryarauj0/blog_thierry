from flask import Flask, request, render_template, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Chave secreta para WTForms e sessões

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Modelo de usuário para o banco de dados
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    admin = db.Column(db.Boolean, default=False)
    

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Modelo de post para o banco de dados
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
  

# Crie o banco de dados e as tabelas dentro do contexto do aplicativo
with app.app_context():
    db.create_all()

# Carregar usuário pelo ID para o Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Rota principal - lista de posts
@app.route('/')
def index():
    if current_user.is_authenticated:
        nome = request.args.get("nome")
        posts = Post.query.all()
        return render_template("index.html", nome=nome, posts=posts)
    else:
        return redirect(url_for('login'))

# Rota para adicionar um novo post
@app.route('/add_post', methods=['POST'])
@login_required
def add_post():
    data = request.get_json()
    new_post = Post(title=data['title'], content=data['content'], user_id=current_user.id)
    db.session.add(new_post)
    db.session.commit()
    return jsonify({"message": "Post added"}), 201

# Rota para deletar um post
@app.route('/delete_post/<int:id>', methods=['DELETE'])
@login_required
def delete_post(id):
    post = Post.query.get(id)
    if post:
        if post.author != current_user and not current_user.admin:
            return jsonify({"message": "Unauthorized"}), 403
        
        db.session.delete(post)
        db.session.commit()
        return jsonify({"message": "Post deleted"}), 200
    return jsonify({"message": "Post not found"}), 404

# Rota para editar um post
@app.route('/edit_post/<int:id>', methods=['PUT'])
@login_required
def edit_post(id):
    data = request.get_json()
    post = Post.query.get(id)
    if post:
        if post.author != current_user and not current_user.admin:
            return jsonify({"message": "Unauthorized"}), 403
        
        post.title = data['title']
        post.content = data['content']
        db.session.commit()
        return jsonify({"message": "Post updated"}), 200
    return jsonify({"message": "Post not found"}), 404

# Rota de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
       
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash('Login bem-sucedido!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Nome de usuário ou senha incorretos.', 'danger')

    return render_template('login.html')

# Rota de registro de usuário
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
       
        if User.query.filter_by(username=username).first():
            flash('Nome de usuário já está em uso.', 'danger')
        else:
            new_user = User(username=username)
            new_user.set_password(password)
          
            db.session.add(new_user)
            db.session.commit()
            flash('Cadastro realizado com sucesso! Faça login para continuar.', 'success')
            return redirect(url_for('login'))

    return render_template('signup.html')

# Rota de logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
