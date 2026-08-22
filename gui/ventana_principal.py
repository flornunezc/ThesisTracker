import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from analyzer import analizar_documento
from database import (
    obtener_historial,
    version_a_diccionario,
    obtener_ultima_version,
    obtener_evolucion
    )
from config import NOMBRE_APP, METRICAS
from stats import (
    obtener_estado_tesis,
    preparar_series_temporales,
    calcular_ritmo_versiones
    )
from visualization import (
    mostrar_grafico_evolucion,
    graficar_ritmo_versiones
    )


def seleccionar_documento():
    ruta = filedialog.askopenfilename(
        title="Seleccionar documento Word",
        filetypes=[
            ("Documentos Word", "*.docx"),
            ("Todos los archivos", "*.*")
        ]
    )

    if ruta:
        resultado = analizar_documento(ruta)

        mensaje = ""

        for metrica, info in METRICAS.items():

            mensaje += (
                f"{info['nombre']}: "
                f"{resultado[metrica]}\n"
            )

        messagebox.showinfo(
            "Resultado del análisis",
            mensaje
        )
        


def mostrar_historial_gui():

    historial = obtener_historial()

    if not historial:
        messagebox.showinfo(
            "Historial de escritura",
            "Todavía no hay versiones registradas."
        )
        return

    texto = ""

    for version in historial:

        version = version_a_diccionario(version)

        texto += (
            f"Versión: {version['id']}\n"
            f"Fecha: {version['fecha']}\n"
        )

        for metrica, info in METRICAS.items():

            cambio = version["cambio_" + metrica]

            if cambio != 0:
                texto += (
                    f"{info['nombre']}: "
                    f"{cambio:+}\n"
                )

        texto += "\n"

    messagebox.showinfo(
        "Historial de escritura",
        texto
    )
    


def mostrar_estado_tesis_gui():

    estado = obtener_estado_tesis()

    if estado is None:

        messagebox.showinfo(
            "Estado de la tesis",
            "Todavía no hay versiones registradas."
        )

        return


    texto = ""

    texto += (
        f"Versión: {estado['version_id']}\n"
        f"Fecha: {estado['fecha']}\n\n"
    )


    texto += "ESTRUCTURA\n"
    texto += "------------------------------\n"

    texto += (
        f"Capítulos: {estado['estadisticas']['capitulos']}\n"
        f"Secciones: {estado['estadisticas']['secciones']}\n"
        f"Subsecciones: {estado['estadisticas']['subsecciones']}\n\n"
    )
    
    
    ultima = obtener_ultima_version()
    ultima = version_a_diccionario(ultima)

    texto += "CONTENIDO\n"
    texto += "------------------------------\n"

    for metrica, info in METRICAS.items():

        texto += (
            f"{info['nombre']}: "
            f"{ultima[metrica]}\n"
        )

    texto += "\n"


    texto += "SECCIONES MÁS Y MENOS TRABAJADAS\n"
    texto += "------------------------------\n"

    mas = estado["estadisticas"]["mas_trabajada"]

    if mas:

        texto += (
            f"Más trabajada: {mas['capitulo_id']} | "
            f"{mas['capitulo']}\n"
            f"  {mas['seccion_id']} | "
            f"{mas['seccion']} - "
            f"{mas['palabras']} palabras\n\n"
        )


    menos = estado["estadisticas"]["menos_trabajada"]

    if menos:

        texto += (
            f"Menos trabajada: {menos['capitulo_id']} | "
            f"{menos['capitulo']}\n"
            f"  {menos['seccion_id']} | "
            f"{menos['seccion']} - "
            f"{menos['palabras']} palabras\n"
        )


    messagebox.showinfo(
        "Estado de la tesis",
        texto
    )



