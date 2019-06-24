from __future__ import unicode_literals
from flask import Flask, render_template, request
import youtube_dl

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/convert', methods=['POST'])
def convert():
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([request.form['url']])
    return render_template('done.html')

@app.route('/done')
def done():
    return render_template('done.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

app.run(port=3000, debug=True)