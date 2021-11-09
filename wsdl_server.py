# framework utilizados nesse modulo
import logging
from datetime import datetime
from typing import Text
from spyne import Application, rpc, ServiceBase, \
    Unicode, Integer, AnyDict, ComplexModel, srpc, Array,XmlAttribute
from spyne.model.primitive import string
from spyne.model.primitive.number import Int
from spyne.model.primitive.string import String
from spyne.protocol import soap
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import log
from wsgiref.simple_server import make_server
# modulo responsavel por criptografar ou descriptografar
from base64 import b64decode, decode
from sql import insertResultado, updateSilanexa,updateStatusErro  # modulo que fica os sql
from config import ConexaoDb  # modulo de comunicação com banco
from spyne import Iterable

logging.basicConfig(filename='/opt/ws_anima_8000/logs/server.log',
                    format='%(asctime)s %(message)s', level=logging.INFO)
formatLOG = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

# ip porta
host = '0.0.0.0'
port = 8000

# monta o parse de response do sucesso ou erro

class CriteriaModel(ComplexModel):
    acao = String
    crmProfissionalResponsavel = String
    exames = AnyDict()
    #hashSha512 = String
    #idPaciente = String
    #laudo = Text
    nomePaciente = String

class Status(ComplexModel):
    id = Integer
    motivo = String

class ReturnStatus(ComplexModel):
    __namespace__ = "http://ws.integracaoresultados.spdata.com.br/"
    examesImportados = Iterable(Integer,wrapped=False)
    examesComErro = Iterable(Status.customize(max_occurs="unbounded"),wrapped=False)
    erroConexao = Status.customize(max_occurs="unbounded") 

""" class examesComErro(ComplexModel):
    id = Integer
    motivo = String """

class ResultadoPedido(ServiceBase):
    __namespace__ = "http://ws.integracaoresultados.spdata.com.br/"



    @rpc(Unicode, Unicode, Unicode,Array(CriteriaModel, wrapped=False), _returns=(ReturnStatus))
    def enviar(ctx,senha,pedido,cnpj,resultados):
       
        senha = senha
        if senha == 'matrix@@2021':
            a = []
            for x in resultados:    
                obj = x
                exames = obj.exames
                validador = 'itens' in exames
                codexames = exames['codigo'][0]
                itPedido = exames['id'][0]
                data = exames['dataHora'][0]
                dtReplace = data.replace('T', ' ')
                dates = datetime.strptime(
                    dtReplace, '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%Y')
                datestime = datetime.strptime(
                    dtReplace, '%Y-%m-%d %H:%M:%S').strftime('%H:%M:%S')
                #decodLaudo = b64decode(laudo[0],validate=False)
                crm = obj.crmProfissionalResponsavel
                if validador == True:
                    itens = exames['itens']
                    for x in itens:
                        elemento = x['codigo'][0]

                        validaResult = 'resultado' in x
                        validaRef = 'valorReferencia' in x
                        
                        if validaResult is True:
                            resultado = x['resultado'][0]
                        else :
                            resultado =None
                        if validaRef is True:
                            vlRef = (x['valorReferencia'][0])
                        else:
                            vlRef = None
                            
                        dbInsert = ConexaoDb()
                        # faz insert na tabela sires01 do resultado
                        logsDb=dbInsert.executeAny(insertResultado, 
                            int(itPedido), int(itPedido), int(itPedido), int(itPedido), int(
                                itPedido), int(itPedido), int(codexames), int(itPedido),
                            int(elemento),
                            str(resultado),dates, int(itPedido), int(itPedido), int(
                                itPedido), int(itPedido), int(crm), int(crm),vlRef,datestime
                            )
                        if logsDb == 0:
                            dbInsert.execute(updateSilanexa, itPedido)
                            my_statusCode = itPedido
                            status = itPedido
                        else:
                            my_statusCode = itPedido
                            status = itPedido
                            my_statusMsg = str(logsDb)
                            statusErro = ReturnStatus()
                            statusErro.examesComErro = [
                                    {'id': my_statusCode, 'motivo': my_statusMsg}]
                            logretorno = (statusErro)
                            log.LOG_insert("/opt/ws_anima_8000/logs/retorno.log", formatLOG,
                                        logretorno, logging.INFO) 
                            #status = examesComErro(id = my_statusCode,motivo= my_statusMsg)
                            #status = {'examesComErro':{'id':my_statusCode,'motivo':my_statusMsg}}
                    a.append(status)
                                        
                    #return status
                else:
                    dbInsert = ConexaoDb()
                    validaResult = 'resultado' in exames
                    validaRef = 'valorReferencia' in exames
                    if validaResult is True:
                        resultado = exames['resultado'][0]
                    else :
                        resultado =None
                    if validaRef is True:
                        vlRef = (exames['valorReferencia'][0])
                    else:
                        vlRef = None
                    logsDb =dbInsert.executeAny(insertResultado,
                        int(itPedido), int(itPedido), int(itPedido), int(itPedido), int(
                            itPedido), int(itPedido), codexames, int(itPedido),
                        0,
                        str(resultado), dates, int(itPedido), int(itPedido), int(
                            itPedido), int(itPedido), int(crm), int(crm), vlRef,datestime
                    ) 
                    if logsDb == 0:
                        dbInsert.execute(updateSilanexa, itPedido)
                        status = itPedido
                        #status = {'examesImportados':my_statusCode}
                        
                    else:
                        my_statusCode = itPedido
                        status = itPedido
                        my_statusMsg = str(logsDb)
                        statusErro = ReturnStatus()
                        statusErro.examesComErro = [
                                {'id': my_statusCode, 'motivo': my_statusMsg}]
                        logretorno = (statusErro)
                        log.LOG_insert("/opt/ws_anima_8000/logs/retorno.log", formatLOG,
                                    logretorno, logging.INFO) 
                        
                        
                    a.append(status)
            
            b = ReturnStatus(examesImportados = (a))
                
                
            return b          
        else:
            my_statusCode = 1
            my_statusMsg = 'senha inválida'
            status = ReturnStatus()
            status.erroConexao = [
                        {'id': my_statusCode, 'motivo': my_statusMsg}]
            logretorno = (str(status))
            log.LOG_insert("/opt/ws_anima_8000/logs/retorno.log", formatLOG,
                               logretorno, logging.INFO)
            return logretorno
        
        
       

