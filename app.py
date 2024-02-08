from flask import Flask, render_template, request
import pandas as pd
import plotly
import plotly.graph_objects as go
import json
import os
import glob
import datetime

app = Flask(__name__)

def load_etf_info():
    csv_files = glob.glob(os.path.join('data', 'etf_csvs', '*.csv'))
    etf_info = {}
    for csv_file in csv_files:
        filename = os.path.basename(csv_file)
        ticker, date_range = filename.split('_prices')[0], filename.split('_prices')[1].replace('.csv', '')
        if ticker not in etf_info:
            etf_info[ticker] = []
        etf_info[ticker].append(date_range)
    return etf_info

def get_user_date_input(prompt):
    date_str = input(prompt)
    try:
        valid_date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        normalized_date_str = valid_date.strftime('%Y-%m-%d')
        return normalized_date_str
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD format.")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    etf_info = load_etf_info()
    selected_ticker = request.form.get('etf_ticker', list(etf_info.keys())[0] if etf_info else 'SPY')
    selected_date_range = request.form.get('date_range', etf_info[selected_ticker][0] if etf_info[selected_ticker] else '')
    selected_data_points = request.form.getlist('data_points')

    # Construct file name using the selected ticker and date range
    csv_filename = f"{selected_ticker}_prices{selected_date_range}.csv"
    csv_path = os.path.join('data', 'etf_csvs', csv_filename)
    
    df = pd.read_csv(csv_path) if os.path.exists(csv_path) else pd.DataFrame()
    
    fig = go.Figure()
    if not df.empty:
        for data_point in ['Open', 'High', 'Low', 'Close', 'Volume']:
            if data_point in df.columns and data_point in selected_data_points:
                if data_point == 'Volume':
                    fig.add_trace(go.Bar(x=df['Date'], y=df[data_point], name=data_point))
                else:
                    fig.add_trace(go.Scatter(x=df['Date'], y=df[data_point], mode='lines', name=data_point))
        fig.update_layout(title=f'{selected_ticker} Data Overview', xaxis_title='Date', yaxis_title='Value')
    else:
        fig.update_layout(title="No Data Available")
    
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html', etf_info=etf_info, selected_ticker=selected_ticker, selected_date_range=selected_date_range, selected_data_points=selected_data_points, graph_json=graph_json)

if __name__ == '__main__':
    app.run(debug=True)
