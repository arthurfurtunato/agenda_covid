from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import requests

from core.models import EstabelecimentoSaude

class Command(BaseCommand):
    help = 'Carrega as informações dos estabelecimentos na base de dados.'

    def handle(self, *args, **options):
        content = requests.get(settings.ESTABELECIMENTOS_URL)
        estabelecimentos = content.json() #Carrega o arquivo json
        for e in estabelecimentos:
            estab = EstabelecimentoSaude(dados_estabelecimento=e)
            estab.save()
            print(f'{e["CO_CNES"]} - {estab.id}')