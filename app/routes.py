from flask import Flask, request, jsonify, session, session
from app.models import Conta, Transacao, RegistroAuditoria
from app import app, db
from config import *
from sqlalchemy.orm.exc import NoResultFound
import random
import string
from helpers import valida_cpf, login_required

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    #Recuperar o número da conta e a senha do JSON de entrada
    numero_conta = data.get('numero_conta')
    senha = data.get('senha')

    #Consulte a conta no banco de dados com base no número da conta
    conta = Conta.query.filter_by(numero_conta=numero_conta).first()

    #Verificar se a conta existe e se a senha está correta
    if not conta or conta.senha != senha:
        return jsonify({'error': 'Número da conta ou senha inválidos'}, 401)
    #Se bem sucedido
    session['logged-in'] = True
    session['numero_conta'] = numero_conta
    return jsonify({'message': 'Login bem-sucedido!', 'numero_conta': numero_conta})
@app.route('/cadastro', methods=['POST'])
def cadastro():
    if session:
        return jsonify({'message': 'Você já esta logado, saia da sua conta para criar um novo cadastro!'})

    data = request.get_json()

    # Recupere os detalhes do usuário do JSON de entrada
    nome_proprietario = data.get('nome_proprietario')
    saldo_inicial = data.get('saldo', 0.0)
    cpf_informado = data.get('cpf')
    senha = data.get('senha')

    # Gerar um número de conta único com o prefixo "000" e 6 números aleatórios
    while True:
        numero_conta = "000" + ''.join(random.choices(string.digits, k=6))
        conta_existente = Conta.query.filter_by(numero_conta=numero_conta).first()
        if not conta_existente:
            break

    if not valida_cpf(cpf_informado):
        return jsonify({'message' : 'Informe um CPF válido!'})

    while True:
        cpf_existente = Conta.query.filter_by(cpf=cpf_informado).first()
        if cpf_existente:
            return jsonify({'message': 'Você já tem uma conta cadastrada nesse CPF!'})
        break

    # Crie uma nova conta de usuário
    nova_conta = Conta(
        numero_conta=numero_conta,
        saldo=saldo_inicial,
        nome_proprietario=nome_proprietario,
        cpf=cpf_informado,
        senha=senha
    )

    # Adicione a nova conta ao banco de dados
    db.session.add(nova_conta)
    db.session.commit()

    # Retorne o número da conta gerado como parte da resposta
    return jsonify({'message': 'Cadastro de usuário realizado com sucesso', 'numero_conta': numero_conta, 'senha' : senha}), 201
@app.route('/saque/', methods=['POST'])
def saque():
    if not login_required(session):
        return jsonify({'error': 'Acesso não autorizado'}), 401

    # Obtenha os dados da solicitação JSON
    data = request.get_json()

    # Verifique se os campos necessários estão presentes na solicitação
    if 'valor' not in data:
        return jsonify({'error': 'Dados de saque inválidos'}), 400

    # Pegue a conta a partir da sessão
    numero_conta = session.get('numero_conta')
    # Recupere o número da conta e o valor do depósito do JSON de entrada
    valor_deposito = data.get('valor')

    # Obtenha a conta com base no número da conta fornecido na URL
    conta = Conta.query.filter_by(numero_conta=numero_conta).first()


    # Verifique se a conta tem saldo suficiente para o saque
    try:
        valor_saque = float(data['valor'])
        if conta.saldo < valor_saque:
            return jsonify({'error': 'Saldo insuficiente para realizar o saque'}), 400
    except ValueError:
        return jsonify({'error': 'O valor deve ser um número inteiro'}), 400

    # Verifique se o valor do saque é maior que zero
    if valor_saque <= 0:
        return jsonify({'error': 'O valor do saque deve ser maior que zero'}), 400

    # Realize o saque, atualizando o saldo da conta e registrando a transação
    novo_saldo = conta.saldo - valor_saque
    conta.saldo = novo_saldo
    db.session.add(conta)

    registro = RegistroAuditoria(acao='Saque', detalhes=f'Saque de {valor_saque} realizado')
    db.session.add(registro)
    # Crie uma nova transação de saque
    transacao = Transacao(
        tipo_transacao='saque',
        valor=valor_saque,
        conta_id=conta.id
    )
    db.session.add(transacao)
    db.session.commit()

    return jsonify({'message': f'Saque realizado com sucesso: R${valor_saque}'}), 200

