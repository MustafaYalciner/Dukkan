import socket           # internet protokolü, transfer ve baglanti icin
import threading        # ayni anda fonksyon yürütmek icin

import time             # cogu zaman lazim oluyor, import datetime da olabilir tarih icin
import sys              # programi acip kapatmak icin, programin fonksyonlarini kurcalamak icin
import os               # dosya acip kapatmak icin (mesela: "Kuryerden baglanti girerse kuryer.py programini ac"


# information kayidi ve kullanmak icin gerekli DEGISKENLER
KURYERCILER = []  # Class halinde toplaniyor, Liste üzeri belli KURYER secilebiliyor
DÜKKANLAR = []  # Class halinde toplaniyor, Liste üzeri belli DÜKKAN secilebiliyor
total_connections = 0  # toplam baglantilar

KURYERICLER_YENI = {"hamm_herringen": [KURYERCI_1, KURYERCI_2],
                    "Hamm_pelkum": []}


DÜKKANLAR_BILGI = {}
KURYERCILER_BIULGI = {}


# Kuryerci class, her KURYERCI icin yeni bir örnek
# Her örnek in socket'i ve adresi ile iliskili maddeleri var
# Atanmış bir kimlik ve müşteri tarafından seçilen bir adla birlikte
# Send KURYERCI data to DÜKKANLAR
class Kuryerci(threading.Thread):
    def __init__(self, socket, address, id, name, signal):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.id = id
        self.name = name
        self.signal = signal

        #
        # self.cevre = cevre

    def __str__(self):
        return str(self.id) + " " + str(self.address)

    # KURYERCIDEN Data alma deneyi
    # Mesaj alinamiyorsa, KURYERCI baaglantiyi kesti diye kabullen   !!!YANLIS OLABILIR!!!
    # If able to and we get data back, print it in the server and send it back to the same client
    def run(self):
        num_price = -1
        num_client = -1
        while self.signal:
            try:

                # KURYERCI DATA yolladiyasa, bunu kabul et. KURYECININ DATASI: location, QR-CODE (Dükkana vardim), vs...
                data = self.socket.recv(70)
            except:
                # KURYERCI DATA yollamadiysa KURYERCILER listesinden KURYERCI'yi sil
                print("KURYERCI " + str(self.address) + " has disconnected")
                self.signal = False
                KURYERCILER.remove(self)
                break
            num_price += 1
            # print("ID " + str(self.id) + ": " + str(data.decode("utf-8")))
            KURYERCILER.append([data.decode("utf-8")])

            # KURYERCI "XYZ" YAPTIYSA (KURYECI'nin DÜKKAN'a yollicagi DATA var ise)
            DÜKKANLAR[0].socket.sendall(data)

            """elif self.address[0] == "127.0.0.1":
                num_client+= 1
                PRICE_LIST.append([data.decode("utf-8")])
                # send data to CLIENT[num]
                KURYERCILER[0].socket.sendall(data)"""


# Kuryerci Class'in DÜKKAN tarafi, asagi yukari ayni olcak. Handi DATA yollanicak o bize bagli (mesela "Ev adresi")
class Dükkan(threading.Thread):
    def __init__(self, socket, address, id, name, signal):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.id = id
        self.name = name
        self.signal = signal

    def __str__(self):
        return str(self.id) + " " + str(self.address)

    def run(self):
        global KURYERCILER
        while self.signal:
            try:
                # DIKKAT: DÜKKANCI KOD TARAFINA
                # import datetime üzeri dükkan BUTTON basarsa, tarih ve saat ve asagidaki informationlari yolla
                # Hem Servere, hemde KURYERCIYE

                # Kuryerci BUTTON a basarsa, ve GEO-LOCATION Müsteri adresinin belli bir cevresinde ise, SIPARISI onayla


                # lokasyonda hata varsa nolcak?

                """
                1. Musteri adi, soy adi
                2. Tel. Numarasi
                3. Adres (sokak falan)
                4. Siparis iceriligi (fiyat)
                5. 
                
                """

                data = self.socket.recv(90)
            except:
                print("KURYERCI " + str(self.address) + " has disconnected")
                self.signal = False
                KURYERCILER.remove(self)
                break
            if data != "":
                print("DÜKKAN" + str(self.id) + ": " + str(data.decode("utf-8")))

                """
                
                
                """


                KURYERCILER[0].socket.sendall(data)
            """for kuryerci in KURYERCILER:
                if kuryerci.address == self.address:
                    kuryerci.socket.sendall(data)"""


# Baglanti geliyor mu diye sonsuza dek bekle
def yeniBaglantilar(socket):
    num = -1
    while True:

        # gelen baglantiyi kabul et
        sock, address = socket.accept()

        num += 1  # only because i couldnt find another local up for client.py
        global total_connections
        print(address)

        # Baglanti KURYECI den ise
        # KURYECILER Listesine "Kuryeci(sock, addressm total_connections, "Name", True)" ekle
        # SORUN: SERVER KURYERCI VE DÜKKANLARI KARISTIRMAMASI LAZIM. (Her Kuryercinin ve Dükkanin özel ismi lazim, ve bu isime göre "name" yerini degistiririz.
        # bu listeler önemli ve güzel organizasyonu gerek!!!!!!!!!!!!!!!!!!!!!
        if address[
            0] != 'kuryeciadresi' and num != 0:  # böyle degistirmemiz gerek => if address[0] in KURYERCILER, cünkü kuryerciler listesi büyük olcak. Kuryerciden baglanti geldi ise, hangi kuryer olduna bak ve sonra O kuryere Göre Class ac

            # Kuryer Class'ini calistir
            KURYERCILER.append(Kuryerci(sock, address, total_connections, "Name", True))
            KURYERCILER[len(KURYERCILER) - 1].start()
            print("New connection | KURYER " + str(KURYERCILER[len(KURYERCILER) - 1]))
            total_connections += 1
            client_ip = address[0]

        # Baglanti DÜKKAN dan ise
        # DÜKKANLAR Listesine Dükkanlar(sock, address, total_connections, "Name", True) ekle
        # yukaridaki ayni sorun
        else:  # suanki hali sadece bir dükkan icin. Cogul gerek.
            print("New connection | DÜKKAN")
            DÜKKANLAR.append(Dükkan(sock, address, total_connections, "Name", True))
            DÜKKANLAR[len(DÜKKANLAR) - 1].start()
            price_ip = address[0]
            print(price_ip)
            # return price_ip


# Serveri kur ve interneti dinle (dinle <=> baglanti ara, baglanmak istiyen var mi diye bak)
def main():
    # host ve port kur
    host = ""  # "" <=> her gelen IP-Adresi kabul et
    port = 7979

    # Create new server socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(5)

    # Yeni Thread kur ve "yeniBaglantilar" fonksyonunu ac
    newConnectionsThread = threading.Thread(target=yeniBaglantilar, args=(sock,))
    newConnectionsThread.start()


# main fonksoynunu ac
main()
