import pandas as pd

class AnalizarClima:

    def __init__(self, df):
        self._df = df.copy()

        #if not pd.api.types.is_datetime64_any_dtype(self._df['date']):
            #self._df['date'] = pd.to_datetime(self._df['date'])

        if self._df['date'].dtype != 'datetime64[ns]':
            self._df['date'] = pd.to_datetime(self._df['date'])

        self._estadisticas = {}

    @property
    def df(self):
        return self._df

    @property
    def estadisticas(self):
        return dict(self._estadisticas)


    def resumen_columnas(self, *args):
        if not args:
            columnas = ['actual_mean_temp', 'actual_max_temp', 'actual_precipitation']
        else:
            columnas = list(args)

        resumen = self._df[columnas].describe()

        self._estadisticas['resumen_personalizado'] = resumen
        return resumen


    def mensual(self):
        df_temp = self._df.assign(mes=self._df['date'].dt.to_period('M'))

        resumen_mensual = df_temp.groupby('mes').agg({
            'actual_mean_temp': 'mean',
            'actual_max_temp': 'max',
            'actual_min_temp': 'min',
            'actual_precipitation': ['min', 'max', 'sum']
        }).reset_index()

        self._estadisticas['mensual'] = resumen_mensual
        return resumen_mensual


    def trimestral(self):
        df_temp = self._df.assign(trimestre=self._df['date'].dt.to_period('Q'))

        resumen_trimestral = df_temp.groupby('trimestre').agg({
            'actual_mean_temp': 'mean',
            'actual_max_temp': 'max',
            'actual_min_temp': 'min',
            'actual_precipitation': ['min', 'max', 'sum']
        }).reset_index()

        self._estadisticas['trimestral'] = resumen_trimestral
        return resumen_trimestral


    def records(self, n=5):
        top_calor = self._df.nlargest(n, 'actual_max_temp')[['date', 'actual_max_temp', 'actual_min_temp', 'actual_precipitation']]
        top_frio = self._df.nsmallest(n, 'actual_min_temp')[['date', 'actual_max_temp', 'actual_min_temp', 'actual_precipitation']]

        resultado_records = {
            'dias_mas_calurosos': top_calor,
            'dias_mas_frios': top_frio
        }

        self._estadisticas['records'] = resultado_records

        return resultado_records


    def amplitud_termica(self, n=5):
        df_temp = self._df.copy()

        df_temp['amplitud_termica'] = df_temp['actual_max_temp'] - df_temp['actual_min_temp']

        mayor_amplitud = df_temp.nlargest(n, 'amplitud_termica')[
            ['date', 'actual_max_temp', 'actual_min_temp', 'amplitud_termica', 'actual_precipitation']
        ]

        self._estadisticas['amplitud_termica'] = mayor_amplitud

        return mayor_amplitud

    def desviacion_historica(self):
        df_temp = self._df.copy()

        df_temp['average_mean_temp'] = (df_temp['average_max_temp'] + df_temp['average_min_temp']) / 2

        df_temp['desviacion_media'] = df_temp['actual_mean_temp'] - df_temp['average_mean_temp']

        df_temp['mes'] = df_temp['date'].dt.to_period('M')
        resumen_desv = df_temp.groupby('mes')['desviacion_media'].mean().reset_index()

        self._estadisticas['desviacion_historica'] = resumen_desv
        return resumen_desv


    def correlaciones(self, **kwargs):
        df_num = self._df.drop(columns=['date'], errors='ignore')

        df_num = df_num.select_dtypes(include=['number'])

        matriz_corr = df_num.corr(**kwargs)
        self._estadisticas['correlaciones'] = matriz_corr

        return matriz_corr


    def deteccion_anomalias(self, umbral=2.0):
        df_temp = self._df.copy()

        media = df_temp['actual_mean_temp'].mean()
        desv_std = df_temp['actual_mean_temp'].std()

        df_temp['z_score'] = (df_temp['actual_mean_temp'] - media) / desv_std
        anomalias = df_temp[abs(df_temp['z_score']) > umbral][['date', 'actual_mean_temp', 'actual_max_temp', 'actual_min_temp', 'actual_precipitation', 'z_score']]

        self._estadisticas['anomalias'] = anomalias

        return anomalias

    def sacar_estadisticas(self):
        self.resumen_columnas()
        self.mensual()
        self.trimestral()
        self.records()
        self.amplitud_termica()
        self.desviacion_historica()
        self.correlaciones()
        self.deteccion_anomalias()

        return self._estadisticas