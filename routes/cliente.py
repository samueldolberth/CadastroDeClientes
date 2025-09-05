from flask import Blueprint, render_template, request
from database.cliente import CLIENTES

cliente_route = Blueprint('cliente', __name__)

@cliente_route.route('/')
def lista_cliente():
    """ listar os clientes """
    return render_template('lista_clientes.html', clientes=CLIENTES)



@cliente_route.route('/', methods=['POST'])
def inserir_cliente():
    """ inserir os dados do cliente """
    
    data = request.json

    novo_usuario = {
        "id": len(CLIENTES) + 1,
        "nome": data['nome'],
        "email": data['email'],
    }

    CLIENTES.append(novo_usuario)
    return render_template('item_cliente.html', cliente=novo_usuario)




@cliente_route.route('/new')
def form_cliente():
    """ formulario para cadastrar um cliente"""
    return render_template('form_cliente.html')



@cliente_route.route('/<int:cliente_id>')
def detalhe_cliente(cliente_id):
    """ formulario para cadastrar um cliente"""

    # Filter com lambda, retorna o cliente que possui o mesmo id do DB CLIENTES,
    # usando Lambda para não precisar usar o "for" como nas outras rotas
    cliente = list(filter(lambda c: c['id'] == cliente_id, CLIENTES))[0] # refaz uma lista com 1 item (que seria o usuario com o ID)
    return render_template('detalhe_cliente.html', cliente=cliente)



@cliente_route.route('/<int:cliente_id>/edit')
def form_edit_cliente(cliente_id):
    """ formulario para editar um cliente"""

    # obtem usuario pelo id
    cliente = None
    for c in CLIENTES:
        if c['id'] == cliente_id:
            cliente = c

    return render_template('form_cliente.html', cliente=cliente)



@cliente_route.route('/<int:cliente_id>/update', methods=['PUT'])
def atualizar_cliente(cliente_id):
    """ atualizar informações do cliente """
    cliente_editado = None
    # obter dados do formulario de edição
    data = request.json

    # obter usuario pelo id
    for c in CLIENTES:
        if c['id'] == cliente_id:
            c['nome'] = data['nome']
            c['email'] = data['email']

            cliente_editado = c

    # editar usuario
    return render_template('item_cliente.html', cliente=cliente_editado)



@cliente_route.route('/<int:cliente_id>/delete', methods=['DELETE'])
def deletar_cliente(cliente_id):
    global CLIENTES
    # o primeiro 'c' é o que vamos colocar na nova lista
    # ou seja, para cada C em CLIENTES, vai colocar na nova lista apenas o C que tiver ID diferente do ID do Cliente
    # cria uma nova lista sem o cliente que desejamos remover
    CLIENTES = [ c for c in CLIENTES if c['id'] != cliente_id]
    return {'deleted': 'ok'}