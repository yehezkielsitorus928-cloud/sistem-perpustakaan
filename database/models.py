from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Petugas(db.Model):
    id_petugas = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(255))

class Buku(db.Model):
    isbn = db.Column(db.String(20), primary_key=True)
    judul = db.Column(db.String(255))
    penulis = db.Column(db.String(100))
    stok = db.Column(db.Integer, default=0)

class Anggota(db.Model):
    nim = db.Column(db.String(15), primary_key=True)
    nama = db.Column(db.String(100))
    prodi = db.Column(db.String(50))

class Peminjaman(db.Model):
    id_pinjam = db.Column(db.Integer, primary_key=True)
    id_anggota = db.Column(db.String(15))
    isbn = db.Column(db.String(20))
    tgl_pinjam = db.Column(db.DateTime, default=datetime.now)
    tgl_tenggat = db.Column(db.DateTime)
    tgl_kembali = db.Column(db.DateTime, nullable=True)
    denda = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='Dipinjam')

    def __init__(self, **kwargs):
        super(Peminjaman, self).__init__(**kwargs)
        if not self.tgl_tenggat:
            self.tgl_tenggat = datetime.now() + timedelta(days=7)