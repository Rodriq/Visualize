from flask import Flask, redirect, url_for, request, render_template
import time

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import seaborn as sns
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

data_frame = ''

# Views
data_frame_head = ''
data_frame_tail = ''
data_frame_columns = ''
data_frame_shape = ''
data_frame_type = ''
data_frame_info = ''
data_frame_describe = ''

data_frame_mean = ''
data_frame_corr = ''
data_frame_count = ''
data_frame_min = ''
data_frame_max = ''
data_frame_median = ''
data_frame_std = ''

data_frame_isnull = ''
data_frame_notnull = ''


@app.route('/')
def index():
    return render_template('index.html', state=0)


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/upload_dataset', methods=['POST', 'GET'])
def upload_dataset():
    if request.method == 'POST':
        file_path = request.form['file-path']
        ds_type = int(request.form['type'])
        print(ds_type, "8888888888")
        try:
            global data_frame
            if ds_type == 1:
                df = pd.read_csv(str(file_path))
                data_frame = df
            if ds_type == 2:
                df = pd.read_excel(str(file_path))
                data_frame = df
            if ds_type == 3:
                df = pd.read_json(str(file_path))
                data_frame = df
        except:
            return render_template('index.html', alert="Error reading that file, Please try again.", state=0)
        # print(str(df))
        global data_frame_columns
        global data_frame_info
        global data_frame_describe
        data_frame_describe = data_frame.describe()
        data_frame_columns = [column for column in data_frame.columns]
        print(data_frame_columns, '---------------')
        # return render_template('columns.html', data_columns=data_frame_columns)
        # data_frame_info = data_frame.info()
        # print(data_frame_info, "innnnnnnnnnnfooooooooooooooooooo")
        return render_template('index.html', state=1, data_columns=data_frame_columns, describe=data_frame_describe.to_html())
    else:
        return redirect(url_for('index'))


@app.route('/print_columns')
def print_columns():
    global data_frame_columns
    data_frame_columns = [column for column in data_frame.columns]
    # print(str(data_frame.columns))
    # print(type(data_frame.columns))
    print(data_frame_columns, '---------------')
    return render_template('columns.html', data_columns=data_frame_columns)
    # return(str(data_frame.columns))


@app.route('/print_head', methods=['POST', 'GET'])
def print_head():
    if request.method == 'POST':
        df_num = request.form['dataset-number']
        # print(data_frame.h)
        try:
            global data_frame_head
            data_frame_head = data_frame.head(int(df_num))
        except:
            return render_template('index.html', alert="Error fetching head, Please try again.", state=1)

        print(data_frame_head.keys, '********11111111***********')
        return render_template('index.html', data_columns=data_frame_columns, dfHead=data_frame_head, length=len(data_frame_head.values[0]), state=1, sub_state=1.1)
        # return str(data_frame_head)
    else:
        return redirect(url_for('index'))
    # data_frame_head = [column for column in data_frame.head()]


@app.route('/print_tail', methods=['POST', 'GET'])
def print_tail():
    if request.method == 'POST':
        df_num = request.form['dataset-number']
        # print(data_frame.h)
        try:
            global data_frame_tail
            data_frame_tail = data_frame.tail(int(df_num))
        except:
            return render_template('index.html', alert="Error fetching head, Please try again.", state=1)

        print(data_frame_head.keys, '********11111111***********')
        return render_template('index.html', data_columns=data_frame_columns, dfTail=data_frame_tail, length=len(data_frame_head.values[0]), state=1, sub_state=1.2)
        # return str(data_frame_head)
    else:
        return redirect(url_for('index'))


@app.route('/data')
def data():
    return render_template('home.html')


@app.route('/info')
def info():
    global data_frame_info
    time.sleep(1)
    data_frame_info = data_frame.info()
    print(data_frame_info, "ffffffffdfffffff")
    return render_template('info.html', info=data_frame_info)


@app.route('/describe')
def describe():
    global data_frame_describe
    data_frame_describe = data_frame.describe()
    print(data_frame_describe, "fffffffffffffff")
    print(len(data_frame_describe), "eeeeeeeeee")
    # print(len(data_frame_describe.values[0]), "gggggggggggg")
    formated = data_frame_describe.to_html()
    print(formated, "gggggggggggg")
    return render_template('info.html', info=data_frame_describe.to_html())


