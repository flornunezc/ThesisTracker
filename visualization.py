import plotly.graph_objects as go
import plotly.express as px
from config import METRICAS


def mostrar_grafico_evolucion(series):

    figura = go.Figure()
    
    for metrica, info in METRICAS.items():
        
        visible = True if metrica == "palabras" else "legendonly"

        figura.add_trace(

            go.Scatter(

                x=series["fechas"],

                y=series[metrica],

                mode="lines+markers",

                name=info["nombre"],
            
                customdata=series["versiones"],

                hovertemplate=(
                "<b>Versión %{customdata}</b><br>"
                "Fecha: %{x}<br>"
                f"{info['nombre']}: %{{y}}"
                "<extra></extra>"
                
                ),
                
                visible=visible
                

            )

        )


    figura.update_layout(

        title=f"Evolución del proyecto",

        xaxis_title="Fecha",

        yaxis_title="Valor",

        template="plotly_white"

    )


    figura.show()
    
    
def graficar_ritmo_versiones(ritmo):

    cambios = ritmo["cambios"]

    versiones = []
    palabras = []

    for cambio in cambios:

        versiones.append(
            f"{cambio['version_anterior']}→{cambio['version']}"
        )

        palabras.append(
            cambio["cambio_palabras"]
        )

    fig = px.bar(
        x=versiones,
        y=palabras,
        labels={
            "x": "Cambio de versión",
            "y": "Palabras"
        },
        title="Palabras agregadas entre versiones"
    )

    fig.update_layout(
        xaxis_title="Cambio de versión",
        yaxis_title="Palabras",
        hovermode="x"
    )

    fig.show()