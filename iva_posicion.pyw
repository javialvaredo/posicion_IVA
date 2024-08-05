import pyodbc
from decimal import Decimal
from datetime import datetime
import locale
from query import Query
import tkinter as tk
from tkinter import ttk, messagebox, font


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


class Mes_actual:

    def __init__(self):
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        fecha_actual = datetime.now()
        # Obtener el nombre del mes y el año actual
        self.mes_actual = fecha_actual.strftime("%B")
        self.año_actual = fecha_actual.year



class IVA_ventas:
    def __init__(self, lista_ventas):
        self.lista_ventas = lista_ventas

    def procesar_datos(self):
        resultado_iva_ventas = {}
        clave = self.lista_ventas[0][1]
        valor = float(round(self.lista_ventas[0][4], 2))
        resultado_iva_ventas[clave] = valor
        return resultado_iva_ventas


class IVA_compras:
    def __init__(self, lista_compras):
        self.lista_compras = lista_compras

    def procesar_datos(self):
        resultado_iva_compras = {}
        for item in self.lista_compras:
            clave = item[1]
            valor = float(round(item[4], 2))
            resultado_iva_compras[clave] = valor
        return resultado_iva_compras


class IVA_retenciones:
    def __init__(self, lista_retenciones):
        self.lista_retenciones = lista_retenciones

    def procesar_datos(self):
        print(self.lista_retenciones, type(self.lista_retenciones))
        resultado_iva_retenciones = {}
        clave = "IVA Retenciones"
        valor = float(round(self.lista_retenciones[0][0], 0))
        resultado_iva_retenciones[clave] = valor
        return resultado_iva_retenciones


def iva_ventas(conexion):
    query_IVA_ventas = Query().query_IVA_ventas()
    results = conexion.fetch_all(query_IVA_ventas)
    datos = IVA_ventas(results)
    lista_formato = datos.procesar_datos()
    return lista_formato


def iva_compras(conexion):
    query_IVA_COMPRAS = Query().query_IVA_compras()
    results = conexion.fetch_all(query_IVA_COMPRAS)
    datos = IVA_compras(results)
    lista_formato = datos.procesar_datos()
    return lista_formato


def total_iva_compras(iva_compras):
    total_iva_compras = 0.0
    for valor in iva_compras.values():
        total_iva_compras += valor
    return total_iva_compras


def iva_retenciones(conexion):
    query_IVA_RETENCIONES = Query().query_IVA_retenciones()
    results = conexion.fetch_all(query_IVA_RETENCIONES)
    datos = IVA_retenciones(results)
    lista_formato = datos.procesar_datos()
    return lista_formato


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Reporte de IVA")
        self.geometry("600x400")

        self.conexion = ConexionSql(Driver=r"{SQL Server}", Server=r"CV-TANGO\SQLEXPRESS", Database=r"CV_CONTROL")
        self.conexion.connect()

        self.create_widgets()

    def create_widgets(self):
        self.label_compras = tk.Label(self, text="IVA Ventas:")
        self.label_compras.grid(row=0, column=0, padx=10, pady=10)
        self.result_compras = tk.Label(self, text="")
        self.result_compras.grid(row=0, column=1, padx=10, pady=10)

        self.label_ventas = tk.Label(self, text="IVA Compras:")
        self.label_ventas.grid(row=1, column=0, padx=10, pady=10)
        self.result_ventas = tk.Label(self, text="")
        self.result_ventas.grid(row=1, column=1, padx=10, pady=10)

        self.label_retenciones = tk.Label(self, text="IVA Retenciones:")
        self.label_retenciones.grid(row=2, column=0, padx=10, pady=10)
        self.result_retenciones = tk.Label(self, text="")
        self.result_retenciones.grid(row=2, column=1, padx=10, pady=10)
        mes_actual= Mes_actual()
        mesYaño = f"{mes_actual.mes_actual}-{mes_actual.año_actual}"

        self.label_posicion = tk.Label(self, text=f"IVA Posicion mes: {mesYaño}")
        self.label_posicion.grid(row=3, column=0, padx=10, pady=10)
        self.result_posicion = tk.Label(self, text="")
        self.result_posicion.grid(row=3, column=1, padx=10, pady=10)

        self.result_saldo = tk.Label(self, text="")
        self.result_saldo.grid(row=3, column=2, padx=10, pady=10)



        self.calculate_button = tk.Button(self, text="Calcular Posicion:", command=self.calculate_iva)
        self.calculate_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def calculate_iva(self):
        a = iva_compras(self.conexion)
        b = iva_ventas(self.conexion)
        c = iva_retenciones(self.conexion)

        total_iva_c = total_iva_compras(a)
        total_iva_v = b['21140101 - IVA Debito Fiscal']
        total_iva_r = c['IVA Retenciones']

        posicion = round(total_iva_c + total_iva_v + total_iva_r, 2)
        posicion_str = f"{posicion:,}"
        saldo = self.como_da(posicion)

        self.result_compras.config(text=f"{total_iva_v:,}")
        self.result_ventas.config(text=f"{total_iva_c:,}")
        self.result_retenciones.config(text=f"{total_iva_r:,}")
        self.result_posicion.config(text=posicion_str, font=font.Font(weight='bold'))
        self.result_saldo.config(text=saldo) 


    def como_da(self, posicion):
        saldo = ""
        if posicion > 0:
            resultado = "A Favor"
        else:
            resultado = "A Pagar"
        return resultado


    def on_closing(self):
        self.conexion.close()
        self.destroy()


if __name__ == '__main__':
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