def mostrar_estado_por_capitulo_gui():

    estado = obtener_estado_tesis()

    if estado is None:

        messagebox.showinfo(
            "Estado por capítulo",
            "Todavía no hay versiones registradas."
        )

        return


    ventana_capitulos = tk.Toplevel()

    ventana_capitulos.title("Estado por capítulo")
    ventana_capitulos.geometry("900x500")


    titulo = tk.Label(
        ventana_capitulos,
        text="Estado por capítulo",
        font=("Arial", 18)
    )

    titulo.pack(pady=15)


    # COLUMNAS

    columnas = ["id", "titulo"]

    for metrica in METRICAS:

        columnas.append(metrica)


    tabla = ttk.Treeview(
        ventana_capitulos,
        columns=columnas,
        show="headings"
    )


    # ENCABEZADOS

    tabla.heading(
        "id",
        text="ID"
    )

    tabla.heading(
        "titulo",
        text="Capítulo"
    )


    for metrica, info in METRICAS.items():

        tabla.heading(
            metrica,
            text=info["nombre"]
        )


    # ANCHO DE COLUMNAS

    tabla.column(
        "id",
        width=60,
        anchor="center"
    )

    tabla.column(
        "titulo",
        width=300,
        anchor="w"
    )


    for metrica in METRICAS:

        tabla.column(
            metrica,
            width=120,
            anchor="center"
        )


    # DATOS

    for capitulo in estado["capitulos"]:

        valores = [
            capitulo["id"],
            capitulo["titulo"]
        ]

        for metrica in METRICAS:

            valores.append(
                capitulo["metricas"][metrica]
            )


        tabla.insert(
            "",
            "end",
            values=valores
        )


    # SCROLL VERTICAL

    scrollbar_vertical = ttk.Scrollbar(
        ventana_capitulos,
        orient="vertical",
        command=tabla.yview
    )

    tabla.configure(
        yscrollcommand=scrollbar_vertical.set
    )


    # SCROLL HORIZONTAL

    scrollbar_horizontal = ttk.Scrollbar(
        ventana_capitulos,
        orient="horizontal",
        command=tabla.xview
    )

    tabla.configure(
        xscrollcommand=scrollbar_horizontal.set
    )


    # POSICIONAR TABLA

    tabla.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar_vertical.pack(
        side="right",
        fill="y"
    )

    scrollbar_horizontal.pack(
        side="bottom",
        fill="x"
    )
    
    

def mostrar_progreso_escritura_gui():

    estado = obtener_estado_tesis()

    if estado is None:

        messagebox.showinfo(
            "Progreso de escritura",
            "Todavía no hay versiones registradas."
        )

        return


    ventana_progreso = tk.Toplevel()

    ventana_progreso.title("Progreso de escritura")
    ventana_progreso.geometry("600x400")


    titulo = tk.Label(
        ventana_progreso,
        text="Progreso de escritura",
        font=("Arial", 18)
    )

    titulo.pack(pady=20)


    mas = estado["estadisticas"]["mas_trabajada"]
    menos = estado["estadisticas"]["menos_trabajada"]


    texto = ""


    if mas:

        texto += "SECCIÓN MÁS TRABAJADA\n"
        texto += "------------------------------\n"

        texto += (
            f"{mas['capitulo_id']} | "
            f"{mas['capitulo']}\n"
        )

        texto += (
            f"{mas['seccion_id']} | "
            f"{mas['seccion']}\n"
        )

        texto += (
            f"Palabras: {mas['palabras']}\n\n"
        )


    if menos:

        texto += "SECCIÓN MENOS TRABAJADA\n"
        texto += "------------------------------\n"

        texto += (
            f"{menos['capitulo_id']} | "
            f"{menos['capitulo']}\n"
        )

        texto += (
            f"{menos['seccion_id']} | "
            f"{menos['seccion']}\n"
        )

        texto += (
            f"Palabras: {menos['palabras']}\n"
        )


    etiqueta = tk.Label(
        ventana_progreso,
        text=texto,
        justify="left",
        anchor="w",
        font=("Arial", 11)
    )

    etiqueta.pack(
        padx=30,
        pady=10,
        anchor="w"
    )
    

def mostrar_evolucion_gui():

    evolucion = obtener_evolucion()

    if not evolucion:

        messagebox.showinfo(
            "Evolución del proyecto",
            "Todavía no hay versiones registradas."
        )

        return


    ventana_evolucion = tk.Toplevel()

    ventana_evolucion.title("Evolución del proyecto")
    ventana_evolucion.geometry("500x300")


    titulo = tk.Label(
        ventana_evolucion,
        text="Evolución del proyecto",
        font=("Arial", 18)
    )

    titulo.pack(pady=25)


    boton_evolucion = tk.Button(
        ventana_evolucion,
        text="Evolución temporal",
        command=mostrar_evolucion_temporal_gui,
        width=25,
        height=2
    )

    boton_evolucion.pack(pady=10)


    boton_ritmo = tk.Button(
        ventana_evolucion,
        text="Ritmo de escritura",
        command=mostrar_ritmo_gui,
        width=25,
        height=2
    )

    boton_ritmo.pack(pady=10)
    
    
    boton_volver = tk.Button(
        ventana_evolucion,
        text="Volver",
        command=ventana_evolucion.destroy,
        width=25,
        height=2
    )

    boton_volver.pack(pady=15)
    


