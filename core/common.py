from core.models import Agendamento
from datetime import datetime, timedelta

def validador_cpf(cpf):
    if len(cpf) != 11:
        return False

    lista = list(cpf[0:9])
    count = 0
    resultado = 0
    resultado2 = 0
    count2 = 0

    sequencia = cpf == cpf[0] * len(cpf)

    for i in lista:
        count += 1
        calculo = int(i) * count
        resultado = resultado + calculo

    digito_10 = (resultado % 11)
    if digito_10 != 10:
        lista.append(str(digito_10))
    else:
        lista.append('0')

    for i in lista:
        calculo = int(i) * count2
        resultado2 = resultado2 + calculo
        count2 += 1

    digito_11 = (resultado2 % 11)
    if digito_11 != 10:
        lista.append(str(digito_11))
    else:
        lista.append('0')

    cpf_str = ''.join(lista)
    if cpf_str == cpf and sequencia == False:
        return True
    else:
        return False