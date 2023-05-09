from typing import Tuple


class DatosMeteorologicos:
    def _init_(self, nombre_archivo: str):
        self.nombre_archivo = nombre_archivo

    def procesar_datos(self) -> Tuple[float, float, float, float, str]:
        temperatura_suma = 0
        humedad_suma = 0
        presion_suma = 0
        velocidad_viento_suma = 0
        direccion_viento_suma = 0
        n_registros = 0
        direcciones_viento = {"N": 0, "NNE": 22.5, "NE": 45, "ENE": 67.5, "E": 90, "ESE": 112.5, "SE": 135,
                              "SSE": 157.5, "S": 180, "SSW": 202.5, "SW": 225, "WSW": 247.5, "W": 270, "WNW": 292.5,
                              "NW": 315, "NNW": 337.5}
        conteo_direcciones_viento = {direccion: 0 for direccion in direcciones_viento}

        with open(self.nombre_archivo) as f:
            for linea in f:
                linea = linea.strip()
                if linea.startswith("Temperatura:"):
                    temperatura_suma += float(linea.split(":")[1])
                elif linea.startswith("Humedad:"):
                    humedad_suma += float(linea.split(":")[1])
                elif linea.startswith("Presión:"):
                    presion_suma += float(linea.split(":")[1])
                elif linea.startswith("Viento:"):
                    viento = linea.split(":")[1].split(",")
                    velocidad_viento_suma += float(viento[0])
                    direccion_viento_suma += direcciones_viento[viento[1]]
                    conteo_direcciones_viento[viento[1]] += 1
                elif linea.startswith("Estación:"):
                    n_registros += 1

        temperatura_promedio = temperatura_suma / n_registros
        humedad_promedio = humedad_suma / n_registros
        presion_promedio = presion_suma / n_registros
        velocidad_viento_promedio = velocidad_viento_suma / n_registros
        direccion_viento_promedio = direccion_viento_suma / n_registros

        direccion_predominante = max(conteo_direcciones_viento, key=conteo_direcciones_viento.get)

        for direccion, grados in direcciones_viento.items():
            if abs(grados - direccion_viento_promedio) < 11.25:
                direccion_viento_promedio = direccion
                break

        return (
        temperatura_promedio, humedad_promedio, presion_promedio, velocidad_viento_promedio, direccion_predominante)