def mostrar_evolucion_temporal_gui():

    evolucion = obtener_evolucion()

    if not evolucion:

        messagebox.showinfo(
            "Evolución temporal",
            "Todavía no hay versiones registradas."
        )

        return


    series = preparar_series_temporales(evolucion)

    mostrar_grafico_evolucion(series)
    
    
def mostrar_ritmo_gui():

    evolucion = obtener_evolucion()

    if not evolucion:

        messagebox.showinfo(
            "Ritmo de escritura",
            "Todavía no hay versiones registradas."
        )

        return


    ritmo = calcular_ritmo_versiones(evolucion)

    if ritmo is None:

        messagebox.showinfo(
            "Ritmo de escritura",
            "Se necesitan al menos dos versiones para calcular el ritmo."
        )

        return


    graficar_ritmo_versiones(ritmo)
    
    
    
def mostrar_estado_tesis_menu_gui():

    ventana_estado = tk.Toplevel()

    ventana_estado.title("Estado de la tesis")
    ventana_estado.geometry("500x350")


    titulo = tk.Label(
        ventana_estado,
        text="Estado de la tesis",
        font=("Arial", 18)
    )

    titulo.pack(pady=25)


    boton_resumen = tk.Button(
        ventana_estado,
        text="Resumen de la tesis",
        command=mostrar_estado_tesis_gui,
        width=25,
        height=2
    )

    boton_resumen.pack(pady=10)


    boton_capitulos = tk.Button(
        ventana_estado,
        text="Estado por capítulo",
        command=mostrar_estado_por_capitulo_gui,
        width=25,
        height=2
    )

    boton_capitulos.pack(pady=10)


    boton_progreso = tk.Button(
        ventana_estado,
        text="Progreso de escritura",
        command=mostrar_progreso_escritura_gui,
        width=25,
        height=2
    )

    boton_progreso.pack(pady=10)
    
    
    boton_volver = tk.Button(
        ventana_estado,
        text="Volver",
        command=ventana_estado.destroy,
        width=25,
        height=2
    )

    boton_volver.pack(pady=15)
    
    
    

def iniciar_app():

    ventana = tk.Tk()

    ventana.title(NOMBRE_APP)
    ventana.geometry("500x300")


    titulo = tk.Label(
        ventana,
        text=NOMBRE_APP,
        font=("Arial", 24)
    )

    titulo.pack(pady=(30, 5))
    
    subtitulo = tk.Label(
        ventana,
        text="Seguimiento de escritura",
        font=("Arial", 12)
    )

    subtitulo.pack(pady=(0, 20))
    
    
    proyecto = tk.Label(
        ventana,
        text="Proyecto actual: ProyectoActual",
        font=("Arial", 11)
    )

    proyecto.pack(pady=(0, 20))

############### BOTONES ################
###    
    boton_analizar = tk.Button(
        ventana,
        text="Analizar nueva versión",
        command=seleccionar_documento,
        width=25,
        height=2
    )

    boton_analizar.pack(pady=10)
    
###    
    boton_estado = tk.Button(
        ventana,
        text="Estado de la tesis",
        command=mostrar_estado_tesis_menu_gui,
        width=25,
        height=2
    )

    boton_estado.pack(pady=10)
    
    
###    
    boton_evolucion = tk.Button(
        ventana,
        text="Evolución del proyecto",
        command=mostrar_evolucion_gui,
        width=25,
        height=2
    )

    boton_evolucion.pack(pady=10)
    
###    
    boton_historial = tk.Button(
        ventana,
        text="Historial de versiones",
        command=mostrar_historial_gui,
        width=25,
        height=2
    )

    boton_historial.pack(pady=10)

###
    boton_salir = tk.Button(
        ventana,
        text="Salir",
        command=ventana.destroy,
        width=25,
        height=2
    )

    boton_salir.pack(pady=20)


    ventana.mainloop()