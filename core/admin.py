from django.contrib import admin
from core.models import Cidadao, EstabelecimentoSaude
    
class CidadaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'nascimento', 'cpf')

class EstabelecimentoSaudeAdmin(admin.ModelAdmin):
    list_display = ('id', 'cnes', 'fantasia', 'bairro')
    search_fields = ['dados_estabelecimento__CO_CNES', 'dados_estabelecimento__NO_FANTASIA']

    def cnes(self, instance):
        data = instance.dados_estabelecimento
        return data["CO_CNES"]

    def fantasia(self, instance):
        data = instance.dados_estabelecimento
        return data["NO_FANTASIA"] 

    def bairro(self, instance):
        data = instance.dados_estabelecimento
        return data["NO_BAIRRO"]  

admin.site.register(Cidadao, CidadaoAdmin)
admin.site.register(EstabelecimentoSaude, EstabelecimentoSaudeAdmin)