from carga import CargadorDatos
from limpieza import Limpiador
from analisis import AnalizarClima
from visualizacion import VisualizarClima
from excepciones import DatasetInvalidoError
from excepciones import ColumnaInexistenteError
from excepciones import ColumnaObligatoriaError


if __name__ == "__main__":
    # 1. Definir la ruta del archivo y tipos de datos a convertir (opcional)
    ruta_archivo = "grupo07_clima_phoenix.csv"

    # Diccionario opcional para conversión explícita de tipos
    tipos_columnas = {"date": "fecha",}

    try:
        print("----- Carga de datos -----")
        # Instanciar y cargar el CSV
        cargador = CargadorDatos(ruta=ruta_archivo, separador=",")
        df_original = cargador.cargar()

        print("\n----- Proceso de limpieza -----")
        limpiador = Limpiador(df_original)

        df_limpio = limpiador.limpiar(estrategia="mediana", tipos=tipos_columnas)
        print(f"Filas originales: {df_original.shape[0]} | Filas finales: {df_limpio.shape[0]}")


        print("\n----- Exportando los resultados -----")
        ruta_salida = limpiador.exportar(ruta="grupo07_clima_phoenix_limpio.csv")

        print(f"\n----- Análisis y Estadísticas -----")
        analizador = AnalizarClima(df_limpio)

        estadisticas_totales = analizador.sacar_estadisticas()

        print(f"\n¡Análisis completado con éxito!")
        print(f"\nSe han generado las siguientes claves estadísticas: {list(estadisticas_totales.keys())}")


        print(f"\n¡Proceso global finalizado con éxito!")
        print(f"Filas originales: {df_original.shape[0]} | Filas finales: {df_limpio.shape[0]}")

        print(f'\n----- Generación de Visualizaciones -----')
        visualizador = VisualizarClima(df_limpio)
        visualizador.generar_graficas()




    except FileNotFoundError as e:
        print(f"\n[Error de archivo]: {e}")
    except DatasetInvalidoError as e:
        print(f"\n[Error en el Dataset]: {e}")
    except ColumnaInexistenteError as e:
        print(f"\n[Error de columna]: {e}")
    except ColumnaObligatoriaError as e:
        print(f"\n[Error de columna obligatoria]: {e}")
    except Exception as e:
        print(f"\n[Error inesperado]: {e}")
    else:
        print(f"\n¡Proceso global finalizado con éxito!")
