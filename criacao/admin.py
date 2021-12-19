from django.contrib import admin

from criacao.models import boi, brinco, cabecagado, cria, ficha_medica, matriz, vacinas, transacao, cabeca_transacionada




# Register your models here.
admin.site.register(matriz)
admin.site.register(cabecagado)
admin.site.register(cria)
admin.site.register(vacinas)
admin.site.register(ficha_medica)
admin.site.register(boi)
admin.site.register(brinco)
admin.site.register(transacao)
admin.site.register(cabeca_transacionada)