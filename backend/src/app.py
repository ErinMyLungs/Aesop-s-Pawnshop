# Dashboard entry file
from flask import Flask, render_template, jsonify
import pandas as pd
import numpy as np
from pymongo_db import db


collection = db["frontend"]

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/v0.1/model', methods=['GET'])
def get_all_price_data():
    """
    Queries database and returns full aggregated pricing information.
    :return: json string in format
    [
    {model: '760', nonTiPrice: 69, tiPrice: 0},
    {model: '780', nonTiPrice: 107, tiPrice: 110}
    ]
    """
    base_df = pd.DataFrame.from_records(collection.find())

    grouped_dataframe = base_df[['model', 'is_ti', 'price']].groupby(['model', 'is_ti']).agg('mean').reset_index()
    frontend_dispaly_data = pd.DataFrame({'model': np.unique(grouped_dataframe.model)})

    ### This merges dataframe and reformats into a df that can then output a very convenient json string in proper format
    frontend_dispaly_data = frontend_dispaly_data.merge(
        right=grouped_dataframe[['model', 'price']].loc[grouped_dataframe.is_ti == False],
        on='model'
    ).rename(columns={'price': 'nonTiPrice'})  # camelCase used to match frontend naming convention

    frontend_dispaly_data = frontend_dispaly_data.merge(
        right=grouped_dataframe[['model', 'price']].loc[grouped_dataframe.is_ti == True],
        on='model',
        how='outer'
    ).rename(columns={'price': 'tiPrice'})

    frontend_dispaly_data = frontend_dispaly_data.fillna(0.0) #fills all missing models with a price of 0.0

    frontend_dispaly_data.loc[:, 'model'] = frontend_dispaly_data.model.map(lambda x: 'GTX ' + str(x) if x < 2000 else 'RTX ' + str(x))

    response = app.response_class(
        response=frontend_dispaly_data.to_json(orient='records'),
        status=200,
        mimetype='application/json')

    return response


if __name__ == '__main__':
    app.run(debug=True)
