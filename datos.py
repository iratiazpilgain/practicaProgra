import pandas as pd
import numpy as np

class CargadorDatos:
    def __init__(self, ruta, separador=",", codificacion="utf-8"):
        self._ruta = ruta
        self._separador = separador
        self._codificacion = codificacion

    @property
    def ruta(self):
        return self._ruta

    def cargar(self):
        """Lee y valida el CSV. Devuelve un DataFrame."""
        if not os.path.isfile(self._ruta):
            raise FileNotFoundError(f"No existe el fichero: {self._ruta}")
        try:
            df = pd.read_csv(self._ruta, sep=self._separador,
                             encoding=self._codificacion)
        except (pd.errors.EmptyDataError, pd.errors.ParserError,
                UnicodeDecodeError) as e:
            raise DatasetInvalidoError(f"CSV ilegible: {e}") from e
        self._validar(df)
        return df

    @staticmethod
    def _validar(df):
        if df.empty:
            raise DatasetInvalidoError("El CSV no contiene filas.")
        if df.shape[1] < 2:
            raise DatasetInvalidoError(
                "El CSV tiene menos de 2 columnas (¿separador incorrecto?).")


class CargadorDatos(object):
    def __init__(self, nombre):
        self.nombre = nombre