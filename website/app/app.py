from flask import Flask, send_file, render_template, request, abort
from prometheus_flask_exporter import PrometheusMetrics

import logging
import time
import os
import yaml

os.environ['TZ'] = "Europe/Berlin"
time.tzset()


logging.basicConfig(
    filename='logs/flask.log',
    encoding='utf-8',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s'
    )

with open("config/cameras.yaml", "r") as yamlfile:
    config = yaml.load(yamlfile, Loader=yaml.FullLoader)
    print("camera config read successful")
#print(yaml)

app = Flask(__name__) 

metrics = PrometheusMetrics(app)

metrics.info('app_info', 'Application info', version='1.0.3')

#@app.errorhandler(500)
#def internal_error(error):
#
#    return "500 error"

@app.errorhandler(404)
def not_found(error):
    filename = 'static/404.jpg'
    return send_file(filename, mimetype='image/jpg'), 404

@app.route('/error',methods = ['POST', 'GET'])
def errorTest():
    abort(500)

@app.route('/',methods = ['POST', 'GET'])
def index():
    return render_template('index.html', config=config)

#@app.route('/BirdStalker')
#def get_image():
#    filename = 'static/BirdStalker.jpg'
#    return send_file(filename, mimetype='image/jpg')



# main driver function
if __name__ == '__main__':
    app.run()

