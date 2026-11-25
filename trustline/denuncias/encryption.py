from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings


def _get_cipher():
    return Fernet(settings.FERNET_KEY)


def criptografar_texto(texto: str) -> str:
    if not texto:
        return ''
    cipher = _get_cipher()
    return cipher.encrypt(texto.encode('utf-8')).decode('utf-8')


def descriptografar_texto(texto_cifrado: str) -> str:
    if not texto_cifrado:
        return ''
    cipher = _get_cipher()
    try:
        return cipher.decrypt(texto_cifrado.encode('utf-8')).decode('utf-8')
    except InvalidToken:
        return '[Erro de integridade ou dado anonimizado]'