def on_method_return_string(ctx):

  #  ctx.out_string[0] = ctx.out_string[0].replace(b'tns:enviarResponse', b'ns2:enviarResponse ')
    ctx.out_string[0] = ctx.out_string[0].replace(
        b'tns:enviarResult>', b'retorno>')
    ctx.out_string[0] = ctx.out_string[0].replace(
        b'tns:examesImportados>', b'examesImportados>')
    ctx.out_string[0] = ctx.out_string[0].replace(
        b'tns:examesComErro>', b'examesComErro>')
    ctx.out_string[0] = ctx.out_string[0].replace(b'tns:id>', b'id>')
    ctx.out_string[0] = ctx.out_string[0].replace(b'tns:motivo>', b'motivo>')
    ctx.out_string[0] = ctx.out_string[0].replace(
        b'soap11env:Envelope', b'soap:Envelope')
    ctx.out_string[0] = ctx.out_string[0].replace(
        b'soap11env:Body', b'soap:Body')
    ctx.out_string[0] = ctx.out_string[0].replace(
        b'xmlns:soap11env', b'xmlns:soap')


# modificador da estrura reponse padrão para personalizado
ResultadoPedido.event_manager.add_listener('method_return_string',
                                           on_method_return_string)

# disponibiliza o metódo para ser acessado pelo ws cliente
application = Application([ResultadoPedido],
                          tns='http://ws.integracaoresultados.spdata.com.br/',
                          in_protocol=Soap11(validator=None,huge_tree=True),
                          out_protocol=Soap11(polymorphic=True),
                          )

if __name__ == '__main__':
    server = make_server(host, port,
                         WsgiApplication(application,max_content_length=50*0x100000))
    logging.info("listening to http://10.11.9.135:8000")
    logging.info("wsdl is at: http://10.11.9.135:8000/?wsdl")
    server.serve_forever()

