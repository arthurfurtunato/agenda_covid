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

def get_dias_ocupados_por_estabelecimento(est_id):
    by_dias = {}
    agendas = Agendamento.objects.filter(estabelecimento=est_id)
    for i in agendas:
        if i.data_vacinacao.date() in by_dias:
            by_dias[i.data_vacinacao.date()].append(i.cidadao.id)
        else:
            by_dias[i.data_vacinacao.date()] = [i.cidadao.id]
    dias_ocupados = [i for i, v in by_dias.items() if len(v) >= 24]
    return dias_ocupados

def horarios_livres_por_dia_por_estabelecimento(est_id, data):
    horarios_disp = []
    dia_horas = Agendamento.objects.filter(estabelecimento=est_id, data_vacinacao__date=datetime.strptime(data, "%d/%m/%Y").date())
    dia_horas = [h.data_vacinacao for h in dia_horas]
    for i in range(24):
        agenda_add = datetime.strptime(f'{data} 08:00', "%d/%m/%Y %H:%M") + timedelta(minutes=10*i)
        if not agenda_add in dia_horas:
            horarios_disp.append(agenda_add.strftime("%H:%M"))
    return horarios_disp
