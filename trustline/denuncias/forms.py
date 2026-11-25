from django import forms
from .models import Denuncia


class DenunciaForm(forms.ModelForm):
    relato = forms.CharField(
        label='Relato Detalhado do Incidente',
        widget=forms.Textarea(attrs={
            'rows': 5,
            'placeholder': 'Descreva o que aconteceu, quais dados foram expostos ou qual falha de segurança foi identificada. Evite inserir seus próprios dados pessoais aqui caso deseje permanecer anônimo.',
            'class': 'form-control'
        })
    )
    identificacao_opcional = forms.CharField(
        label='Identificação Sigilosa (Opcional — deixe em branco para envio 100% anônimo)',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ex.: Nome ou e-mail para contato sigiloso (será criptografado)',
            'class': 'form-control'
        })
    )
    consentimento_lgpd = forms.BooleanField(
        required=True,
        label='Li e concordo com a Política de Privacidade e Finalidade (LGPD): declaro ciência de que as informações enviadas serão tratadas exclusivamente para apuração do incidente de segurança.',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Denuncia
        fields = [
            'perfil_denunciante',
            'categoria',
            'empresa_ou_setor',
            'data_incidente',
            'consentimento_lgpd',
        ]
        widgets = {
            'perfil_denunciante': forms.Select(attrs={'class': 'form-select'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'empresa_ou_setor': forms.TextInput(attrs={
                'placeholder': 'Ex.: Empresa Alfa / Setor de TI ou RH',
                'class': 'form-control'
            }),
            'data_incidente': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
        }


class ConsultaProtocoloForm(forms.Form):
    protocolo = forms.CharField(
        max_length=20,
        label='Código de Protocolo Hash',
        widget=forms.TextInput(attrs={
            'placeholder': 'Ex.: TL-A1B2-C3D4-E5F6',
            'class': 'form-control text-uppercase'
        })
    )


class TratamentoDenunciaForm(forms.ModelForm):
    class Meta:
        model = Denuncia
        fields = ['status', 'parecer_investigador']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'parecer_investigador': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Escreva uma atualização ou medida de mitigação adotada (visível ao denunciante ao consultar o protocolo).',
                'class': 'form-control'
            }),
        }