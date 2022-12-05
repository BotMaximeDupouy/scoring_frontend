import numpy as np
import plotly.graph_objects as go


def create_gauge_plot(probabilitie):
    '''
    https://community.plotly.com/t/gauge-chart-with-python/57279/3
    Create a gauge graph
    '''
    plot_bgcolor = "#fff"
    quadrant_colors = [plot_bgcolor, "#357A8C", "#4286DE", "#F7CB48", "#EE9948", "#BD3E1E"]
    quadrant_text = ["", "<b>Very high</b>", "<b>High</b>", "<b>Medium</b>", "<b>Low</b>", "<b>Very low</b>"]
    n_quadrants = len(quadrant_colors) - 1

    current_value = (probabilitie-0.5)
    min_value = 0 # valeur minimale
    max_value = 0.5 # valeur maximale
    hand_length = np.sqrt(2) / 4 # for arrow
    hand_angle = np.pi * (1 - (
        max(min_value, min(max_value, current_value)
            ) - min_value) / (max_value - min_value)
        ) # for arrow

    fig = go.Figure(
        data=[
            go.Pie(
                values=[0.5] + (np.ones(n_quadrants) / 2 / n_quadrants).tolist(),
                rotation=90,
                hole=0.5,
                marker_colors=quadrant_colors,
                text=quadrant_text,
                textinfo="text",
                hoverinfo="skip",
            ),
        ],
        layout=go.Layout(
            showlegend=False,
            margin=dict(b=0,t=10,l=10,r=10),
            width=450,
            height=450,
            paper_bgcolor=plot_bgcolor,
            annotations=[
                go.layout.Annotation(
                    text=f"<b>Probability that client is well classified :</b><br>{round(probabilitie, 2)}",
                    x=0.5, xanchor="center", xref="paper",
                    y=0.25, yanchor="bottom", yref="paper",
                    showarrow=False,
                )
            ],
            shapes=[
                go.layout.Shape(
                    type="circle",
                    x0=0.48, x1=0.52,
                    y0=0.48, y1=0.52,
                    fillcolor="#333",
                    line_color="#333",
                ),
                go.layout.Shape(
                    type="line",
                    x0=0.5, x1=0.5 + hand_length * np.cos(hand_angle),
                    y0=0.5, y1=0.5 + hand_length * np.sin(hand_angle),
                    line=dict(color="#333", width=4)
                )
            ]
        )
    )
    return fig #fig.show()
