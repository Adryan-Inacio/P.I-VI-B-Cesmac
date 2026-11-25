from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Denuncia, TrilhaAuditoria
from .forms import DenunciaForm, ConsultaProtocoloForm, TratamentoDenunciaForm


def index(request):
    """Página inicial com visão ética, pilares LGPD e atalhos principais."""
    return render(request, 'denuncias/index.html')


def politica_privacidade(request):
    """Página de Transparência Real (LGPD Art. 6º) em linguagem clara."""
    return render(request, 'denuncias/privacidade.html')


def registrar_denuncia(request):
    """Formulário seguro para envio anônimo ou sigiloso."""
    if request.method == 'POST':
        form = DenunciaForm(request.POST)
        if form.is_valid():
            denuncia = form.save(commit=False)
            relato_limpo = form.cleaned_data['relato']
            identificacao_limpa = form.cleaned_data.get('identificacao_opcional', '')

            denuncia.definir_dados_sensiveis(relato_limpo, identificacao_limpa)
            denuncia.save()

            TrilhaAuditoria.objects.create(
                usuario=None,
                protocolo_denuncia=denuncia.protocolo,
                acao='Registro de nova denúncia realizado no portal.'
            )

            return render(request, 'denuncias/sucesso.html', {
                'protocolo': denuncia.protocolo,
                'anonima': denuncia.anonima
            })
    else:
        form = DenunciaForm()

    return render(request, 'denuncias/registrar.html', {'form': form})


def consultar_denuncia(request):
    """Permite ao denunciante acompanhar o status via hash e exercer direitos LGPD."""
    denuncia = None
    nao_encontrada = False

    if request.method == 'POST':
        form = ConsultaProtocoloForm(request.POST)
        if form.is_valid():
            codigo = form.cleaned_data['protocolo'].strip().upper()
            try:
                denuncia = Denuncia.objects.get(protocolo=codigo)
            except Denuncia.DoesNotExist:
                nao_encontrada = True
    else:
        codigo_get = request.GET.get('protocolo', '').strip().upper()
        if codigo_get:
            form = ConsultaProtocoloForm(initial={'protocolo': codigo_get})
            try:
                denuncia = Denuncia.objects.get(protocolo=codigo_get)
            except Denuncia.DoesNotExist:
                nao_encontrada = True
        else:
            form = ConsultaProtocoloForm()

    return render(request, 'denuncias/consultar.html', {
        'form': form,
        'denuncia': denuncia,
        'nao_encontrada': nao_encontrada
    })


def anonimizar_dados_titular(request, protocolo):
    """Direito do Titular (Art. 18 LGPD): exclui/anonimiza a identificação pessoal."""
    if request.method == 'POST':
        denuncia = get_object_or_404(Denuncia, protocolo=protocolo)
        if not denuncia.anonima:
            denuncia.anonimizar_titular()
            TrilhaAuditoria.objects.create(
                usuario=None,
                protocolo_denuncia=denuncia.protocolo,
                acao='Titular exerceu direito LGPD (Art. 18): dados identificáveis eliminados.'
            )
            messages.success(
                request,
                'Seus dados de identificação foram permanentemente removidos. A denúncia permanece ativa de forma 100% anônima.'
            )
        return redirect(f"/consultar/?protocolo={denuncia.protocolo}")
    return redirect('consultar_denuncia')


@login_required
def painel_admin(request):
    """Painel restrito aos investigadores/administradores autorizados."""
    status_filtro = request.GET.get('status', '')
    denuncias = Denuncia.objects.all()
    if status_filtro:
        denuncias = denuncias.filter(status=status_filtro)

    metricas = {
        'total': Denuncia.objects.count(),
        'recebidas': Denuncia.objects.filter(status='recebida').count(),
        'em_analise': Denuncia.objects.filter(status='em_analise').count(),
        'mitigadas': Denuncia.objects.filter(status='mitigada').count(),
        'concluidas': Denuncia.objects.filter(status='concluida').count(),
    }

    auditorias = TrilhaAuditoria.objects.all()[:15]

    return render(request, 'denuncias/painel_admin.html', {
        'denuncias': denuncias,
        'metricas': metricas,
        'auditorias': auditorias,
        'status_filtro': status_filtro
    })


@login_required
def detalhe_denuncia_admin(request, protocolo):
    """Leitura descriptografada e tratamento da denúncia com registro na trilha de auditoria."""
    denuncia = get_object_or_404(Denuncia, protocolo=protocolo)

    if request.method == 'POST':
        form = TratamentoDenunciaForm(request.POST, instance=denuncia)
        if form.is_valid():
            form.save()
            TrilhaAuditoria.objects.create(
                usuario=request.user,
                protocolo_denuncia=denuncia.protocolo,
                acao=f"Atualizou status para '{denuncia.get_status_display()}' e registrou parecer."
            )
            messages.success(request, f'Denúncia {denuncia.protocolo} atualizada com sucesso.')
            return redirect('detalhe_denuncia_admin', protocolo=denuncia.protocolo)
    else:
        form = TratamentoDenunciaForm(instance=denuncia)
        
        TrilhaAuditoria.objects.create(
            usuario=request.user,
            protocolo_denuncia=denuncia.protocolo,
            acao='Visualizou o conteúdo descriptografado da denúncia.'
        )

    logs_denuncia = TrilhaAuditoria.objects.filter(protocolo_denuncia=denuncia.protocolo)

    return render(request, 'denuncias/detalhe_admin.html', {
        'denuncia': denuncia,
        'form': form,
        'logs_denuncia': logs_denuncia
    })