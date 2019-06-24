from __future__ import unicode_literals
from flask import Flask, render_template, request, send_file
import youtube_dl
import os

from config import MP3_DIRECTORY

app = Flask(__name__)

if not os.path.exists(MP3_DIRECTORY):
    os.makedirs(MP3_DIRECTORY)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/convert', methods=['POST'])
def convert():
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': './MP3/%(title)s.%(ext)s',
        'forcefilename': 'True',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        url = request.form['url']
        info_dict = ydl.extract_info(url)
        fn = ydl.prepare_filename(info_dict).replace('webm', 'mp3')[6:]
        ydl.download([url])
    return render_template('done.html', download_path=fn)

@app.route('/done')
def done():
    return render_template('done.html')

@app.route('/download/<download_path>')
def download(download_path = None):
   return send_file(MP3_DIRECTORY+'/'+download_path, as_attachment=True)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

app.run(port=3000, debug=True)