import json

# http://jsonpickle.github.io/
import jsonpickle
from flask import Flask, request, make_response, session

from Lokasyon import Lokasyon
from Motorcu import Motorcu
from Dukkan import Dukkan
from Siparis import Siparis
from VeriTabaninaYazar import VeriTabaninaYazar

app = Flask("Dukkan Uygulamasi")

motorcular = [Motorcu("Ismet007", False, Lokasyon(12, 13)), Motorcu("Fatih88", True, Lokasyon(12, 13))]

# dükkanlar class olustur mustafa kafanı kırar;


Dukkanlar = [Dukkan("Pasa Doner",True,Lokasyon(11,14)),Dukkan("Firin Sanati",False,Lokasyon(9,15))]

siparisler=[Siparis("ismet","cetin",Lokasyon(11,11),"tavukdurum")]

# ________ YENI _______________________________________________________________________

dukkanlar_dict = {}
dukkanlar_dict_class = {}


@app.route('/todo/api/v1.0/dukkan/<dukkan_user>', methods=['POST'])
def dukkan_login(dukkan_user):
    # session.clear()
    # location, availability
    login_data = jsonpickle.encode(request.get_data())

    session[dukkan_user] = []
    dukkanlar_dict[dukkan_user] = []

    # dukkanlar_dict_class[dukkan_user] = []

    # aslinda session kurduk, ve dukkan offline olursa session de kaniyor. Ama daha tam emin olmadigimdan ve REST CLIENT sadece string yolladigindan
    def boolean_converter(bool):
        if bool == "1" or "True" or "true" or "TRUE":
            return True
        else:
            return False

    # class topla
    yeni_dukkan_class = Dukkan(dukkan_user, boolean_converter(login_data[1]), Lokasyon(login_data[2][0], login_data[2][2]))

    dukkanlar_dict_class[yeni_dukkan_class] = []

    print(f"sessions: {session}, classes: {dukkanlar_dict_class}, storage: {dukkanlar_dict}")

    return dukkanlar_dict, dukkanlar_dict_class


@app.route('/todo/api/v1.0/dukkan/<dukkan_user>/siparis', methods=['PUT'])
def dukkan_siparis(dukkan_user):
    siparis_data = jsonpickle.decode(request.get_data())
    print(siparis_data)
    """
    if dukkan_user in session:
        print("hallo")
    else:
        print("bye")
    """

    if dukkan_user in dukkanlar_dict:
        dukkanlar_dict[dukkan_user].append(siparis_data)
        # dukkanlar_dict_class[Dukkan(dukkan_user, True)].append(Siparis(siparis_data[0], Lokasyon(siparis_data[1][0], siparis_data[1][2]), siparis_data[2]))
    else:
        pass

    print(dukkanlar_dict)
    print(dukkanlar_dict_class)

    return dukkanlar_dict


# REST CLIENTE BUNU YAZ:

"""
1. Method: POST - url: http://127.0.0.1:5000/todo/api/v1.0/dukkan/farketmezistediginiyaz
                        body: ["farketmezistediginiyaz", "true", "1,2"]

2. Method PUT - url    http://127.0.0.1:5000/todo/api/v1.0/dukkan/farketmezistediginiyaz/siparis
                  body:     ["Fatih Senguel", "2,3", "Adana ve Cola"]


sonra dukkan ismini degistir veya yeni siparis ver

"""


# ________________________________________________________________________________________________________________



@app.route('/todo/api/v1.0/siparisler', methods=['PUT'])
def update_siparisler():
    Siparis = jsonpickle.decode(request.get_data())
    siparisler.append(Siparis)
    return jsonpickle.encode(Dukkan)
@app.route('/todo/api/v1.0/siparisler', methods=['GET'])
def get_siparisler():
    return jsonpickle.encode(siparisler)

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
    veriTabaninaYazar = VeriTabaninaYazar()
    veriTabaninaYazar.dukkani_kayit_et(Dukkan("Pasa Doner",True,Lokasyon(11,14)))
    app.run(debug=True)


