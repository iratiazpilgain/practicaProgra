import pandas as pd


class Limpiador():
    def __init__(self, df):
        self._df = df.copy()
        self._informe = {}

    @property
    def df(self):
        return self._df

    @property
    def informe(self):
        return dict(self._informe)

    def normalizar_texto(self, texto, minusculas=False):
        #Elimina espacios sobrantes y normaliza un valor de texto.
        if pd.isna(texto):
            return texto

        texto = " ".join(str(texto).split())

        if minusculas:
            texto = texto.lower()

        return texto

    def normalizar_columnas(self, minusculas=True):
        # Estandariza los nombres de las columnas.
        nuevas_columnas = []

        for col in self._df.columns:
            columna = self.normalizar_texto(col, minusculas=minusculas)
            columna = columna.replace(" ", "_")
            nuevas_columnas.append(columna)

        self._df.columns = nuevas_columnas
        self._informe["columnas_normalizadas"] = True

        return self

    def eliminar_duplicados(self):
        # Elimina filas exactamente iguales.
        filas_antes = len(self._df)

        self._df = self._df.drop_duplicates().reset_index(drop=True)

        filas_despues = len(self._df)
        duplicados = filas_antes - filas_despues

        self._informe["duplicados_eliminados"] = duplicados
        return self

    def limpiar_texto(self, minusculas=False):
        # Limpia cadenas de texto en columnas tipo object/string.
        columnas_texto = self._df.select_dtypes(include=["object", "string"]).columns

        for col in columnas_texto:
            # Aplicamos la función normalizar_texto directamente a cada elemento
            self._df[col] = self._df[col].apply(lambda val: self.normalizar_texto(val, minusculas=minusculas))
            # Convertimos cadenas vacías en NaN/NA
            self._df[col] = self._df[col].replace("", pd.NA)

        self._informe["columnas_texto_limpiadas"] = list(columnas_texto)
        return self


    def convertir_tipos(self, tipos):

        for col in tipos:
            tipo = tipos[col]

            if col not in self.df.columns:
                raise ValueError(f"La columna '{col}' no existe")

            if tipo == "fecha":
                self.df[col] = pd.to_datetime(self.df[col],errors="coerce")

            elif tipo == "int":
                self.df[col] = pd.to_numeric(self.df[col],errors="coerce").astype("Int64")

            elif tipo == "float":
                self.df[col] = pd.to_numeric(self.df[col],errors="coerce")

            else:
                self.df[col] = self.df[col].astype(tipo)

        self._informe["tipos_convertidos"] = tipos
        return self

    def tratar_nulos(self, estrategia="mediana",umbral_columna=0.6,texto_defecto="desconocido"):
        # Elimina columnas con demasiados nulos e imputa los valores faltantes restantes
        estrategias_validas = ["mediana", "media", "cero", "eliminar"]

        if estrategia not in estrategias_validas:
            raise ValueError(f"Estrategia no válida: {estrategia}. Opciones: {sorted(estrategias_validas)}")

        nulos_antes = int(self._df.isna().sum().sum())

        # 1. Eliminar columnas con porcentaje de nulos superior al umbral
        proporcion_nulos = self._df.isna().mean()
        columnas_eliminar = [col for col in self._df.columns if proporcion_nulos[col] > umbral_columna]

        if columnas_eliminar:
            self._df = self._df.drop(columns=columnas_eliminar)

        self._informe["columnas_eliminadas"] = columnas_eliminar

        # 2. Tratar nulos restantes
        if estrategia == "eliminar":
            self._df = self._df.dropna().reset_index(drop=True)
        else:
            # Columnas numéricas
            columnas_numericas = self._df.select_dtypes(include="number").columns
            for col in columnas_numericas:
                if estrategia == "mediana":
                    valor = self._df[col].median()
                elif estrategia == "media":
                    valor = self._df[col].mean()
                elif estrategia == "cero":
                    valor = 0

                self._df[col] = self._df[col].fillna(valor)

            # Columnas de texto / no numéricas
            columnas_texto = self._df.select_dtypes(exclude="number").columns
            for col in columnas_texto:
                if not pd.api.types.is_datetime64_any_dtype(self._df[col]):
                    self._df[col] = self._df[col].fillna(texto_defecto)

        nulos_despues = int(self._df.isna().sum().sum())
        nulos_tratados = nulos_antes - nulos_despues

        self._informe["nulos_tratados"] = int(nulos_tratados)
        return self

    def limpiar(self, estrategia="mediana", tipos=None):
        # Ejecuta el pipeline completo de limpieza.
        self.normalizar_columnas()
        self.limpiar_texto()
        self.eliminar_duplicados()

        if tipos is not None:
            self.convertir_tipos(tipos)

        self.tratar_nulos(estrategia=estrategia)

        print("Limpieza terminada con éxito.")
        print(self.informe)

        return self._df


    def exportar(self, ruta="resultados/dataset_limpio.csv"):

        self.df.to_csv(ruta,index=False)
        print(f"Dataset exportado en: {ruta}")

        return ruta
