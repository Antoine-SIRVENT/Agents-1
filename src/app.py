from flask import Flask, render_template, request
from nltosql.crew import Nltosql

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        try:
            result = Nltosql().crew().kickoff(inputs={'query': query})
            return render_template('index.html', result=result, query=query)
        except Exception as e:
            error = str(e)
            return render_template('index.html', error=error)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

