# Dashboard entry file
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from src.pymongo_db import db
import pandas as pd
import numpy as np

collection = db["frontend"]


def create_data_for_barchart(collection):
    base_dataframe = pd.DataFrame.from_records(collection.find())
    all_models = list(np.unique(base_dataframe.model))
    ti_df = base_dataframe.loc[base_dataframe.is_ti == True]
    nonti_df = base_dataframe.loc[base_dataframe.is_ti == False]
    grouped_ti = ti_df.groupby("model").agg("mean").sort_values("model").reset_index()
    grouped_nonti = (
        nonti_df.groupby("model").agg("mean").sort_values("model").reset_index()
    )

    for model in all_models:
        row = {
            key: zero
            for key in list(base_dataframe.columns)
            for zero in [0] * len(base_dataframe.columns)
        }
        row["model"] = model

        if (grouped_nonti.model == model).sum() == 0:
            grouped_nonti.append(row, ignore_index=True)

        if (grouped_ti.model == model).sum() == 0:
            grouped_ti.append(row, ignore_index=True)

        return grouped_ti, grouped_nonti


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

ti_data, nonti_data = create_data_for_barchart(collection)

app.layout = html.Div(
    children=[
        html.H1(children="Used GPU Market on /r/hardwareswap"),
        html.Div(
            children="""
        A visualization dashboard to look at used GPU pricing for NVidia GPUs.
    """
        ),
        dcc.Graph(
            id="example-graph",
            figure={
                "data": [
                    {
                        "x": nonti_data.model.map(lambda x: "GTX " + str(x)).values,
                        "y": nonti_data.price,
                        "type": "bar",
                        "name": "non-TI",
                    },
                    {
                        "x": ti_data.model.map(lambda x: "GTX " + str(x)).values,
                        "y": ti_data.price,
                        "type": "bar",
                        "name": "TI",
                    },
                ],
                "layout": {"title": "Average GPU Price in Dollars"},
            },
        ),
    ]
)


if __name__ == "__main__":
    app.run_server(debug=True)
