from sql import pedido
from config import ConexaoDb
from codecs import encode
import base64

def parse_xml():
    db = ConexaoDb()
    ped = db.queryOne(pedido) 
    #db.cursor.close()
    if ped == None:
        dados =None
        vitpedido=None
        return dados,vitpedido
    else:  
        valida_rn = ped['RN']
        if valida_rn == 'F':
            dados = {
            'Operacao':{
                'solicitacao':{
                    'acao':'I',
                    'ato': ped['ATO'],
                    'Id_solicitacao':ped['PEDIDO'],
                    'local_atendimento':11, # multiempresa       
                    'id_paciente':ped['PRONTUARIO'],
                    'nome_paciente':ped['NOME_PACIENTE'],
                    'data_nascimento':ped['NASC'],
                    'sexo':ped['SEXO'],
                    'nome_mae':ped['NOME_MAE'],
                    'bloco':ped['HORA'],
                    'acomodacao':ped['DESC_ACOMO'],
                    'leito': ped['LEITO'],
                    'crm_medico':ped['CRM_SOLICITANTE'],
                    'nome_medico':ped['MEDICO_SOLICITANTE'],
                    'ufmedico':ped['UF'],
                    'convenio':0,
                    'unidade':'0'+str(ped['UNIDADE']), 
                    'exames':{
                        'acao':'I',
                        'id_lanc_exame':ped['ITPEDIDO'],
                        'codigo_exame':ped['SIGLA'],
                        'obs_exame':base64.b64encode(str(ped['OBS']).encode("utf-8")),
                        'urgencia':ped['URGENCIA'],
                        'codigo_material':ped['MATERIAL']
                    }
                }
            }
            }
        else:
            dados = {
            'Operacao':{
                'solicitacao':{
                    'acao':'I',
                    'ato': ped['ATO'],
                    'Id_solicitacao':ped['PEDIDO'],
                    'local_atendimento':11, # multiempresa       
                    'id_paciente':ped['PRONTUARIO'],
                    'nome_paciente':('RN DE '+ped['NOME_PACIENTE']),
                    'data_nascimento':ped['NASC'],
                    'sexo':ped['SEXO'],
                    'nome_mae':ped['NOME_MAE'],
                    'bloco':ped['HORA'],
                    'acomodacao':ped['DESC_ACOMO'],
                    'leito': ped['LEITO'],
                    'crm_medico':ped['CRM_SOLICITANTE'],
                    'nome_medico':ped['MEDICO_SOLICITANTE'],
                    'ufmedico':ped['UF'],
                    'convenio':0,
                    'unidade':'0'+str(ped['UNIDADE']), 
                    'exames':{
                        'acao':'I',
                        'id_lanc_exame':ped['ITPEDIDO'],
                        'codigo_exame':ped['SIGLA'],
                        'obs_exame':base64.b64encode(str(ped['OBS']).encode("utf-8")),
                        'urgencia':ped['URGENCIA'],
                        'codigo_material':ped['MATERIAL']
                    }
                }
            }
            }
        vitpedido = ped['ITPEDIDO']
        db.cursor.close()
        db.con.close() 
        return dados,vitpedido
#print(parse_xml())
if __name__ == "__main__":
    parse_xml()
