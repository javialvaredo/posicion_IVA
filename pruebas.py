import pyodbc
from decimal import Decimal
from datetime import datetime
from query import Query

class ConexionSql:
    def __init__(self, Driver="", Server="", Database="", Trusted_C="yes", usuario="", contrasenia=""):
        self.driver = Driver
        self.server = Server
        self.database = Database
        self.trusted_C = Trusted_C
        self.usuario = usuario
        self.contrasenia = contrasenia

    def get_connection_string(self):
        if self.trusted_C.lower() == "yes":
            return f"DRIVER={self.driver};SERVER={self.server};DATABASE={self.database};Trusted_Connection=yes;"
        else:
            return f"DRIVER={self.driver};SERVER={self.server};DATABASE={self.database};UID={self.usuario};PWD={self.contrasenia};"

    def connect(self):
        try:
            self.connection = pyodbc.connect(self.get_connection_string())
            self.cursor = self.connection.cursor()
            print("Connection successful")
        except Exception as e:
            print(f"Error connecting to database: {e}")

    def execute_query(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
            print("Query executed successfully")
        except Exception as e:
            print(f"Error executing query: {e}")

    def fetch_all(self, query):
        try:
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            return results
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None

    def close(self):
        try:
            self.cursor.close()
            self.connection.close()
            print("Connection closed successfully")
        except Exception as e:
            print(f"Error closing the connection: {e}")


class IVA_ventas_ant:

    def __init__(self, lista):
        self.lista = lista
        self.suma_iva_pesos = 0

    def convertir_formato_lista(self):
        
        for i in range(len(self.lista)):
            
            fecha_emis = self.lista[i][0]
            fecha_emis = fecha_emis.strftime('%d-%m-%Y')
            tcomp = self.lista[i][1]
            n_comp = self.lista[i][2]
            importe_gr = round(self.lista[i][3], 2)

            cotiz = round(self.lista[i][4],2)
            importe_iv = round(self.lista[i][5], 2)
            
            if cotiz > 1:
                iva_pesos = round(cotiz * importe_iv, 2)
            else:
                iva_pesos = 1 * round(importe_iv, 2) 
            
            if tcomp == 'N/C'or tcomp == 'CDC' or tcomp == 'CRI':
                importe_gr = -importe_gr
                importe_iv = -importe_iv
                iva_pesos = -iva_pesos

            self.suma_iva_pesos += iva_pesos 
                                
            print(fecha_emis, tcomp, n_comp, importe_gr, cotiz, importe_iv, iva_pesos)
            total_con_formato = f" Total IVA VENTAS: {self.suma_iva_pesos:,}"
        


class IVA_ventas:
    def __init__(self, lista_ventas):
        self.lista_ventas = lista_ventas

    def procesar_datos(self):
            resultado_iva_ventas = {}
            clave = self.lista_ventas[0][1]
            valor = float(round(self.lista_ventas[0][4],2))
                       
            resultado_iva_ventas[clave] = valor
            return resultado_iva_ventas


class IVA_compras:
        def __init__(self, lista_compras):
            self.lista_compras = lista_compras
            
        def procesar_datos(self):
            resultado_iva_compras = {}

            for item in self.lista_compras:
                clave = item[1]  # Segundo elemento de la tupla
                valor = float(round(item[4],2))  # Último elemento de la tupla
                resultado_iva_compras[clave] = valor

            return resultado_iva_compras
        
class IVA_retenciones:
        def __init__(self, lista_retenciones):
             self.lista_retenciones = lista_retenciones

        def procesar_datos(self):
                print(self.lista_retenciones, type(self.lista_retenciones))
                resultado_iva_retenciones = {}
                clave = "IVA Retenciones"
                valor = float(round(self.lista_retenciones[0][0],0))
                            
                resultado_iva_retenciones[clave] = valor

                return resultado_iva_retenciones
        



def iva_ventas():
        query_IVA_ventas = Query().query_IVA_ventas()
        results = conexion.fetch_all(query_IVA_ventas)
        datos = IVA_ventas(results)
        lista_formato =  datos.procesar_datos()
                      
        return lista_formato

def iva_compras():
        query_IVA_COMPRAS = Query().query_IVA_compras()
        results = conexion.fetch_all(query_IVA_COMPRAS)
        datos = IVA_compras(results)
        lista_formato =  datos.procesar_datos()
                
        return lista_formato

def total_iva_compras(iva_compras):
    total_iva_compras = 0.0

    for valor in iva_compras.values():
        total_iva_compras += valor

    return total_iva_compras


def iva_retenciones():
        query_IVA_RETENCIONES = Query().query_IVA_retenciones()
        results = conexion.fetch_all(query_IVA_RETENCIONES)
        datos = IVA_retenciones(results)
        lista_formato =  datos.procesar_datos()
                
        return lista_formato

   

if __name__ == '__main__':
    conexion = ConexionSql(Driver=r"{SQL Server}", Server=r"CV-TANGO\SQLEXPRESS", Database=r"CV_CONTROL")
    conexion.connect()

    a = iva_compras()
    b = iva_ventas()
    c = iva_retenciones()

    total_iva_c = total_iva_compras(a)
    total_iva_v = b['21140101 - IVA Debito Fiscal']
    total_iva_r = c['IVA Retenciones']

    posicion = round(total_iva_c + total_iva_v + total_iva_r,2)  
    posicion = f"{posicion:,}" 

    total_iva_c = f"{total_iva_c:,}"
    total_iva_v = f"{total_iva_v:,}"
    total_iva_r = f"{total_iva_r:,}"

    print("IVA Compras: ", total_iva_c)
    print("IVA Ventas: ", total_iva_v)
    print("IVA Retenciones:  ", total_iva_r)
    print("")
    print("---------------------------------")
    print("IVA Posicion: ", posicion)
    

    conexion.close()

    