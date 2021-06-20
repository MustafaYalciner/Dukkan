import json

# http://jsonpickle.github.io/
import jsonpickle
from flask import Flask, request, make_response
from idna import unicode

from GelenBilgiler import GelenBilgiler

import geopy.distance

from Lokasyon import Lokasyon
from Motorcu import Motorcu

app = Flask("Dukkan Uygulamasi")

motorcular = [Motorcu("Ismet007", False, Lokasyon(12, 13)), Motorcu("Fatih88", True, Lokasyon(12, 13))]


@app.route('/')
def index():
    return "Dukkan uygulamasi. 'Advanced REST Client' plugini chrome icin yükleyin ve kullanin"


@app.route('/todo/api/v1.0/motorcular', methods=['GET'])
def get_tasks():
    return jsonpickle.encode(motorcular)


# cevapin json formatinda gelmesi icin özel olarak cevapliyoruz
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonpickle.encode("error, not found"), 404)


@app.route('/todo/api/v1.0/motorcular', methods=['PUT'])
def update_task():
    motorcu = jsonpickle.decode(request.get_data())
    motorcular.append(motorcu)
    return jsonpickle.encode(motorcu)


@app.route('/todo/api/v1.0/motorcular/<string:isim>', methods=['DELETE'])
def delete_motorcu(isim):
    return

@app.route('/todo/api/v1.0/motorcular/<string:isim>', methods=['POST'])
def create_task():
    return

if __name__ == '__main__':
    app.run(debug=True)


