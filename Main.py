import json

# http://jsonpickle.github.io/
import jsonpickle
from flask import Flask, request, make_response

from Lokasyon import Lokasyon
from Motorcu import Motorcu
from Dukkan import Dukkan
app = Flask("Dukkan Uygulamasi")

motorcular = [Motorcu("Ismet007", False, Lokasyon(12, 13)), Motorcu("Fatih88", True, Lokasyon(12, 13))]

# dükkanlar class olustur mustafa kafanı kırar;


Dukkanlar = [Dukkan("Pasa Doner",True,Lokasyon(11,14)),Dukkan("Firin Sanati",False,Lokasyon(9,15))]

@app.route('/todo/api/v1.0/dukkanlar', methods=['PUT'])
def update_dukkanlar():
    Dukkan = jsonpickle.decode(request.get_data())
    Dukkanlar.append(Dukkan)
    return jsonpickle.encode(Dukkan)
@app.route('/todo/api/v1.0/dukkanlar', methods=['GET'])
def get_tasks():
    return jsonpickle.encode(Dukkanlar)

@app.route('/')
def index():
    return "Dukkan uygulamasi. 'Advanced REST Client' plugini chrome icin yükleyin ve kullanin"


@app.route('/todo/api/v1.0/isver/<isim>', methods=['GET'])
def get_is(isim):
    return jsonpickle.encode(isim)



@app.route('/todo/api/v1.0/motorcular', methods=['GET'])
def get_motorcular():
    return jsonpickle.encode(motorcular)


@app.route('/todo/api/v1.0/motorcular', methods=['PUT'])
def update_task():
    motorcu = jsonpickle.decode(request.get_data())
    motorcular.append(motorcu)
    return jsonpickle.encode(motorcu)


# cevapin json formatinda gelmesi icin özel olarak cevapliyoruz
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonpickle.encode("error, not found"), 404)



@app.route('/todo/api/v1.0/motorcular/<string:isim>', methods=['DELETE'])
def delete_motorcu(isim):
    return

@app.route('/todo/api/v1.0/motorcular/<string:isim>', methods=['POST'])
def create_task():
    return

if __name__ == '__main__':
    app.run(debug=True)


