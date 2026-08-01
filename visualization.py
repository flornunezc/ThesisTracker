import plotly.graph_objects as go
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