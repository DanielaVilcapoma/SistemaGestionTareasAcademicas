import json
import os
from datetime import datetime

ARCHIVO_DATOS = "tareas_academicas.json"


class Tarea:
    def __init__(self, titulo, descripcion, fecha, estado="pendiente"):
        self.titulo = titulo.strip()
        self.descripcion = descripcion.strip()
        self.fecha = fecha.strip()
        self.estado = estado.strip().lower()

    def to_dict(self):
        return {
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "fecha": self.fecha,
            "estado": self.estado
        }

    @staticmethod
    def from_dict(datos):
        return Tarea(
            datos.get("titulo", ""),
            datos.get("descripcion", ""),
            datos.get("fecha", ""),
            datos.get("estado", "pendiente")
        )


class GestorTareas:
    def __init__(self, archivo=ARCHIVO_DATOS):
        self.archivo = archivo
        self.tareas = self.cargar_tareas()

    def validar_texto(self, valor, campo):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError(f"El campo '{campo}' no puede estar vacío.")
        return valor.strip()

    def validar_fecha(self, fecha):
        self.validar_texto(fecha, "fecha")
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            raise ValueError("La fecha debe tener el formato AAAA-MM-DD.")
        return fecha

    def validar_estado(self, estado):
        estado = self.validar_texto(estado, "estado").lower()
        estados_validos = ["pendiente", "en proceso", "completada"]

        if estado not in estados_validos:
            raise ValueError(
                "Estado inválido. Usa: pendiente, en proceso o completada."
            )

        return estado

    def agregar_tarea(self, titulo, descripcion, fecha):
        titulo = self.validar_texto(titulo, "titulo").title()
        descripcion = self.validar_texto(descripcion, "descripcion")
        fecha = self.validar_fecha(fecha)

        nueva = Tarea(titulo, descripcion, fecha)

        self.tareas.append(nueva)
        self.guardar_tareas()

        return "Tarea agregada correctamente."

    def listar_tareas(self):
        if not self.tareas:
            return "No hay tareas registradas."

        salida = []

        for i, tarea in enumerate(self.tareas, 1):
            salida.append(
                f"{i}. [{tarea.estado}] {tarea.titulo} | "
                f"{tarea.descripcion} | Fecha: {tarea.fecha}"
            )

        return "\n".join(salida)

    def buscar_tareas(self, palabra):
        palabra = self.validar_texto(
            palabra,
            "palabra clave"
        ).lower()

        resultados = []

        for i, tarea in enumerate(self.tareas, 1):
            texto = (
                f"{tarea.titulo} "
                f"{tarea.descripcion} "
                f"{tarea.fecha} "
                f"{tarea.estado}"
            ).lower()

            if palabra in texto:
                resultados.append(
                    f"{i}. [{tarea.estado}] "
                    f"{tarea.titulo} | "
                    f"{tarea.descripcion} | "
                    f"Fecha: {tarea.fecha}"
                )

        return resultados if resultados else [
            "No se encontraron coincidencias."
        ]

    def editar_tarea(self, indice, nuevo_titulo, nueva_descripcion, nueva_fecha):
        tarea = self.obtener_tarea(indice)

        tarea.titulo = self.validar_texto(
            nuevo_titulo,
            "titulo"
        ).title()

        tarea.descripcion = self.validar_texto(
            nueva_descripcion,
            "descripcion"
        )

        tarea.fecha = self.validar_fecha(
            nueva_fecha
        )

        self.guardar_tareas()

        return "Tarea editada correctamente."

    def cambiar_estado(self, indice, nuevo_estado):
        tarea = self.obtener_tarea(indice)

        tarea.estado = self.validar_estado(
            nuevo_estado
        )

        self.guardar_tareas()

        return "Estado actualizado correctamente."

    def eliminar_tarea(self, indice):
        if indice < 1 or indice > len(self.tareas):
            raise IndexError(
                "El número de tarea no existe."
            )

        eliminada = self.tareas.pop(indice - 1)

        self.guardar_tareas()

        return f"Tarea eliminada: {eliminada.titulo}"

    def obtener_tarea(self, indice):
        if indice < 1 or indice > len(self.tareas):
            raise IndexError(
                "El número de tarea no existe."
            )

        return self.tareas[indice - 1]

    def guardar_tareas(self):
        datos = [tarea.to_dict() for tarea in self.tareas]

        with open(
            self.archivo,
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(
                datos,
                f,
                ensure_ascii=False,
                indent=4
            )

    def cargar_tareas(self):
        if not os.path.exists(self.archivo):
            return []

        try:
            with open(
                self.archivo,
                "r",
                encoding="utf-8"
            ) as f:
                datos = json.load(f)

            return [
                Tarea.from_dict(item)
                for item in datos
            ]

        except json.JSONDecodeError:
            print(
                "Advertencia: el archivo JSON está dañado. "
                "Se iniciará con una lista vacía."
            )
            return []

        except Exception as e:
            print(
                f"Error al cargar el archivo: {e}"
            )
            return []


def mostrar_menu():
    print("\n=== SISTEMA DE GESTIÓN DE TAREAS ACADÉMICAS ===")
    print("1. Agregar tarea")
    print("2. Listar tareas")
    print("3. Buscar tarea")
    print("4. Editar tarea")
    print("5. Cambiar estado")
    print("6. Eliminar tarea")
    print("7. Salir")


def ejecutar_app():
    gestor = GestorTareas()

    while True:
        mostrar_menu()
        opcion = input("Elige una opción: ").strip()

        try:
            if opcion == "1":
                titulo = input("Título: ")
                descripcion = input("Descripción: ")
                fecha = input("Fecha (AAAA-MM-DD): ")

                print(
                    gestor.agregar_tarea(
                        titulo,
                        descripcion,
                        fecha
                    )
                )

            elif opcion == "2":
                print(
                    gestor.listar_tareas()
                )

            elif opcion == "3":
                palabra = input(
                    "Palabra clave: "
                )

                resultados = gestor.buscar_tareas(
                    palabra
                )

                print(
                    "\n".join(resultados)
                )

            elif opcion == "4":
                indice = int(
                    input(
                        "Número de tarea a editar: "
                    )
                )

                nuevo_titulo = input(
                    "Nuevo título: "
                )

                nueva_descripcion = input(
                    "Nueva descripción: "
                )

                nueva_fecha = input(
                    "Nueva fecha (AAAA-MM-DD): "
                )

                print(
                    gestor.editar_tarea(
                        indice,
                        nuevo_titulo,
                        nueva_descripcion,
                        nueva_fecha
                    )
                )

            elif opcion == "5":
                indice = int(
                    input(
                        "Número de tarea: "
                    )
                )

                nuevo_estado = input(
                    "Nuevo estado (pendiente / en proceso / completada): "
                )

                print(
                    gestor.cambiar_estado(
                        indice,
                        nuevo_estado
                    )
                )

            elif opcion == "6":
                indice = int(
                    input(
                        "Número de tarea: "
                    )
                )

                print(
                    gestor.eliminar_tarea(
                        indice
                    )
                )

            elif opcion == "7":
                print(
                    "Saliendo del sistema..."
                )
                break

            else:
                print(
                    "Opción inválida."
                )

        except ValueError as e:
            print(
                f"Error de validación: {e}"
            )

        except IndexError as e:
            print(
                f"Error de índice: {e}"
            )

        except Exception as e:
            print(
                f"Error inesperado: {e}"
            )


if __name__ == "__main__":
    ejecutar_app()
