from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/convert')
def convert():
    return render_template('convert.html')

@app.route('/done')
def done():
    return render_template('done.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

app.run(port=3000, debug=True)