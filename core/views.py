from django.core.checks import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

def inicio(request):
    return redirect('index')

def index(request):
    return render(request, 'index.html')

def cadastrar(request):
    if request.method != 'POST':
        return render(request, 'cadastrar.html')

    nome = request.POST.get('nome')
    nascimento = request.POST.get('nascimento')
    cpf = request.POST.get('cpf')
    senha = request.POST.get('senha')
    senha2 = request.POST.get('senha2')

    if not nome or not nascimento or not cpf or not senha or not senha2:
        messages.add_message(request, messages.ERROR, 'Algum campo está vazio.')
        return render(request, 'cadastrar.html')

    if senha != senha2:
        messages.error(request, 'As senhas não conferem.')
        return render(request, 'cadastrar.html')

    if len(cpf) != 11:
        messages.error(request, 'CPF inválido.')
        return render(request, 'cadastrar.html')


    return render(request, 'cadastrar.html')

def entrar(request):
    return render(request, 'entrar.html')

def agendar(request):
    return render(request, 'agendar.html')
