# API BaaS (Banking as a Service)
- A API BaaS é uma API bancária simples que oferece recursos para autenticação de login, gerenciamento de contas, e transações bancárias, como extrato, saque, depósito e transferência entre contas. Ela foi desenvolvida usando o Flask, SQLAlchemy para interagir com um banco de dados MySQL, e Alembic para migrações de banco de dados.

## Funcionalidades Principais
- Login e Autenticação: Os usuários podem fazer login usando seu número de conta e senha. As credenciais são verificadas no banco de dados e uma sessão é estabelecida para autenticar o usuário.

- Cadastro de Conta: Novos usuários podem se cadastrar fornecendo informações como nome, CPF, senha e saldo inicial. Um número de conta único é gerado automaticamente.

- Extrato: Os usuários podem visualizar o extrato de sua conta, incluindo informações sobre saldo atual e histórico de transações.

- Saque: Os usuários podem realizar saques de suas contas, com verificação de saldo e registro da transação.

- Depósito: Depósitos podem ser feitos em contas existentes, com registro da transação e atualização de saldo.

- Transferência: Os usuários podem transferir dinheiro entre suas próprias contas ou para outras contas, com validações de saldo e registro das transações.

## Pré-requisitos
- Python 3.x
- Flask
- SQLAlchemy
- MySQL
- Alembic (para migração do banco de dados)

## Configuração 
- Clone o repositório para o seu ambiente de desenvolvimento.
- Crie um ambiente virtual
- Instale as dependências do projeto com pip freeze -r requirements.txt
- Faça as migrações do alembic para criar o banco de dados, certifique-se de configurar corretamente as informações do seu banco de dados no env.py na linha 17

## Endpoints da API
- Endpoints da API:
Login:
```
/login - POST
JSON:
{
	"numero_conta" : "000260948"
	"senha" : "123"
}
```

- Cadastrar:
```
/cadastrar - POST
json:
{
	"nome_proprietario" : "Joao Silva"
	"cpf" : "11122233344"
	"senha" : "123"
}
```

- Logout:
```
/logout - POST
```

- Saque
```  
/saque/<numero_conta>
JSON:
{
     "valor": "200"
}
```

Deposito - POST
```
/deposito/
{
	"valor" : "200"
}
```

- Transferência entre contas - POST
```
/transferencia/
{
    "conta_destino": "000456",  # Substitua pelo número da conta de destino desejada
    "valor": 100.0  # Substitua pelo valor que deseja transferir
}
```

- Extrato:
```
/extrato/<numero_conta> - GET
```
