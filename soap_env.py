import asyncio
from parse import parse_xml
from soap import envia_pedido
import logging
import log
from sql import updateStatusPedido,updateStatusErro
from config import ConexaoDb
import gc

formatLOG = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

async def soap_envia():
    while True:

        xml_parse,itpedido= parse_xml()
       # print (xml_parse)
        #print(pedido is None)
        if xml_parse != None and itpedido != None:
           # hora=xml_parse['Operacao']['solicitacao']['bloco']
            #pedido = xml_parse['Operacao']['solicitacao']['Id_solicitacao']
            #print(xml_parse)
            #print(xml_parse)
            retorno = envia_pedido(xml_parse)
            db = ConexaoDb()
            if retorno['codigo'] == '0':
                logdb = db.execute(updateStatusPedido,itpedido) 
                db.con.close()
            else:
                logdb = db.execute(updateStatusErro,itpedido) 
                db.con.close() 
                log_retorno = (str(itpedido) + str(retorno)+ str(logdb))  
                log.LOG_insert("logs/soap_env.log", formatLOG ,log_retorno, logging.INFO)            
        else:
            pass
        
        for i in range(2):
            gc.collect()
            gc.garbage
        await asyncio.sleep(1)

async def main():
    #await asyncio.sleep(1)
    await asyncio.ensure_future(soap_envia())
    #await asyncio.sleep(1)
    
if __name__ == "__main__":
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main()) 
   