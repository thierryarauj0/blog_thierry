from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

# Crie o banco de dados e as tabelas dentro do contexto do aplicativo
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    nome = request.args.get("nome")
    posts = Post.query.all()
    return render_template("index.html", nome=nome, posts=posts)

@app.route('/add_post', methods=['POST'])
def add_post():
    data = request.get_json()
    new_post = Post(title=data['title'], content=data['content'])
    db.session.add(new_post)
    db.session.commit()
    return jsonify({"message": "Post added"}), 201

@app.route('/delete_post/<int:id>', methods=['DELETE'])
def delete_post(id):
    post = Post.query.get(id)
    if post:
        db.session.delete(post)
        db.session.commit()
        return jsonify({"message": "Post deleted"}), 200
    return jsonify({"message": "Post not found"}), 404

@app.route('/edit_post/<int:id>', methods=['PUT'])
def edit_post(id):
    data = request.get_json()
    post = Post.query.get(id)
    if post:
        post.title = data['title']
        post.content = data['content']
        db.session.commit()
        return jsonify({"message": "Post updated"}), 200
    return jsonify({"message": "Post not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
