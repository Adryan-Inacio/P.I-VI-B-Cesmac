import hashlib
import secrets
from django.db import models
from django.contrib.auth.models import User
from .encryption import criptografar_texto, descriptografar_texto


def gerar_protocolo_hash():
    semente = secrets.token_bytes(32)
    digest = hashlib.sha256(semente).hexdigest().upper()
    return f"TL-{digest[:4]}-{digest[4:8]}-{digest[8:12]}"


class Denuncia(models.Model):
    PERFIL_CHOICES = [
        ('colaborador', 'Colaborador (Funcionário)'),
        ('parceiro', 'Parceiro / Prestador de Serviço'),
        ('terceiro', 'Terceiro (Público Externo)'),
    ]

    CATEGORIA_CHOICES = [
        ('vazamento', 'Vazamento de Dados Pessoais/Sensíveis'),
        ('pratica_inadequada', 'Prática Inadequada de Segurança da Informação'),
        ('atividade_suspeita', 'Atividade Suspeita / Acesso Indevido'),
    ]

    STATUS_CHOICES = [
        ('recebida', 'Recebida'),
        ('em_analise', 'Em Análise Técnica'),
        ('mitigada', 'Incidente Contido / Mitigado'),
        ('concluida', 'Concluída'),
    ]

    protocolo = models.CharField(
        max_length=20,
        unique=True,
        default=gerar_protocolo_hash,
        editable=False,
        verbose_name='Protocolo Hash'
    )
    perfil_denunciante = models.CharField(
        max_length=20,
        choices=PERFIL_CHOICES,
        verbose_name='Vínculo com a Empresa'
    )
    categoria = models.CharField(
        max_length=30,
        choices=CATEGORIA_CHOICES,
        verbose_name='Tipo de Incidente'
    )
    empresa_ou_setor = models.CharField(
        max_length=150,
        verbose_name='Empresa ou Setor Envolvido'
    )
    data_incidente = models.DateField(
        verbose_name='Data Aproximada do Ocorrido'
    )

    # Campos armazenados criptografados em repouso
    relato_criptografado = models.TextField(
        verbose_name='Relato Detalhado (Criptografado)'
    )
    identificacao_criptografada = models.TextField(
        blank=True,
        default='',
        verbose_name='Identificação Sigilosa Opcional (Criptografada)'
    )

    anonima = models.BooleanField(
        default=True,
        verbose_name='Denúncia Anônima'
    )
    consentimento_lgpd = models.BooleanField(
        default=True,
        verbose_name='Ciência e Consentimento LGPD'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='recebida',
        verbose_name='Status da Apuração'
    )
    parecer_investigador = models.TextField(
        blank=True,
        default='',
        verbose_name='Resposta / Atualização ao Denunciante'
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-criado_em']
        verbose_name = 'Denúncia'
        verbose_name_plural = 'Denúncias'

    def __str__(self):
        return f"{self.protocolo} - {self.get_categoria_display()}"

    def definir_dados_sensiveis(self, relato_texto: str, identificacao_texto: str = ''):
        self.relato_criptografado = criptografar_texto(relato_texto)
        if identificacao_texto and identificacao_texto.strip():
            self.identificacao_criptografada = criptografar_texto(identificacao_texto.strip())
            self.anonima = False
        else:
            self.identificacao_criptografada = ''
            self.anonima = True

    @property
    def relato_legivel(self) -> str:
        return descriptografar_texto(self.relato_criptografado)

    @property
    def identificacao_legivel(self) -> str:
        if self.anonima or not self.identificacao_criptografada:
            return 'Anônimo (Nenhum dado pessoal coletado)'
        return descriptografar_texto(self.identificacao_criptografada)

    def anonimizar_titular(self):
        """Exerce o direito do titular (LGPD Art. 18) removendo dados identificáveis."""
        self.identificacao_criptografada = ''
        self.anonima = True
        self.save(update_fields=['identificacao_criptografada', 'anonima', 'atualizado_em'])


class TrilhaAuditoria(models.Model):
    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Responsável pelo Acesso'
    )
    protocolo_denuncia = models.CharField(
        max_length=20,
        verbose_name='Protocolo Acessado'
    )
    acao = models.CharField(
        max_length=255,
        verbose_name='Ação Realizada'
    )
    data_hora = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data e Hora'
    )

    class Meta:
        ordering = ['-data_hora']
        verbose_name = 'Registro de Auditoria'
        verbose_name_plural = 'Trilha de Auditoria'

    def __str__(self):
        ator = self.usuario.username if self.usuario else 'Titular/Sistema'
        return f"[{self.data_hora:%d/%m/%Y %H:%M}] {ator} -> {self.acao} ({self.protocolo_denuncia})"