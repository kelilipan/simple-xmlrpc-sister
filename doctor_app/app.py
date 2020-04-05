# Import library yang diperlukan
from flask import Flask, render_template, request, redirect
import xmlrpc.client
import json

# Inisialisasi flask dan konek ke server rpc
server = xmlrpc.client.ServerProxy('http://8ec8ee05.ngrok.io')
app = Flask(__name__)


# Membuat route untuk homepage
@app.route('/', methods=['post', 'get'])
def home():  # fungsi home
    result = server.getAll()  # mengambil data dari fungsi server
    data = json.loads(result)  # decode dari json ke python
    return render_template('index.html', data=data)


@app.route('/send', methods=['post', 'get'])
def send():  # fungsi send pesan
    if request.method == 'POST':
        id = int(request.form.get('id'))  # mengambil data dari form html
        pesan = request.form.get('pesan')  # mengambil data dari form html
        server.sendMessage(id, pesan)  # mengirim pesan ke server
    # return render_template('index.html', data=data)
    return redirect('http://127.0.0.1:5000/', code=200)


if __name__ == '__main__':
    app.run(debug=True)
