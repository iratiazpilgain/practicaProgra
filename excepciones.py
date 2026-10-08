class ColumnaInexistenteError(Exception):
    #Al acceder a una columna que no existe.
    def __init__(self, columna):
        self.columna = columna
        super().__init__(f"La columna '{self.columna}' a la que se quiere acceder no existe.")

class FiltroSinResultadosError(Exception):
    #Cuando al aplicar una condición la base de datos se queda vacía.
    def __init__(self, condicion):
        self.condicion = condicion
        super().__init__(f"No existe ninguna fila que cumpla la condición:'{self.condicion}'. No hay datos para analizar o visualizar.")

 class GraficoSinDatosError(Exception):
    #Al hacer un gráfico cuando no hay ningun dato en la base de datos.
    def __init__(self, grafico):
        self.grafico = grafico
        super().__init__("No hay datos para visualizar.")

class GuardarResultadoError(Exception):
    #Al guardar los gráficos en la carpeta y que haya algun error como que este mal la ruta.
    def __init__(self, grafico):
        self.grafico = grafico
        super().__init__(f"No se ha podido guardar el gráfico '{self.grafico}' en la carpeta")


class DatasetInvalidoError(Exception):
    def __init__(self, dataset):
        self.dataset = dataset

DatasetInvalidoError: Sugerida en el ejemplo del documento, útil para cuando el CSV no se puede leer correctamente, está vacío o el separador no es el adecuado.
FormatoArchivoError: Para validar que el archivo cargado tiene la extensión correcta (por ejemplo, si por error se intenta cargar un .txt en lugar de un .csv).