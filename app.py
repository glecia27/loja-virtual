from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Configurações do banco de dados
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="loja_virtual",
    port=3307
)

cursor = db.cursor(dictionary=True)

# Rota para listar produtos (AGORA CARREGA CATEGORIAS TAMBÉM)
@app.route('/')
def listar_produtos():
    cursor.execute("SELECT p.*, c.nome AS categoria_nome FROM produtos p LEFT JOIN categorias c ON p.categoria_id = c.id")
    produtos = cursor.fetchall()

    # Adiciona a busca por categorias para preencher o dropdown no formulário de adicionar
    cursor.execute("SELECT id, nome FROM categorias")
    categorias = cursor.fetchall()

    return render_template('produtos.html', produtos=produtos, categorias=categorias) # Passa categorias

# Rota para adicionar produto
@app.route('/adicionar', methods=['POST'])
def adicionar_produto():
    nome = request.form['nome']
    descricao = request.form['descricao']
    preco = request.form['preco']
    estoque = request.form['estoque']
    categoria_id = request.form['categoria_id']
    
    cursor.execute("""
        INSERT INTO produtos (nome, descricao, preco, estoque, categoria_id)
        VALUES (%s, %s, %s, %s, %s)
    """, (nome, descricao, preco, estoque, categoria_id))
    
    db.commit()
    return redirect(url_for('listar_produtos'))

# Rota para deletar produto
@app.route('/deletar/<int:id>')
def deletar_produto(id):
    cursor.execute("DELETE FROM produtos WHERE id = %s", (id,))
    db.commit()
    return redirect(url_for('listar_produtos'))

# Rota para editar produto (carrega dados) - JÁ ESTAVA CERTO
@app.route('/editar/<int:id>')
def editar_produto(id):
    cursor.execute("SELECT * FROM produtos WHERE id = %s", (id,))
    produto = cursor.fetchone()

    cursor.execute("SELECT * FROM categorias")
    categorias = cursor.fetchall()
    
    return render_template('editar.html', produto=produto, categorias=categorias)

# Rota para atualizar produto
@app.route('/atualizar/<int:id>', methods=['POST'])
def atualizar_produto(id):
    nome = request.form['nome']
    descricao = request.form['descricao']
    preco = request.form['preco']
    estoque = request.form['estoque']
    categoria_id = request.form['categoria_id']

    cursor.execute("""
        UPDATE produtos
        SET nome=%s, descricao=%s, preco=%s, estoque=%s, categoria_id=%s
        WHERE id=%s
    """, (nome, descricao, preco, estoque, categoria_id, id))
    
    db.commit()
    return redirect(url_for('listar_produtos'))

if __name__ == '__main__':
    app.run(debug=True)