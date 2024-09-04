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

"""
class Mes_actual:

    def __init__(self):
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        fecha_actual = datetime.now()
        # Obtener el nombre del mes y el año actual
        self.mes_actual = fecha_actual.strftime("%B")
        self.año_actual = fecha_actual.year


class Mes_actual:

    def __init__(self):
        fecha_actual = datetime.now()
        # Obtener el mes y el año en formato numérico
        self.mes_actual = fecha_actual.strftime("%m")  # Month in MM format
        self.año_actual = fecha_actual.strftime("%y")  # Year in YY format
"""


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
        resultado_iva_retenciones = {}
        clave = "IVA Retenciones"
        valor = float(round(self.lista_retenciones[0][0], 0))
        resultado_iva_retenciones[clave] = valor
        return resultado_iva_retenciones


def iva_ventas(conexion, mes, año):
    query_IVA_ventas = Query().query_IVA_ventas(mes, año)
    results = conexion.fetch_all(query_IVA_ventas)
    datos = IVA_ventas(results)
    lista_formato = datos.procesar_datos()
    return lista_formato


def iva_compras(conexion, mes, año):
    query_IVA_COMPRAS = Query().query_IVA_compras(mes, año)
    results = conexion.fetch_all(query_IVA_COMPRAS)
    datos = IVA_compras(results)
    lista_formato = datos.procesar_datos()
    return lista_formato


def total_iva_compras(iva_compras):
    total_iva_compras = 0.0
    for valor in iva_compras.values():
        total_iva_compras += valor
    return total_iva_compras


def iva_retenciones(conexion, mes, año):
    query_IVA_RETENCIONES = Query().query_IVA_retenciones(mes, año)
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
        self.label_compras = tk.Label(self, text="Ventas:")
        self.label_compras.grid(row=2, column=0, padx=10, pady=10)
        self.result_compras = tk.Label(self, text="")
        self.result_compras.grid(row=2, column=1, padx=10, pady=10)

        self.label_ventas = tk.Label(self, text="Compras:")
        self.label_ventas.grid(row=3, column=0, padx=10, pady=10)
        self.result_ventas = tk.Label(self, text="")
        self.result_ventas.grid(row=3, column=1, padx=10, pady=10)

        self.label_retenciones = tk.Label(self, text="Retenciones:")
        self.label_retenciones.grid(row=4, column=0, padx=10, pady=10)
        self.result_retenciones = tk.Label(self, text="")
        self.result_retenciones.grid(row=4, column=1, padx=10, pady=10)

        # Mes and Año labels and entries in the same row
        self.label_mes = tk.Label(self, text="Mes:")
        self.label_mes.grid(row=0, column=0, padx=5, pady=5, sticky="e")  # Align to the right

        self.entry_mes = tk.Entry(self, width=5)
        self.entry_mes.grid(row=0, column=1, padx=5, pady=5, sticky="w")  # Align to the left

        self.label_año = tk.Label(self, text="Año:")
        self.label_año.grid(row=1, column=0, padx=5, pady=5, sticky="e")  # Align to the right

        self.entry_año = tk.Entry(self, width=5)
        self.entry_año.grid(row=1, column=1, padx=5, pady=5, sticky="w")  # Align to the left

        self.label_posicion = tk.Label(self, text="IVA Posición:")
        self.label_posicion.grid(row=5, column=0, padx=10, pady=10)
        self.result_posicion = tk.Label(self, text="")
        self.result_posicion.grid(row=5, column=1, padx=10, pady=10)

        self.result_saldo = tk.Label(self, text="")
        self.result_saldo.grid(row=5, column=2, padx=10, pady=10)

        self.calculate_button = tk.Button(self, text="Calcular Posición:", command=self.calculate_iva)
        self.calculate_button.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

    def calculate_iva(self):
        # Get manual input for month and year
        self.mes = self.entry_mes.get().strip()
        self.año = self.entry_año.get().strip()

        if not self.mes or not self.año:  # Use current month and year if no input
            mes_actual = Mes_actual()
            self.mes = mes_actual.mes_actual
            self.año = mes_actual.año_actual

        # Proceed with the calculation using the specified month and year
        a = iva_compras(self.conexion, self.mes, self.año)
        b = iva_ventas(self.conexion, self.mes, self.año)
        c = iva_retenciones(self.conexion, self.mes, self.año)

        total_iva_c = round(total_iva_compras(a), 2)
        total_iva_v = b['21140101 - IVA Debito Fiscal']
        total_iva_r = c['IVA Retenciones']

        posicion = round(total_iva_c + total_iva_v + total_iva_r, 2)
        posicion_str = f"{posicion:,}"
        saldo = self.como_da(posicion)
        fuente_negrita = font.Font(weight='bold', size=10)

        self.result_compras.config(text=f"{total_iva_v:,}")
        self.result_ventas.config(text=f"{total_iva_c:,}")
        self.result_retenciones.config(text=f"{total_iva_r:,}")
        self.result_posicion.config(text=f"{self.mes}/{self.año}: {posicion_str}", font=fuente_negrita)
        self.result_saldo.config(text=saldo, font=fuente_negrita )

    def como_da(self, posicion):
        if posicion > 0:
            return "a Favor"
        else:
            return "a Pagar"

    def on_closing(self):
        self.conexion.close()
        self.destroy()

if __name__ == '__main__':
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
