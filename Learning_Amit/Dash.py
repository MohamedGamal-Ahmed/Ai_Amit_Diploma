import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

""" 
dash >>> main app object
dcc >>> dash core components like graphs, dropdowns, sliders
html >>> HTML components (div , h1, table, tr, td)
input, output >>> for interactivity and callbacks

"""

df = pd.read_csv('C:/Users/Mgama/Ai_Amit_Diploma/Learning_Amit/Dash.csv')
app = Dash()
app. title = "Interactive Dashboard"

num_cols = df.select_dtypes(include='number').columns

app.layout = html.Div([html.H1("Interactive Dashboard with Pie chart"),
                    html.Label("Select a value to show in pie chart"),
                    dcc.Dropdown(id = 'column-dropdown', 
                                options =[{'label':col,'value':col} for col in num_cols],
                                value=num_cols[0]),
                    dcc.Graph(id = 'pie-chart')

                    ])

@app.callback(
    Output('pie-chart', 'figure'),
    Input('column-dropdown', 'value')
)

def update_pie_chart(selected_column):
    groups = df.groupby('Area')[selected_column].sum().reset_index()
    fig = px.pie(
        groups,
        names='Area',
        values=selected_column,
    )

    return fig

if __name__ == '__main__':
    app.run(debug=True)