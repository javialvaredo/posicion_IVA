from datetime import datetime, timedelta
import calendar

class Mes_actual:

    def fecha_inicio_fecha_fin(self):
        
        # Obtener la fecha actual
        fecha_actual = datetime.now()

        # Obtener el primer día del mes actual
        fecha_inicial = fecha_actual.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        # Calcular el primer día del próximo mes y restar un segundo para obtener el último día del mes actual
        if fecha_actual.month == 12:
            # Si es diciembre, el próximo mes es enero del próximo año
            fecha_final = fecha_actual.replace(year=fecha_actual.year + 1, month=1, day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(seconds=1)
        else:
            # Si no es diciembre, avanzar al próximo mes
            fecha_final = fecha_actual.replace(month=fecha_actual.month + 1, day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(seconds=1)

        # Formatear las fechas en el formato deseado
        fecha_inicial_formateada = fecha_inicial.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
        fecha_final_formateada = fecha_final.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]

        return (fecha_inicial_formateada, fecha_final_formateada)


class Fecha_posicion:

    def fecha_inicio_fecha_fin(self, mes, año):
        self.mes = int(mes)
        self.año = int(año)

    # Obtener el número de días en el mes
        dias_en_mes = calendar.monthrange(self.año, self.mes)
        dias_en_mes = dias_en_mes[1]

        self.mes = str(self.mes)
        if len(self.mes)<2:
            self.mes=f"0{self.mes}"
         
        fecha_inicial = f"{self.año}-{self.mes}-01T00:00:00.000"
        fecha_final = f"{self.año}-{self.mes}-{dias_en_mes}T23:59:59.000"

                               
        # Formatear las fechas en el formato deseado
        #fecha_inicial_formateada = fecha_inicial.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
        #fecha_final_formateada = fecha_final.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
       
        return (fecha_inicial, fecha_final)


class Query:

    def query_IVA_ventas(self, mes, año):
        self.mes = mes
        self.año = año

        mes_actual = Fecha_posicion()
        fechas = mes_actual.fecha_inicio_fecha_fin(self.mes, self.año)
        fecha_inicio = fechas[0]
        fecha_fin = fechas[1]
        
        #fecha_inicio = '2024-07-01T00:00:00.000'
        #fecha_fin = '2024-07-31T23:59:59.000'


        self.query_IV = f"""DECLARE @__Debe_Key_2 nvarchar(4000) = N'D';
            DECLARE @__Haber_Key_3 nvarchar(4000) = N'H';
            DECLARE @__p_0 datetime = '{fecha_inicio}';
            DECLARE @__p_1 datetime = '{fecha_fin}';
            DECLARE @__ToUpper_4 nvarchar(4000) = N'21140101 - IVA DEBITO FISCAL';

            SET DEADLOCK_PRIORITY -8;

            SELECT [a0].[ID_CUENTA], [a0].[COD_DESC_CUENTA] AS N'Cuenta', COALESCE(SUM(CASE
                WHEN [a].[D_H] = @__Debe_Key_2 THEN [a].[IMPORTE_RENGLON_BASE_GV]
                ELSE 0.0
            END), 0.0) AS N'Debe (CTE)', COALESCE(SUM(CASE
                WHEN [a].[D_H] = @__Haber_Key_3 THEN [a].[IMPORTE_RENGLON_BASE_GV]
                ELSE 0.0
            END), 0.0) AS N'Haber (CTE)', COALESCE(SUM(CASE
                WHEN [a].[D_H] = @__Debe_Key_2 THEN [a].[IMPORTE_RENGLON_BASE_GV]
                ELSE -[a].[IMPORTE_RENGLON_BASE_GV]
            END), 0.0) AS N'Saldo (CTE)'

            FROM [AXV_LIVE_ASIENTO_COMPROBANTE_GV] AS [a]
            INNER JOIN [AXV_CUENTA] AS [a0] ON [a].[ID_CUENTA] = [a0].[ID_CUENTA]
            LEFT JOIN [GVA14] AS [g] ON [a].[ID_GVA14] = [g].[ID_GVA14]
            WHERE ([a].[FECHA_EMIS] IS NOT NULL AND (CONVERT(date, [a].[FECHA_EMIS]) >= @__p_0)) AND (CONVERT(date, [a].[FECHA_EMIS]) <= @__p_1)
            GROUP BY [a0].[ID_CUENTA], [a0].[COD_DESC_CUENTA]
            HAVING [a0].[COD_DESC_CUENTA] IS NOT NULL AND (UPPER([a0].[COD_DESC_CUENTA]) = @__ToUpper_4)"""
        
        return self.query_IV
    
    def query_IVA_compras(self, mes, año):
        self.mes = mes
        self.año = año
        mes_actual = Fecha_posicion()
        fechas = mes_actual.fecha_inicio_fecha_fin(self.mes, self.año)
        fecha_inicio = fechas[0]
        fecha_fin = fechas[1]
      
        #fecha_inicio = '2024-07-01T00:00:00.000'
        #fecha_fin = '2024-07-31T00:00:00.000'

        self.query_IC = f"""DECLARE @__Debe_Key_4 nvarchar(4000) = N'D';
        DECLARE @__Haber_Key_5 nvarchar(4000) = N'H';
        DECLARE @__doJoin_1 int = 0;
        DECLARE @__p_2 datetime = '{fecha_inicio}';
        DECLARE @__p_3 datetime = '{fecha_fin}';
        DECLARE @__ToUpper_6 nvarchar(4000) = N'11320301 - IVA CREDITO FISCAL';
        DECLARE @__ToUpper_7 nvarchar(4000) = N'11320302 - IVA PERCEPCION ANA';
        DECLARE @__ToUpper_8 nvarchar(4000) = N'11320307 - IVA PERCEPCION 3 %';

        SET DEADLOCK_PRIORITY -8;

        SELECT [a0].[ID_CUENTA], [a0].[COD_DESC_CUENTA] AS N'Cuenta', COALESCE(SUM(CASE
            WHEN [a].[D_H] = @__Debe_Key_4 THEN [a].[IMPORTE_RENGLON_BASE_CP]
            ELSE 0.0
        END), 0.0) AS N'Debe (CTE)', COALESCE(SUM(CASE
            WHEN [a].[D_H] = @__Haber_Key_5 THEN [a].[IMPORTE_RENGLON_BASE_CP]
            ELSE 0.0
        END), 0.0) AS N'Haber (CTE)', COALESCE(SUM(CASE
            WHEN [a].[D_H] = @__Debe_Key_4 THEN [a].[IMPORTE_RENGLON_BASE_CP]
            ELSE -[a].[IMPORTE_RENGLON_BASE_CP]
        END), 0.0) AS N'Saldo (CTE)'

        FROM [AXV_LIVE_ASIENTO_COMPROBANTE_CP] AS [a]
        INNER JOIN [AXV_CUENTA] AS [a0] ON [a].[ID_CUENTA] = [a0].[ID_CUENTA]
        LEFT JOIN [CPA01] AS [c] ON [a].[ID_CPA01] = [c].[ID_CPA01]
        LEFT JOIN [dbo].[ClasificadorCPA01](@__doJoin_1) AS [c0] ON [c].[ID_CPA01] = [c0].[ID_CPA01]
        WHERE (CONVERT(date, [a].[FECHA_CONT]) >= @__p_2) AND (CONVERT(date, [a].[FECHA_CONT]) <= @__p_3)
        GROUP BY [a0].[ID_CUENTA], [a0].[COD_DESC_CUENTA]
        HAVING (([a0].[COD_DESC_CUENTA] IS NOT NULL AND (UPPER([a0].[COD_DESC_CUENTA]) = @__ToUpper_6)) OR ([a0].[COD_DESC_CUENTA] IS NOT NULL AND (UPPER([a0].[COD_DESC_CUENTA]) = @__ToUpper_7))) OR ([a0].[COD_DESC_CUENTA] IS NOT NULL AND (UPPER([a0].[COD_DESC_CUENTA]) = @__ToUpper_8))"""
        print(self.query_IC)
        return self.query_IC
    
    
    def query_IVA_retenciones(self, mes, año):
        self.mes = mes
        self.año = año

        self.mes = mes
        self.año = año
        mes_actual = Fecha_posicion()
        fechas = mes_actual.fecha_inicio_fecha_fin(self.mes, self.año)
        fecha_inicio = fechas[0]
        fecha_fin = fechas[1]

        
        #fecha_inicio = '2024-07-01T00:00:00.000'
        #fecha_fin = '2024-07-31T00:00:00.000'


        self.query_Ret = f"""SELECT 
                                    SUM(MONTO) AS TOTAL_MONTO
                                FROM 
                                    SBA05 
                                WHERE 
                                    COD_CTA = '31' 
                                    AND FECHA >= '{fecha_inicio}' 
                                    AND FECHA <= '{fecha_fin}';"""
        
        return self.query_Ret
    

    query_IVv = f"""SELECT FECHA_EMIS, T_COMP, N_COMP, IMPORTE_GR, COTIZ, IMPORTE_IV
            FROM GVA12
            WHERE IMPORTE_IV <> 0 AND FECHA_EMIS > '2024-06-01'AND FECHA_EMIS <= '2024-06-30';
            """


if __name__ == '__main__':


   """obj = Query()
   query = obj.query_IVA_ventas()
   print(query)"""

   año = 2024
   mes = 7

   dias = Fecha_posicion()
   dias.fecha_inicio_fecha_fin(2024,7)
   
   print(dias)

   

   
    
        

    