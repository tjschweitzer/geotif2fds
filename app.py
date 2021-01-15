import os

from flask import Flask, flash, request, render_template,send_file
import landfireCurl


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/request')
def my_form():
    return render_template('input-form.html')

@app.route('/request', methods=['POST'])
def my_form_post():



    name = request.form['name']
    if ".tif" not in name:
        name = name.split('.')[0]+'.tif'
    longitude = request.form['longitude']
    latitude = request.form['latitude']
    resolution = request.form['resolution']
    extent = request.form['extent']
    time = request.form['time']
    x1_fire = request.form['x1_fire']
    y1_fire = request.form['y1_fire']
    x2_fire = request.form['x2_fire']
    y2_fire = request.form['y2_fire']
    fds = landfireCurl.backend(name,latitude,longitude,resolution=resolution,size=extent,fire_points=[[x1_fire,y1_fire],[x2_fire,y2_fire]])
    fds.makeGeo(time)
    cFileName=os.path.join('data/',fds.fdsRun())

    return send_file(cFileName, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')