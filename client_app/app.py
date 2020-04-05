# import library yang diperlukan
from flask import Flask, render_template, request
import xmlrpc.client
import json

# inisialisasi server RPC dan flask
server = xmlrpc.client.ServerProxy('http://8ec8ee05.ngrok.io')
app = Flask(__name__)


# mendefinisikan route untuk home
@app.route('/', methods=['post', 'get'])
def home():
    data = []
    n_pesan = 0
    data = json.loads(server.getAll())  # mengambil data dari server
    for user in data:
        if user['status'] == True:
            n_pesan += 1  # menghitung jumlah pesan
    data = {}
    if request.method == 'POST':
        nama = request.form.get('nama')  # mengambil data dari form
        gula_darah = request.form.get('gula_darah')
        # mengirim data ke server
        result = server.controlGula(nama, gula_darah)
        data['status'] = result
    # render html menggunakan data
    return render_template('submit.html', data=data, n_pesan=n_pesan)

# route untuk halaman pesan
@app.route('/messages', methods=['post', 'get'])
def messages():
    data = []
    pesan = []
    n_pesan = 0
    if request.method == 'GET':
        # mengambil data dari server dan decode JSON
        data = json.loads(server.getAll())
        for user in data:
            if user['status'] == True:
                n_pesan += 1  # menghitung pesan
                # dan memasukan ke list untuk ditampilkan di menu pesan
                pesan.append(user)
    return render_template('messages.html', data=data, n_pesan=n_pesan, pesan=pesan)


if __name__ == '__main__':
    app.run(debug=True)
