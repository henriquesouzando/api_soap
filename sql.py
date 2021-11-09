pedido = """
SELECT 
    FIRST 1
    CAST(ITPEDIDO.ID AS INT) ITPEDIDO  ,
    ITPEDIDO.DATA,
    lpad( ITPEDIDO.hora,2,'0') HORA,
    ITPEDIDO.ATO ,
    PEDIDO.REG ||  REPLACE(ITPEDIDO.data,'-','')|| lpad( ITPEDIDO.hora,2,'0') PEDIDO,
    CAST(PEDIDO.ID AS INT) COD_PEDIDO,
    PACIENTE.PRONT PRONTUARIO,
    PACIENTE.NOME NOME_PACIENTE,
    PACIENTE.MAE NOME_MAE,
    extract(year from PACIENTE.NASC) || '/'
        || lpad(extract(month from PACIENTE.NASC),2,'0') || '/'
        || lpad(extract(day from PACIENTE.NASC),2,'0') NASC  ,
   decode(PACIENTE.SEXO,
    'F','FEMININO',
    'M','MASCULINO') SEXO ,
   LEITO.cod_leito leito,
   setor.cod DESC_ACOMO,
   pedido.unidade,
   CRM.COD CRM_SOLICITANTE,
   MEDICO.NOME MEDICO_SOLICITANTE,
   CRM.UF,
    EXAME.id SIGLA,
    ITPEDIDO.OBS,
    ITPEDIDO.URG URGENCIA,
    EXAME.MATERIAL ,
    LPAD(ITPEDIDO.HORA,2,'0'),
    ITPEDIDO.RN
    FROM   RICADPAC     PACIENTE
    INNER JOIN  ATCABECATEND  ATEND  ON ATEND.id_ricadpac = PACIENTE.id
    INNER JOIN SICADATE PEDIDO ON PEDIDO.id_atcabecatend = ATEND.id
    INNER JOIN SILANEXA ITPEDIDO ON ITPEDIDO.id_sicadate = PEDIDO.ID
    INNER JOIN SITABPRO EXAME  ON EXAME.codalf = ITPEDIDO.exame     AND ITPEDIDO.ato = EXAME.ATO
    INNER JOIN tbcencus C ON C.cod = ITPEDIDO.cdc
    LEFT join tbleito leito on leito.id = atend.id_tbleito
    INNER join tbcencus setor on setor.cod = pedido.cdc
    INNER JOIN   tbcbopro CRM ON CRM.id  = PEDIDO.id_tbcbopro_solicitante
    INNER JOIN   TBPROFIS  MEDICO ON MEDICO.id = CRM.id_tbprofis

    WHERE
     ITpedido.data = current_date
    and exame.id not in ( select id from sitabpro where ato not in (15) and situacao = 'A')
    and COALESCE(ITPEDIDO.coletor,0) = 0
    AND ITPEDIDO.ATO IN (15)
    --AND ITPEDIDO.pend_sadt = 'F'
    ORDER BY
    1

"""
updateStatusPedido = """
       UPDATE SILANEXA  SET COLETOR = 2, COLETA = current_date, HRCOL = current_TIME  WHERE
            COALESCE(coletor,0) = 0
            AND ATO IN (15)
            AND ID =  ?
    """
updateStatusErro = """
        update silanexa set COLETOR = 3   where
                    COALESCE(coletor,0) = 0
                    AND ATO IN (15)
                    AND ID =  ?
                    """

insertResultado = """
 insert into sires01 (
ID,
ID_SILANEXA,
DATA,
DATA_HORA_INCLUSAO,
REG,
CONTA,
ATEND,
ATO,
EXAME,
SEQUENCIA,
ELEMENTO,
ALFA,
DATARES,
HORA,
CRM,
MEDICO,
ID_TBCBOPRO_SOLICITANTE,
CRM_EMISSOR,
EMISSOR  ,
ID_TBCBOPRO_EMISSOR,
AMOSTRA,
DATA_HORA_RES
)
 VALUES(
   GEN_ID(GEN_SIRES01_ID, 1),
   ?,
   (SELECT DATA FROM SILANEXA WHERE ID = ?),
   current_time, 
   (select reg from silanexa where id = ?),
   (select CONTA from silanexa where id = ?),
   (select ATEND from silanexa where id = ?) ,
   (select ATO from silanexa where id = ?),
    (select codalf from sitabpro where  id = ?),
    (select SEQUENCIA from silanexa where id = ?),
    ?,
    ?,
    ?,
    (SELECT (substring(HORA from 1 for 2)||':'||substring(HORA from 3 for 2)||':'||'00') HORA FROM SILANEXA WHERE ID =?),
      (select CRMSOLICITANTE from silanexa where id = ?),
      (select NSOLICITANTE from silanexa where id = ?),
      (select ID_TBCBOPRO_SOLICITANTE from silanexa where id = ?),
      ?,
     ( SELECT FIRST 1 MEDICO.NOME FROM  tbcbopro CRM
      INNER JOIN   TBPROFIS  MEDICO ON MEDICO.id = CRM.id_tbprofis
      WHERE CRM.COD = ?  ),
      ( SELECT FIRST 1 crm.id FROM  tbcbopro CRM
      WHERE CRM.COD = 0  ),
      ?,
      ?
 )
"""
updateSilanexa= """
         UPDATE SILANEXA  SET RESLIB = 'T',DIGRES = 'T',EMIRES = 'T', DATA_HORA_LIBERA_EXAME_UTC = current_timestamp  WHERE ID =  ?
    """