from django.contrib import admin
from .models import Denuncia, TrilhaAuditoria


@admin.register(Denuncia)
class DenunciaAdmin(admin.ModelAdmin):
    list_display = ('protocolo', 'categoria', 'perfil_denunciante', 'empresa_ou_setor', 'anonima', 'status', 'criado_em')
    list_filter = ('status', 'categoria', 'anonima', 'perfil_denunciante')
    search_fields = ('protocolo', 'empresa_ou_setor')
    readonly_fields = ('protocolo', 'relato_criptografado', 'identificacao_criptografada', 'criado_em', 'atualizado_em')


@admin.register(TrilhaAuditoria)
class TrilhaAuditoriaAdmin(admin.ModelAdmin):
    list_display = ('data_hora', 'usuario', 'protocolo_denuncia', 'acao')
    list_filter = ('usuario', 'data_hora')
    search_fields = ('protocolo_denuncia', 'acao')
    readonly_fields = ('usuario', 'protocolo_denuncia', 'acao', 'data_hora')