@app.route('/deposito', methods=['POST'])
def deposito():
    if not login_required(session):
        return jsonify({'error': 'Acesso não autorizado'}), 401

    data = request.get_json()

    # Pegue a conta a partir da sessão
    numero_conta = session.get('numero_conta')
    # Recupere o número da conta e o valor do depósito do JSON de entrada
    valor_deposito = data.get('valor')

    # Validação básica: Verifique se o valor do depósito são fornecidos
    if not valor_deposito:
        return jsonify({'error': 'Número da conta e valor do depósito são obrigatórios'}), 400

    # Consulte a conta no banco de dados com base no número da conta da sessão
    conta = Conta.query.filter_by(numero_conta=numero_conta).first()

    # Verifique se a conta existe
    if not conta:
        return jsonify({'error': 'Conta não encontrada'}), 404

    # Validação adicional: Verifique se o valor do depósito é positivo
    try:
        valor_deposito = int(valor_deposito)
        if valor_deposito <= 0:
            return jsonify({'error': 'O valor do depósito deve ser positivo'}), 400
    except ValueError:
        return jsonify({'error': 'O valor do depósito deve ser um número inteiro'}, 400)

    # Atualize o saldo da conta com o valor do depósito
    conta.saldo += valor_deposito

    registro = RegistroAuditoria(acao='Deposito', detalhes='Deposito de {} realizado'.format(data['valor']))
    db.session.add(registro)

    # Registre a transação de depósito
    transacao = Transacao(tipo_transacao='deposito', valor=valor_deposito, conta_id=conta.id)
    db.session.add(transacao)

    # Atualize o banco de dados
    db.session.commit()

    return jsonify({'message': 'Depósito realizado com sucesso'})
@app.route('/transferencia', methods=['POST'])
def transferencia():
    if not login_required(session):
        return jsonify({'error': 'Acesso não autorizado'}), 401

    data = request.get_json()

    # Verifique se os campos necessários estão presentes na solicitação
    if 'conta_destino' not in data or 'valor' not in data:
        return jsonify({'error': 'Dados de transferência inválidos'}), 400

    #Pega o numero_conta da sessão
    numero_conta_origem = session.get('numero_conta')

    # Obtenha as contas com base nos números de conta fornecidos
    conta_origem = Conta.query.filter_by(numero_conta=numero_conta_origem).first()
    conta_destino = Conta.query.filter_by(numero_conta=data['conta_destino']).first()

    # Verifique se as contas existem
    if not conta_origem or not conta_destino:
        return jsonify({'error': 'Uma das contas não foi encontrada'}), 404

    # Verifique se a conta de origem tem saldo suficiente para a transferência
    try:
        valor_transferencia = float(data['valor'])
        if conta_origem.saldo < valor_transferencia:
            return jsonify({'error': 'Saldo insuficiente para realizar a transferência'}), 400
    except ValueError:
        return jsonify({'error': 'O valor deve ser um número inteiro'}), 400

    # Verifique se o valor da transferência é maior que zero
    if valor_transferencia <= 0:
        return jsonify({'error': 'O valor da transferência deve ser maior que zero'}), 400

    # Realize a transferência, atualizando os saldos das contas e registrando as transações
    novo_saldo_origem = conta_origem.saldo - valor_transferencia
    novo_saldo_destino = conta_destino.saldo + valor_transferencia

    conta_origem.saldo = novo_saldo_origem
    conta_destino.saldo = novo_saldo_destino

    db.session.add(conta_origem)
    db.session.add(conta_destino)

    registro_origem = RegistroAuditoria(acao='Transferencia',
                                        detalhes=f'Transferência de R${valor_transferencia} para {conta_destino.numero_conta}')
    registro_destino = RegistroAuditoria(acao='Transferencia',
                                         detalhes=f'Recebido R${valor_transferencia} de {conta_origem.numero_conta}')

    db.session.add(registro_origem)
    db.session.add(registro_destino)

    # Crie novas transações de transferência
    transacao_origem = Transacao(
        tipo_transacao='transferencia',
        valor=valor_transferencia,
        conta_id=conta_origem.id
    )

    transacao_destino = Transacao(
        tipo_transacao='transferencia',
        valor=valor_transferencia,
        conta_id=conta_destino.id
    )

    db.session.add(transacao_origem)
    db.session.add(transacao_destino)

    # Atualize o banco de dados
    db.session.commit()

    return jsonify({'message': f'Transferência de R${valor_transferencia} realizada com sucesso'}), 200

@app.route('/extrato/', methods=['GET'])
def extrato():
    if not login_required(session):
        return jsonify({'error': 'Acesso não autorizado'}), 401

    numero_conta_origem = session.get('numero_conta')

    #Pra fornecer o numero da conta na url e depois puxar a transação pelo conta_id
    try:
        conta = Conta.query.filter_by(numero_conta=numero_conta_origem).one()
    except NoResultFound:
        return jsonify({'error': 'Conta não encontrada'})

    #Consulta as transações associadas a conta
    transacoes = Transacao.query.filter_by(conta_id=conta.id).all()

    lista_transacoes = []

    for transacao in transacoes:
        transacao_info = {
            'tipo_transacao': transacao.tipo_transacao,
            'valor': transacao.valor,
            'timestamp': transacao.timestamp
        }
        lista_transacoes.append(transacao_info)

    extrato = {
        'nome_proprietario': conta.nome_proprietario,
        'numero_conta': conta.numero_conta,
        'saldo' : conta.saldo,
        'transacoes' : lista_transacoes
    }
    return jsonify({'message': 'Extrato da conta obtido com sucesso', 'extrato': extrato})

@app.route('/logout', methods=['POST'])
def logout():
    if session:
        session.clear()
        return jsonify({'message': 'Logout bem-sucedido!'})
    else:
        return jsonify({'message': 'Você já está deslogado!'})