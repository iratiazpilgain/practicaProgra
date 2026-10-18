import pandas as pd
import matplotlib.pyplot as plt
from analisis import AnalizarClima
from excepciones import ColumnaObligatoriaError, ColumnaInexistenteError


# definimos la clase hijo que hereda de AnalizarClima
class VisualizarClima(AnalizarClima):
    def __init__(self, df):
        super().__init__(df)
        self.sacar_estadisticas()   # ejecutamos esto para que nos de el diccionario de estadísticas


    #  definimos las funciones que dibujan y guardan nuestras gráficas

    def barras_trimestral(self, salida='barras_trimestral.png'): #gráfico de barras con máximos, mínimos y medias trimestrales
        df_trimestral = self.estadisticas['trimestral'].copy() # copiamos el resumen trimestral del diccionario
        df_trimestral['trimestre'] = df_trimestral['trimestre'].astype(str)
        df_trimestral.set_index('trimestre', inplace=True)

        cols = [('actual_max_temp', 'max'), ('actual_mean_temp', 'mean'), ('actual_min_temp', 'min')]  # seleccionamos laa columnas que queremos
        df_barras = df_trimestral[cols]
        df_barras.columns = ['Máx (absoluta)', 'Media', 'Mín (absoluta)']

        fig, ax = plt.subplots(figsize=(10, 5))

        df_barras.plot(kind='bar', ax=ax, color=['red', 'orange', 'blue'])
        ax.set_title('Temperaturas trimestral')
        ax.set_xlabel('Trimestre')
        ax.set_ylabel('Temperatura (°F)')
        ax.grid(True, axis='y')
        ax.legend(title="")
        plt.xticks(rotation=0)  # Para que los trimestres salgan derechos
        plt.tight_layout()
        fig.savefig(salida)
        plt.close(fig)
        print(f'Gráfico de barras trimestral guardado como: {salida}')


    def histograma_lluvias(self, salida='histograma_lluvias.png'):
        df_mensual = self.estadisticas['mensual']
        meses = df_mensual['mes'].astype(str) # extraemos los meses

        fig, ax = plt.subplots(figsize=(10, 5))

        ax.bar(meses, df_mensual[('actual_precipitation', 'sum')], color='lightblue')
        ax.set_title('precipitaciones acumuladas mensuales')
        ax.set_xlabel('Mes')
        ax.set_ylabel('Precipitación total')
        ax.grid(True, axis='y')

        plt.tight_layout()
        fig.savefig(salida)
        plt.close(fig)
        print(f'Gráfico de precipitación mensual guardado como: {salida}')

    def temperaturas_mensuales(self, salida='temperaturas_mensuales.png'):
        df_mensual = self.estadisticas['mensual']
        meses = df_mensual['mes'].astype(str)

        fig, ax = plt.subplots(figsize=(10, 5))

        ax.plot(meses, df_mensual[('actual_max_temp', 'max')], color='red', label='Max (absoluta)')
        ax.plot(meses, df_mensual[('actual_mean_temp', 'mean')], color='orange', label='Media')
        ax.plot(meses, df_mensual[('actual_min_temp', 'min')], color='dodgerblue', label='Min (absoluta)')

        ax.set_title('Evolución de temperaturas mensuales')
        ax.set_xlabel('Mes')
        ax.set_ylabel('Temperatura (°F)')
        ax.grid(True,alpha=0.3)
        ax.legend()

        plt.tight_layout()
        fig.savefig(salida)
        plt.close(fig)
        print(f'Gráfico de temperaturas mensuales guardado como: {salida}')

    def matriz_correlacion(self, salida='matriz_correlacion.png'):
        if 'correlaciones' not in self.estadisticas:
            raise ColumnaObligatoriaError('Falta la columna obligatoria correlaciones')
        df_corr = self.estadisticas['correlaciones']  # cogemos la matriz de correlación del padre

        fig, ax = plt.subplots(figsize=(8, 6))
        fig.colorbar(ax.matshow(df_corr, cmap='coolwarm'))

        ax.set_xticks(range(len(df_corr.columns)))
        ax.set_yticks(range(len(df_corr.columns)))
        ax.set_xticklabels(df_corr.columns, rotation=90, ha='left')
        ax.set_yticklabels(df_corr.index)

        ax.set_title("Matriz de Correlación de Variables Climáticas", pad=20)

        plt.tight_layout()
        fig.savefig(salida)
        plt.close(fig)
        print(f'Mapa de correlación guardado como: {salida}')

    def outliers(self, salida='outliers.png'):
        if 'anomalias' not in self.estadisticas:
            raise ColumnaObligatoriaError('Falta la columna obligatoria anomalias')

        df_anomalias = self.estadisticas['anomalias'].copy()
        df_completo = self.df.copy()

        df_completo['date'] = pd.to_datetime(df_completo['date'])
        df_anomalias['date'] = pd.to_datetime(df_anomalias['date'])

        fig, ax = plt.subplots(figsize=(11, 6))

        ax.plot(df_completo['date'], df_completo['actual_mean_temp'], color='green', label='Temperatura normal')
        ax.scatter(df_anomalias['date'], df_anomalias['actual_mean_temp'], color='red',s=30, zorder=5, label='Valores anómalos')
        ax.set_title('Días anómalos')
        ax.set_xlabel('Fecha')
        ax.set_ylabel('Temperatura media(°F)')
        ax.legend()

        plt.tight_layout()
        fig.savefig(salida)
        plt.close(fig)
        print(f'Gráfico de anomalías destacadas guardado como: {salida}')




    def temperaturas_lineas(self, ruta_csv='dataset_limpio.csv', salida='temperaturas_lineas.png', *col_extra):
        df = self.df.copy()
        col_obligatorias = ['date', 'actual_max_temp', 'actual_mean_temp', 'actual_min_temp']
        columnas_disponibles = list(df.columns)  # columnas disponibles
        for col in col_obligatorias:         # validamos obligatorias con el error personalizado
            if col not in df.columns:
                raise ColumnaObligatoriaError(f'Falta la columna obligatoria {col}')

        for col in col_extra:  # validamos las extrasde *col_extra con el error personalizado
            if col not in df.columns:
                raise ColumnaInexistenteError(f'La columna extra {col} no existe. Columnas disponibles: {list(columnas_disponibles)}')

        df_plot = df.copy()   # no podemos acceder a los datos del diccionario porque necesitamos TODOS los días
        df_plot['date'] = pd.to_datetime(df_plot['date'])
        df_plot = df_plot.sort_values('date')

        fig, ax = plt.subplots(figsize=(12, 6))

        ax.plot(df_plot['date'], df_plot['actual_max_temp'], color='red', label='Máxima diaria', linewidth=1)
        ax.plot(df_plot['date'], df_plot['actual_mean_temp'], color='green', label='Media diaria', linewidth=1)
        ax.plot(df_plot['date'], df_plot['actual_min_temp'], color='blue', label='Mínima diaria', linewidth=1)


        for col in col_extra:    # dibujar las columnas extra
            ax.plot(df_plot['date'], df_plot[col], label=f'Extra {col}', linestyle='--', alpha=0.6)

        ax.set_title('Evolución siaria de temperaturas')
        ax.set_xlabel('Fecha')
        ax.set_ylabel('Temperatura (en ºF)')
        ax.legend(loc='lower left')
        ax.grid(True, linestyle='--', alpha=0.4)

        plt.tight_layout()
        fig.savefig(salida)
        plt.close(fig)
        print(f'Gráfico de temperaturas diarias guardado como: {salida}')



def generar_graficas(self): # para facilitar el main
    print('Generando temperaturas diarias')
    self.temperaturas_lineas(salida='grafico_temperaturas_diarias.png')
    print('Generando gráfico de barras trimestral')
    self.barras_trimestral()
    print('Generando histograma de lluvias')
    self.histograma_lluvias()
    print('Generando temperaturas mensuales')
    self.temperaturas_mensuales()
    print('Generando matriz de correlación')
    self.matriz_correlacion()
    print('Generando gráfico de outliers')
    self.outliers()
