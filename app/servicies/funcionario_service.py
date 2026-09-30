
from app.repositories.funcionario_repository import gerar_codigo
def criar_codigo(material, kg, uid):
    return gerar_codigo(material, kg, uid)
