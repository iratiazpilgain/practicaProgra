from carga import CargadorDatos
from limpieza import Limpiador
# from excepciones import DatasetInvalidoError, ColumnaInexistenteError

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

        print("\n----- Exportando los resultados -----")
        ruta_salida = limpiador.exportar(ruta="grupo07_clima_phoenix_limpio.csv")

        print(f"\n¡Proceso finalizado con éxito!")
        print(f"Filas originales: {df_original.shape[0]} | Filas finales: {df_limpio.shape[0]}")


    except FileNotFoundError as e:
        print(f"\n[Error de archivo]: {e}")
    #
    # except DatasetInvalidoError as e:
    #     print(f"\n[Error en el Dataset]: {e}")
    #
    # except Exception as e:
    #     print(f"\n[Error inesperado]: {e}")