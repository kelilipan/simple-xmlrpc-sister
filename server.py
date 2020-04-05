# import library yang dibutuhkan
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import json

# Batasi hanya pada path /RPC2 saja supaya tidak bisa mengakses path lainnya


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


# Buat server
with SimpleXMLRPCServer(("localhost", 80),
                        requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    # membuat database untuk menerima inputan
    db = []
    # batas normal kadar gula darah
    threshold = 100

    # fungsi menentukan pasien sakit atau tidak
    def controlGula(nama, gula_darah):
        # inisialisasi data
        data = {
            'id': len(db)+1,
            'nama': nama,
            'gula_darah': int(gula_darah),
            'status': False,
            'danger': False,
            'pesan': ''
        }
        result = 'Sehat'
        if data['gula_darah'] > threshold:
            data['danger'] = True
            result = 'Sakit'
        db.append(data)
        return result
    server.register_function(controlGula)  # meregister fungsi ke fungsi server

    # fungsi untuk mengambil semua data di database
    def getAll():
        data = json.dumps(db)  # encoding data ke json
        return data
    server.register_function(getAll)  # meregister fungsi ke fungsi server

    # fungsi send message untuk dokter ke pasien
    def sendMessage(id, pesan):
        try:
            # pesan yang diinput oleh dokter akan di assign ke database
            db[id-1]['pesan'] = pesan
            # jika pesan sudah dikirim maka dokter sudah tidak mengirim pesan lagi
            db[id-1]['status'] = True
            return 'Success!'
        except:
            return False

    server.register_function(sendMessage)  # meregister fungsi ke fungsi server

    print("Server Aplikasi dokter berjalan...")
    # Run the server's main loop
    server.serve_forever()
