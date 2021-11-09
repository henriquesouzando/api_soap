from zeep import Client
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep.transports import Transport
from zeep.exceptions import Fault

def envia_pedido(r):
  try:   
    wsdl = 'http://srv1374.corp.medgrupo.net/MatrixNET/wsrvSPDATA.SPDATAHA.svc?wsdl' #variável que recebe a url do ws terceiro
    session = Session() #variável que recebe o metodo session
    session.auth = HTTPBasicAuth('SPDATAHA', 'MATRIX') #passando os parametros de usuario e senha via http para o ws terceiro
    client = Client(wsdl=wsdl, transport=Transport(session=session)) #variável que receber o método Client passando os parametros outras variáveis para conectar com o ws terceiro
    response = client.service.RecebeRequisicaoSpdata(**r) #variável de envio dos pedidos e retorno.
  except Fault as fault:
    response = Client.wsdl.types.deserialize(fault.detail[0])#erro caso não consiga conectar com o terceiro
  return response

if __name__ == "__main__":
  envia_pedido()