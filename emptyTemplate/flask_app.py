from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import os
import pandas as pd
import stats_graphs as sg


app = Flask(__name__)

UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
ALLOWED_EXTENSIONS = set(os.getenv('ALLOWED_EXTENSIONS', 'csv').split(','))

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secret')  # used to sign session cookies


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('message.html', message="POST but no file in request.files", redirect_url=request.url)
        file = request.files['file']
        if file.filename == '':
            return render_template('message.html', message="You haven't selected a file.", redirect_url=request.url)
        if file:
            if not allowed_file(file.filename):
                return render_template('message.html', message="The file selected isn't a csv.", redirect_url=request.url)
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            try:
                data=pd.read_csv(file_path)
            except:
                return render_template('message.html', message="CSV can't be put into pandas.", redirect_url=request.url)

            required_columns = ["Name", "Age", "Job", "JoinDate", "Salary", "Department", "Location"]
            if not all(column in data.columns for column in required_columns):
                return render_template('message.html', message="Not all columns are present.", redirect_url=request.url)

            #Example of 2 stats and graph calling:
            firstThreeRows = sg.generate_first_three_rows(data)
            data4 = sg.generate_average_age(data)
            sg.generate_graph(data)

            # Important data values:
            # call here the rest of your stats
            data1 = sg.generate_stat1(data)
            data2 = sg.generate_stat2(data)
            data3 = sg.generate_stat3(data)

            sg.generate_graph1(data)
            sg.generate_graph2(data)
            sg.generate_graph3(data)
            sg.generate_graph4(data)
            sg.generate_graph5(data)


            ###Don't edit below
            graph_filename = 'graph.png'
            graph_filename1 = 'graph1.png'
            graph_filename2 = 'graph2.png'
            graph_filename3 = 'graph3.png'
            graph_filename4 = 'graph4.png'
            graph_filename5 = 'graph5.png'

            try:
                data_html = firstThreeRows.to_html()
            except:
                data_html = firstThreeRows
            try:
                data1_html = data1.to_html()
            except:
                data1_html = data1
            try:
                data2_html = data2.to_html()
            except:
                data2_html = data2
            try:
                data3_html = data3.to_html()
            except:
                data3_html = data3
            try:
                data4_html = data4.to_html()
            except:
                data4_html = data4


            ###
            return redirect(
                url_for('uploaded_file', filename=filename, data=data_html, data1=data1_html, data2=data2_html,
                        data3=data3_html,data4=data4_html, graph_filename=graph_filename, graph_filename1=graph_filename1,
                        graph_filename2=graph_filename2, graph_filename3=graph_filename3, graph_filename4=graph_filename4, graph_filename5=graph_filename5))

        return render_template('message.html', message="Post, but no file, this shouldnt even show.", redirect_url=request.url)


    return render_template('upload.html')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    data = request.args.get('data')
    data1 = request.args.get('data1')
    data2 = request.args.get('data2')
    data3 = request.args.get('data3')
    data4 = request.args.get('data4')

    graph_filename = request.args.get('graph_filename')
    graph_filename1 = request.args.get('graph_filename1')
    graph_filename2 = request.args.get('graph_filename2')
    graph_filename3 = request.args.get('graph_filename3')
    graph_filename4 = request.args.get('graph_filename4')
    graph_filename5 = request.args.get('graph_filename5')

    return render_template('uploaded.html', filename=filename, data=data,
                           data1=data1, data2=data2, data3=data3,data4=data4, graph_filename=graph_filename,
                           graph_filename1=graph_filename1, graph_filename2=graph_filename2,
                           graph_filename3=graph_filename3, graph_filename4=graph_filename4, graph_filename5=graph_filename5)


if __name__ == '__main__':
    app.run(debug=True)
