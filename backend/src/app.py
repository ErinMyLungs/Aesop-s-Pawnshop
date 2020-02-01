# Dashboard entry file
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
from pymongo_db import db

# TODO: Refactor this to hell and back because it's currently pretty terrible

collection = db["frontend"]


def create_date_labels(dataframe):
    """
    Create date_labels column for easy labeling of our line plot
    :param dataframe: dataframe with created column
    :return: dataframe with date_label column
    """
    dataframe.loc[:, "created_datetime"] = pd.to_datetime(dataframe.created, unit="s")
    dataframe.loc[:, "date_label"] = dataframe.created_datetime.map(
        lambda x: f"{x.month}-{x.day}-{x.year}"
    )
    dataframe.drop(axis=0, columns="created_datetime", inplace=True)
    return dataframe


def create_data_for_barchart(collection):
    """
    Creates dataframes with data from front-end collection and pre-processes it for dashboard
    :param collection: collection where front-end preprocessed data lives
    :return: tuple of base dataframe and the aggregated ti and non-ti dataframes
    """
    base_dataframe = pd.DataFrame.from_records(collection.find())

    base_dataframe = create_date_labels(base_dataframe)

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

        return base_dataframe, grouped_ti, grouped_nonti


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

raw, ti_data, nonti_data = create_data_for_barchart(collection)


app.layout = html.Div(
    [
        html.H1(children="Used GPU Market on /r/hardwareswap"),
        html.Div(
            children="""
        A visualization dashboard to look at used GPU pricing for NVidia GPUs.
    """
        ),
        dcc.Graph(
            id="gpu-bar-chart",
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
                "layout": {
                    "title": "Average GPU Price in Dollars",
                    "clickmode": "event",
                    "xaxis": {"title": "GPU Model (Arranged by Generation)"},
                    "yaxis": {"title": "Average Cost USD"},
                },
            },
        ),
        dcc.Graph(
            id="model-price-over-time-lineplot",
            figure={"data": [], "layout": {"title": "model price over time"}},
        ),
    ]
)


@app.callback(
    Output("model-price-over-time-lineplot", "figure"),
    [Input("gpu-bar-chart", "clickData")],
)
def display_click_data(clickData):
    """
    Callback function that adds interactivity to bar chart above -> on click sends model data to line plot below
    :param clickData: Callback val from gpu-bar-chart
    :return: updated lineplot
    """
    if not clickData:
        return {"data": [dict(x=0, y=0, ids=0, type="plot", mode="lines+markers")]}

    ti = False
    if len(clickData.get("points")) == 2:
        ti = True

    traces = []

    model = clickData.get("points")[0].get("x")
    if not model:
        return

    model = int(model[model.find(" ") + 1 :])
    non_ti_model_data = raw.loc[raw.is_ti == False].loc[raw.model == model]

    ticktext = list(non_ti_model_data.date_label.values)
    tickval = list(non_ti_model_data.created.values)
    non_ti_model_data = non_ti_model_data.sort_values("created")
    traces.append(
        dict(
            x=non_ti_model_data.created,
            y=non_ti_model_data.price,
            ids=non_ti_model_data.post_id,
            type="plot",
            mode="lines+markers",
            name=f"GTX {model}",
        )
    )
    if ti:
        ti_model_data = raw.loc[raw.is_ti == True].loc[raw.model == model]
        ti_model_data = ti_model_data.sort_values("created")

        ticktext.extend(list(ti_model_data.date_label.values))
        tickval.extend(list(ti_model_data.created.values))

        traces.append(
            dict(
                x=ti_model_data.created,
                y=ti_model_data.price,
                ids=ti_model_data.post_id,
                type="plot",
                mode="lines+markers",
                name=f"GTX {model}Ti",
            )
        )
    if (
        len(ticktext) > 10
    ):  # This logic culls the ticktext from everything to one that is at each 10% of the data (min, 10%, 20%,..., max) so x-tick labels are less cluttered
        quartiles = np.arange(0, 110, 10)  # generate np array 0 -> 100 in 10s
        percentile = np.percentile(tickval, quartiles, interpolation="nearest")
        positions = [np.argwhere(tickval == perc).item() for perc in percentile]
        ticktext = [ticktext[pos] for pos in positions]
        tickval = [tickval[pos] for pos in positions]

    return {
        "data": traces,
        "layout": {
            "title": f"Model {model} price over time",
            "xaxis": {"title": "Date", "ticktext": ticktext, "tickvals": tickval},
            "yaxis": {"title": "Sale Price USD"},
        },
    }


if __name__ == "__main__":
    aws = False

    if aws:
        app.run_server(debug=False, host="0.0.0.0", port=80)
    else:
        app.run_server(debug=True)
