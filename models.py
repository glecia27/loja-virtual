from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Categoria(db.Model):
    __tablename__ = 'categorias'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

    produtos = db.relationship('Produto', backref='categoria', lazy=True)

class Produto(db.Model):
    __tablename__ = 'produtos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    preco = db.Column(db.Float)
    estoque = db.Column(db.Integer)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=True)
