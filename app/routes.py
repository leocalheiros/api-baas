from flask import Flask, request, jsonify, flash, session, url_for
from app.models import Conta, Transacao, RegistroAuditoria
from app import *
from app import db
from config import *
@app.route('/saque', methods=['POST'])
def saque():
    # Obtenha os dados da solicitação JSON
    data = request.get_json()

    # Verifique se os campos necessários estão presentes na solicitação
    if 'conta_id' not in data or 'valor' not in data:
        return jsonify({'error': 'Dados de saque inválidos'}), 400

    # Obtenha a conta com base no ID da conta fornecido na solicitação
    conta = Conta.query.get(data['conta_id'])

    # Verifique se a conta existe
    if not conta:
        return jsonify({'error': 'Conta não encontrada'}), 404

    # Verifique se a conta tem saldo suficiente para o saque
    if conta.saldo < data['valor']:
        return jsonify({'error': 'Saldo insuficiente para realizar o saque'}), 400

    # Verifique se o valor do saque é maior que zero
    if data['valor'] <= 0:
        return jsonify({'error': 'O valor do saque deve ser maior que zero'}), 400

    # Realize o saque, atualizando o saldo da conta e registrando a transação
    novo_saldo = conta.saldo - data['valor']
    conta.saldo = novo_saldo
    db.session.add(conta)

    registro = RegistroAuditoria(acao='Saque', detalhes='Saque de {} realizado'.format(data['valor']))
    db.session.add(registro)
    # Crie uma nova transação de saque
    transacao = Transacao(
        tipo_transacao='saque',
        valor=data['valor'],
        conta_id=conta.id
    )
    db.session.add(transacao)
    db.session.commit()
