from flask import session, jsonify
def valida_cpf(cpf):
    # Remove caracteres não numéricos
    cpf = ''.join(filter(str.isdigit, cpf))

    # Verifique se o CPF tem 11 dígitos
    if len(cpf) != 11:
        return False

    # Verifique se todos os dígitos são iguais
    if len(set(cpf)) == 1:
        return False

    # Cálculo do primeiro dígito verificador
    soma = 0
    for i in range(9):
        soma += int(cpf[i]) * (10 - i)
    resto = 11 - (soma % 11)
    if resto in (10, 11):
        resto = 0
    if resto != int(cpf[9]):
        return False

    # Cálculo do segundo dígito verificador
    soma = 0
    for i in range(10):
        soma += int(cpf[i]) * (11 - i)
    resto = 11 - (soma % 11)
    if resto in (10, 11):
        resto = 0
    if resto != int(cpf[10]):
        return False

    return True

def login_required(session):
    if 'logged-in' not in session:
        return False
    return True


