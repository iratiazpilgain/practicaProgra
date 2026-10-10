import os
import pandas as pd

class DatasetInvalidoError(Exception):
    # Excepción personalizada para errores en el formato o contenido de un dataset.
    pass

class CargadorDatos:

    def __init__(self, ruta, separador=","):
        self.ruta = ruta
        self._separador = separador

    @property
    def ruta(self):
        return self._ruta

    @ruta.setter
    def ruta(self, nueva):
        if not isinstance(nueva, str) or not nueva.strip():
            raise ValueError("La ruta debe ser un texto no vacío")

        self._ruta = nueva

    def cargar(self):

        if not os.path.isfile(self._ruta):
            raise FileNotFoundError(f"No existe el fichero: {self._ruta}")

        try:
            df = pd.read_csv(self._ruta, sep=self._separador, encoding="utf-8")

        except UnicodeDecodeError:
            try:
                df = pd.read_csv(self._ruta, sep=self._separador, encoding="latin-1")

            except (pd.errors.EmptyDataError, pd.errors.ParserError) as e:
                raise DatasetInvalidoError(f"No se ha podido leer el CSV: {e}") from e

        except pd.errors.EmptyDataError as e:
            raise DatasetInvalidoError("El fichero CSV está vacío.") from e

        except pd.errors.ParserError as e:
            raise DatasetInvalidoError(f"El CSV está mal formado: {e}") from e

        self.validar(df)

        print(f"CSV cargado: {df.shape[0]} filas y {df.shape[1]} columnas.")

        return df

    def validar(self, df):

        if df.empty:
            raise DatasetInvalidoError("El CSV no contiene filas.")

        if df.shape[1] < 2:
            raise DatasetInvalidoError("Hay menos de dos columnas, comprueba el separador.")

        if df.isna().all().all():
            raise DatasetInvalidoError("Todas las celdas están vacías.")