from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/all')
def fetch_all():
    return render_template('all.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5051)