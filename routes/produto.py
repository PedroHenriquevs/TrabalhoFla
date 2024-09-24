from flask import Blueprint, render_template, request, redirect, url_for, flash
from utils import db
from models import Produto

produto_route = Blueprint('produto', __name__)

@produto_route.route('/listar_produtos')
def listagem_produtos():
    lista_produto = Produto.query.all()
    return render_template('listar.html', lista=lista_produto)

@produto_route.route('/cadastrar')
def cadastrar_produto():
    return render_template('cadastrar.html')

@produto_route.route('/cadastrar_enviar', methods=['POST'])
def cadastrar_enviar_produto():
    nome = request.form['nome']
    categoria = request.form['categoria']
    
    
    quantidade = request.form['quantidade'] or 0  
    preco = request.form['preco'] or 0.0  
    
    try:
        quantidade = int(quantidade) 
        preco = float(preco)  
    except ValueError:
        flash('Quantidade e preço devem ser valores numéricos!', 'danger')
        return redirect(url_for('produto.cadastrar_produto'))

    p = Produto(nome=nome, categoria=categoria, quantidade=quantidade, preco=preco)

    db.session.add(p)
    db.session.commit()
    
    flash('Produto cadastrado com sucesso!', 'success')
    
    # Redirecionar de volta para a página de cadastro
    return redirect(url_for('produto.cadastrar_produto'))

@produto_route.route('/editar_produto/<int:id_produto>')
def editar(id_produto):
    p = Produto.query.get(id_produto)
    return render_template('editar.html', dados_produto=p)

@produto_route.route('/editar_enviar', methods=['POST'])
def editar_enviar():
    id_produto = request.form['id_produto']
    nome = request.form['nome']
    categoria = request.form['categoria']
    
    # Validação para quantidade e preço
    quantidade = request.form['quantidade'] or 0
    preco = request.form['preco'] or 0.0
    
    try:
        quantidade = int(quantidade)
        preco = float(preco)
    except ValueError:
        flash('Quantidade e preço devem ser valores numéricos!', 'danger')
        return redirect(url_for('produto.editar', id_produto=id_produto))

    p = Produto.query.get(id_produto)
    p.nome = nome
    p.categoria = categoria
    p.quantidade = quantidade
    p.preco = preco

    db.session.add(p)
    db.session.commit()

    flash('Produto editado com sucesso!', 'success')
    return redirect(url_for('produto.listagem_produtos'))

@produto_route.route('/excluir/<int:id_produto>')
def excluir(id_produto):
    p = Produto.query.get(id_produto)

    db.session.delete(p)
    db.session.commit()

    flash('Produto excluído com sucesso!', 'danger')
    return redirect(url_for('produto.listagem_produtos'))
