from flask import Flask, render_template, request, redirect, url_for
from models import db, Produto, Categoria

app = Flask(__name__)

# Configuração do banco (ajuste a porta conforme necessário)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3307/loja_virtual'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o SQLAlchemy com o app
db.init_app(app)

@app.route('/')
def listar_produtos():
    produtos = Produto.query.join(Categoria, isouter=True).add_columns(
        Produto.id, Produto.nome, Produto.descricao, Produto.preco, Produto.estoque, Categoria.nome.label('categoria_nome')
    ).all()

    categorias = Categoria.query.all()
    return render_template('produtos.html', produtos=produtos, categorias=categorias)

@app.route('/adicionar', methods=['POST'])
def adicionar_produto():
    produto = Produto(
        nome=request.form['nome'],
        descricao=request.form['descricao'],
        preco=request.form['preco'],
        estoque=request.form['estoque'],
        categoria_id=request.form['categoria_id']
    )
    db.session.add(produto)
    db.session.commit()
    return redirect(url_for('listar_produtos'))

@app.route('/deletar/<int:id>')
def deletar_produto(id):
    produto = Produto.query.get_or_404(id)
    db.session.delete(produto)
    db.session.commit()
    return redirect(url_for('listar_produtos'))

@app.route('/editar/<int:id>')
def editar_produto(id):
    produto = Produto.query.get_or_404(id)
    categorias = Categoria.query.all()
    return render_template('editar.html', produto=produto, categorias=categorias)

@app.route('/atualizar/<int:id>', methods=['POST'])
def atualizar_produto(id):
    produto = Produto.query.get_or_404(id)
    produto.nome = request.form['nome']
    produto.descricao = request.form['descricao']
    produto.preco = request.form['preco']
    produto.estoque = request.form['estoque']
    produto.categoria_id = request.form['categoria_id']
    db.session.commit()
    return redirect(url_for('listar_produtos'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria as tabelas se não existirem
    app.run(debug=True)
