import fdb
from fdb.ibase import paramdsc
import log
import logging
formatLOG = logging.Formatter('%(asctime)s %(levelname)s %(message)s')


class ConexaoDb:
    def __init__(self):
        connected = False
        while not connected:
            try: 
                self.con = fdb.connect(
                host='10.1.1.23', database='/home/BancoProd/SGHDADOS.1829',
                user='SYSDBA', password='Ad@amina@1829')
                self.cursor = self.con.cursor()
                #sucesso = "Banco conectado com sucesso!!"
                #log.LOG_insert("logs/dba.log", formatLOG , sucesso, logging.INFO)
                connected = True
            except fdb.Error as err: 
                err = 'There is an error in the Firebird database:', err            
                log.LOG_insert("logs/dba.log", formatLOG , err, logging.INFO) 
                
   
    def queryOne(self,sql):
        try:
            self.cursor.execute(sql)
            a = self.cursor.fetchonemap()
            #print(a)
            self.con.rollback()

            #self.cursor.close()
            #self.con.close()  
        except fdb.Error as err:
            info = 'fdb:', err   
        return a  
        
    """  def queryAll(self,sql,*parms):
        try:
            self.cursor.execute(sql,parms)
            b = self.cursor.fetchallmap()
            #print(b)
            self.con.rollback()
            #self.cursor.close()
            #self.con.close() 
        except fdb.Error as err:
            info = 'fdb:', err   
        return b
 """
    def execute(self,sql,*parms):
        try:
            self.cursor.execute(sql,parms)
            self.con.commit()
            #self.con.close()  
            info = 'Update com sucesso' 
        except fdb.Error as err:
            info = 'fdb:', err   
        return info    

    def executeAny(self,sql,*parms):
        try:
            
            self.cursor.execute(sql,(parms))  
            #self.cursor.close()
            self.con.commit()
            #self.con.close()  
            info = 0 
        except fdb.Error as err:
            info = 'fdb:', err 
        return info    

if __name__ == "__main__": 
    ConexaoDb()

