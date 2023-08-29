from app import db


# Modelo para representar as contas de usuário
class Conta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero_conta = db.Column(db.String(20), unique=True, nullable=False)
    saldo = db.Column(db.Float, default=0.0)
    nome_proprietario = db.Column(db.String(100), nullable=False)

    # Relacionamento com as transações
    transacoes = db.relationship('Transacao', backref='conta', lazy=True)

    def __repr__(self):
        return f'<Conta {self.numero_conta}>'


# Modelo para representar as transações (depósito e saque)
class Transacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo_transacao = db.Column(db.String(10), nullable=False)  # 'deposito' ou 'saque'
    valor = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    # Chave estrangeira para a conta relacionada
    conta_id = db.Column(db.Integer, db.ForeignKey('conta.id'), nullable=False)

    def __repr__(self):
        return f'<Transacao {self.tipo_transacao} {self.valor}>'
