from django.core.checks import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from core.common import get_dias_ocupados_por_estabelecimento, horarios_livres_por_dia_por_estabelecimento, validador_cpf
from datetime import date, datetime
import json

from core.models import Agendamento, Cidadao, EstabelecimentoSaude

def inicio(request):
    return redirect('index')

def index(request):
    if request.user.is_authenticated:
        cidadao = Cidadao.objects.filter(usuario=request.user).first() #Filtrando em cidadaos o usuario logado, e pegando o primeiro QuerySet
        idade = date.today().year - cidadao.nascimento.year
        agendamento = Agendamento.objects.filter(cidadao=cidadao)
        agendamento_estab = ""
        agendamento_data = ""
        if len(agendamento) > 0:
            agendamento_estab = agendamento.first().estabelecimento.dados_estabelecimento["NO_FANTASIA"]
            agendamento_data = agendamento.first().data_vacinacao.strftime("%d/%m/%Y às %H:%M")
        if date(date.today().year, cidadao.nascimento.month, cidadao.nascimento.day) > date.today():
            idade = idade - 1
        return render(request, 'index.html', {
            'cidadao': cidadao,
            'idade': idade,
            'agendamento_estab': agendamento_estab,
            'agendamento_data': agendamento_data, 
        })
    else:
        return render(request, 'index_noauth.html')

def cadastrar(request):
    if request.method != 'POST':
        return render(request, 'cadastrar.html')

    nome = request.POST.get('nome')

    nascimento = request.POST.get('nascimento')
    data_nascimento = nascimento.split('-')
    data_nascimento = date(int(data_nascimento[0]), int(data_nascimento[1]),int(data_nascimento[2]))

    cpf = request.POST.get('cpf').split(".")
    cpf_nodecoration = ''.join(cpf[0:2] + cpf[2].split("-"))

    senha = request.POST.get('senha')
    senha2 = request.POST.get('senha2')

    idade = date.today().year - data_nascimento.year
    if date(date.today().year, data_nascimento.month, data_nascimento.day) > date.today():
        idade = idade - 1

    if not nome or not nascimento or not cpf or not senha or not senha2:
        messages.error(request, 'Algum campo está vazio.')
        return render(request, 'cadastrar.html')

    if senha != senha2:
        messages.error(request, 'As senhas não conferem.')
        return render(request, 'cadastrar.html')

    if Cidadao.objects.filter(cpf=cpf_nodecoration).exists():
        messages.error(request, 'CPF já existente.')
        return render(request, 'cadastrar.html')

    if len(senha) < 6:
        messages.error(request, 'A senha precisa ter pelo menos 6 caracteres.')
        return render(request, 'cadastrar.html')

    if validador_cpf(cpf_nodecoration) == False:
        messages.error(request, 'O cpf está inválido')
        return render(request, 'cadastrar.html')

    if idade < 18:
        messages.error(request, 'Para realizar o cadastro, precisa ser maior de 18 anos.')
        return render(request, 'cadastrar.html')

    user = User.objects.create_user(cpf_nodecoration, email=None, password=senha)
    user.save()

    cidadao = Cidadao(nome=nome, cpf=cpf_nodecoration, nascimento=nascimento, usuario=user)
    cidadao.save()
    messages.success(request, 'Registrado com sucesso.')
    return redirect('/cidadao/entrar')

def entrar(request):
    if request.method != 'POST':
        return render(request, 'entrar.html')

    cpf = request.POST.get('cpf')
    senha = request.POST.get('senha')

    user = auth.authenticate(request, username=cpf, password=senha)

    if not user:
        messages.error(request, 'Usuário ou senha estáo incorretos')
        return render(request, 'entrar.html')
    else:
        auth.login(request, user)
        return redirect('index')

@login_required(login_url='/cidadao/')
def agendar(request):
    if len(Agendamento.objects.filter(cidadao=Cidadao.objects.filter(usuario=request.user).first())) > 0:
        messages.info(request, 'Cidadao ja tem agendamento')
        return redirect('index')
    if request.method == 'GET':
        estabelecimentos = EstabelecimentoSaude.objects.all()
        estab_tupla = [(i.id, i.dados_estabelecimento["CO_CNES"], i.dados_estabelecimento["NO_FANTASIA"]) for i in estabelecimentos]
        return render(request, 'agendar1.html', {
            'estabelecimentos': estab_tupla
        })
    else:
        if 'estabelecimento' in request.POST:
            estab = EstabelecimentoSaude.objects.filter(id=request.POST['estabelecimento'])
            estab_n = estab[0]
            dias_ocupados = get_dias_ocupados_por_estabelecimento(estab_n.id)
            return render(request, 'agendar2.html', {
                'estabelecimento_id': estab_n.id,
                'estabelecimento_nome': estab_n.dados_estabelecimento["NO_FANTASIA"],
                'dias_ocupados': json.dumps(dias_ocupados)
            })
        elif 'data' in request.POST and not 'horarios' in request.POST:
            if datetime.strptime(request.POST["data"], "%d/%m/%Y").weekday() in [5, 6]:
                messages.error(request, 'Agendamento permitido somente de segunda à sexta.')
                return redirect('/cidadao/')
            lista_horas = horarios_livres_por_dia_por_estabelecimento(request.POST['estabelecimento_id'], request.POST["data"])
            return render(request, 'agendar3.html', {
                'horarios': lista_horas,
                'data': request.POST["data"],
                'estabelecimento_id': request.POST["estabelecimento_id"],
                'estabelecimento_nome': request.POST["estabelecimento_nome"]
            })
        elif 'horarios' in request.POST and not 'salvar' in request.POST:
            return render(request, 'agendar4.html', {
                'horarios': request.POST['horarios'],
                'data':request.POST['data'],
                'estabelecimento_id':request.POST['estabelecimento_id'],
                'estabelecimento_nome':request.POST['estabelecimento_nome']
            })

        elif 'salvar':
            estabelecimento = EstabelecimentoSaude.objects.filter(id=request.POST['estabelecimento_id']).first()
            cidadao = Cidadao.objects.filter(usuario=request.user).first()
            data = datetime.strptime(f'{request.POST["data"]} {request.POST["horarios"]}', "%d/%m/%Y %H:%M")

            agendamento = Agendamento(cidadao=cidadao, estabelecimento=estabelecimento, data_vacinacao=data)
            agendamento.save()

            messages.success(request, "Agendamento confirmado com sucesso")
            return redirect('index')

def sair(request):
    auth.logout(request)
    return redirect('/cidadao/')
