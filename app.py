import os, json

from flask import Flask, flash, request, render_template, send_file
import landfireCurl

app = Flask(__name__)

def _tifFileFormat(name):
    if '.tif' not in name:
        name = name.split('.')[0] + '.tif'

    return name

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/request-builder')
def my_form():
    return render_template('input-form.html')

"""
RUN-FDS ENDPOINT (GET/POST)
    Generate and run an FDS simulation with specified conditions. Uses LANDFIRE CONUS data.
    Query Parameters:
        latitude
            - latitude coordinate for center of simulation domain. must be within CONUS.
        longitude
            - longitude coordinate for center of simulation domain must be within CONUS.
        resolution (max=30 ???)
            - the resolution for queried data in meters.
        extent (min=5, max=60)
            - the area for the simulation domain in miles. (centered at the lat/long coordinates provided)
        x1_fire, y1_fire, x2_fire, y2_fire
            - ???
        run (true/false)
            - if "true", query triggers an FDS simulation and returns the input file & output upon completion. 
            - if "false", query returns only the generated FDS input file.
"""
@app.route('/run-fds', methods=['GET', 'POST'])
def run_fds():
    if request.method == "POST":
        if (request.form['run'] == "true"):
            run_sim = True
        else: 
            run_sim = False

        fds = landfireCurl.backend(
            _tifFileFormat(request.form['name']),
            request.form['latitude'],
            request.form['longitude'],
            resolution=request.form['resolution'],
            size=request.form['extent'],
            fire_points=[
                [request.form['x1_fire'],request.form['y1_fire']],
                [request.form['x2_fire'],request.form['y2_fire']]],
            run_sim=run_sim)

        fds.makeGeo(request.form['time'])
        cFileName=os.path.join('data/',fds.fdsRun())

    else:
        if (request.args.get('run') == "true"):
            run_sim = True
        else:
            run_sim = False

        fds = landfireCurl.backend(
            _tifFileFormat(request.args.get('name')),
            request.args.get('latitude'),
            request.args.get('longitude'),
            resolution=request.args.get('resolution'),
            size=request.args.get('extent'),
            fire_points=[
                [request.args.get('x1_fire'),request.args.get('y1_fire')],
                [request.args.get('x2_fire'),request.args.get('y2_fire')]],
            run_sim=run_sim)

        fds.makeGeo(request.args.get('time'))
        cFileName=os.path.join('data/',fds.fdsRun())

    return send_file(cFileName, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')