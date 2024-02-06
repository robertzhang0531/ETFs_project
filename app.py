from flask import Flask, render_template, request
import pandas as pd
import plotly
import plotly.graph_objects as go
import json
import os
import glob

app = Flask(__name__)

def load_etf_info():
    """
    Dynamically loads ETF information based on CSV files in the data/etf_csvs directory.
    Returns a dictionary with tickers as keys and file paths as values.
    """
    csv_files = glob.glob('data/etf_csvs/*.csv')
    etf_info = {}
    for csv_file in csv_files:
        filename = os.path.basename(csv_file)
        ticker = filename.split('_prices')[0]
        etf_info[ticker] = csv_file
    return etf_info

@app.route('/', methods=['GET', 'POST'])
def index():
    etf_info = load_etf_info()
    selected_ticker = request.form.get('etf_ticker', list(etf_info.keys())[0] if etf_info else 'SPY')
    selected_data_points = request.form.getlist('data_points')

    csv_path = etf_info.get(selected_ticker, '')
    if csv_path and os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
    else:
        df = pd.DataFrame()
    
    fig = go.Figure()

    if df.empty:
        fig.update_layout(title="No Data Available")
    else:
        for data_point in selected_data_points:
            if data_point in df.columns:
                if data_point == 'Volume':
                    fig.add_trace(go.Bar(x=df['Date'], y=df[data_point], name=data_point))
                else:
                    fig.add_trace(go.Scatter(x=df['Date'], y=df[data_point], mode='lines', name=data_point))
        fig.update_layout(title=f'{selected_ticker} Data Overview', xaxis_title='Date', yaxis_title='Value')

    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html', etf_info=etf_info, selected_ticker=selected_ticker, graph_json=graph_json)

if __name__ == '__main__':
    app.run(debug=True)