@app.route('/dtypes')
def dtypes():
    global data_frame_type
    data_frame_type = data_frame.dtypes
    return render_template('export.html')


@app.route('/view')
def view():
    return render_template('view.html')


@app.route('/statistics')
def statistics():
    global data_frame_corr
    global data_frame_max
    global data_frame_min
    global data_frame_mean
    data_frame_corr = data_frame.corr().to_html()
    data_frame_mean = data_frame.mean().to_dict()
    data_frame_max = data_frame.max().to_dict()
    data_frame_min = data_frame.min().to_dict()
    return render_template('pages/statistics.html', state=3, corr=data_frame_corr, mean=data_frame_mean, min=data_frame_min, max=data_frame_max)


@app.route('/plot')
def plot():
    global data_frame_columns
    return render_template('pages/plot.html', data_columns=data_frame_columns, state=4)


@app.route('/plot_graph', methods=['GET', 'POST'])
def plot_graph():
    global data_frame_columns
    if request.method == 'POST':
        global data_frame
        column1 = str(request.form['column1'])
        column2 = str(request.form['column2'])
        graph_type = int(request.form['type'])
        plt.figure()
        if graph_type == 1:
            try:
                plt.plot(data_frame[column1], data_frame[column2])
                plt.legend()
                plt.xlabel(column1)
                plt.ylabel(column2)
                plt.title("Line plot of " + column1 + " and " + column2)
                dir = "static/images/"+str(time.time())+".png"
                plt.savefig(dir)
                return render_template('pages/plot.html', data_columns=data_frame_columns, state=4, path=dir, sub_state=4.1)
            except:
                return render_template('pages/plot.html', data_columns=data_frame_columns, state=4, alert="Error Cannot Plot tables")
        elif graph_type == 2:
            try:
                plt.scatter(data_frame[column1], data_frame[column2])
                plt.legend()
                plt.xlabel(column1)
                plt.ylabel(column2)
                plt.title("Scatter plot of " + column1 + " and " + column2)
                dir = "static/images/"+str(time.time())+".png"
                plt.savefig(dir)
                return render_template('pages/plot.html', data_columns=data_frame_columns, state=4, path=dir, sub_state=4.1)
            except:
                return render_template('pages/plot.html', data_columns=data_frame_columns, state=4, alert="Error Cannot Plot tables")

        elif graph_type == 3:
            try:
                plt.bar(data_frame[column1], data_frame[column2],
                        label=column1, color="c", width=.5)
                plt.legend()
                plt.xlabel(column1)
                plt.ylabel(column2)
                plt.title("Bar plot of "+ column1 +" and " + column2)
                dir = "static/images/"+str(time.time())+".png"
                plt.savefig(dir)
                return render_template('pages/plot.html', data_columns=data_frame_columns, state=4, path=dir, sub_state=4.1)
            except:
                return render_template('pages/plot.html', data_columns=data_frame_columns, state=4, alert="Error Cannot Plot tables")

        elif graph_type == 4:
            try:
                plt.hist(data_frame[column1], data_frame[column2], histtype="bar", rwidth=0.8)
                plt.legend()
                plt.xlabel(column1)
                plt.ylabel(column2)
                plt.title("Histogram plot of " + column1 + " and " + column2)
                dir = "static/images/"+str(time.time())+".png"
                plt.savefig(dir)
                return render_template('pages/plot.html', data_columns=data_frame_columns, state=4, path=dir, sub_state=4.1)
            except:
                return render_template('pages/plot.html', data_columns=data_frame_columns, state=4, alert="Error Cannot Plot tables")


    # return render_template('pages/plot.html', data_columns=data_frame_columns, state=4)


@app.route('/export')
def export():
    return render_template('pages/export.html', state=5)


@app.route('/export_dataset', methods=['POST', 'GET'])
def export_dataset():
    if request.method == 'POST':
        file_path = request.form['file-path']
        ds_type = int(request.form['type'])
        print(ds_type, "8888888888")
        try:
            global data_frame
            if ds_type == 1:
                data_frame.to_csv(str(file_path))
            if ds_type == 2:
                data_frame.to_excel(str(file_path))
            if ds_type == 3:
                data_frame.to_json(str(file_path))
        except:
            return render_template('pages/export.html', alert="Error Exporting that file, Please try again.", state=5)
        return render_template('index.html', state=0)


if __name__ == '__main__':
    app.run(debug=True)
