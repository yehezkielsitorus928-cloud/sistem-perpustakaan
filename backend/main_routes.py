from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database.models import db, Petugas, Buku, Anggota, Peminjaman

# Konfigurasi Blueprint dengan menunjuk folder template frontend
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def katalog():
    buku = Buku.query.all()
    return render_template('katalog.html', buku=buku)

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = Petugas.query.filter_by(username=request.form['user'], password=request.form['pass']).first()
        if user:
            session['user'] = user.username
            return redirect(url_for('main.admin'))
        flash('Username atau password salah!', 'danger')
    return render_template('login.html')

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        db.session.add(Petugas(username=request.form['user'], password=request.form['pass']))
        db.session.commit()
        return redirect(url_for('main.login'))
    return render_template('register.html')

@main_bp.route('/admin')
def admin():
    if 'user' not in session: 
        return redirect(url_for('main.login'))
    
    buku = Buku.query.all()
    mhs = Anggota.query.all()
    pinjam = Peminjaman.query.order_by(Peminjaman.id_pinjam.desc()).all()
    
    return render_template('admin.html', buku=buku, mhs=mhs, pinjam=pinjam)

@main_bp.route('/tambah_buku', methods=['POST'])
def tambah_buku():
    db.session.add(Buku(isbn=request.form['isbn'], judul=request.form['judul'], penulis=request.form['penulis'], stok=request.form['stok']))
    db.session.commit()
    return redirect(url_for('main.admin'))

@main_bp.route('/tambah_mhs', methods=['POST'])
def tambah_mhs():
    db.session.add(Anggota(nim=request.form['nim'], nama=request.form['nama'], prodi=request.form['prodi']))
    db.session.commit()
    return redirect(url_for('main.admin'))

@main_bp.route('/pinjam', methods=['POST'])
def pinjam():
    nim = request.form['nim'].strip()
    isbn = request.form['isbn'].strip()
    
    mhs = Anggota.query.get(nim)
    buku = Buku.query.get(isbn)
    
    if mhs and buku and buku.stok > 0:
        db.session.add(Peminjaman(id_anggota=mhs.nim, isbn=buku.isbn))
        buku.stok -= 1
        db.session.commit()
    return redirect(url_for('main.admin'))

@main_bp.route('/kembali/<int:id_pinjam>')
def kembali(id_pinjam):
    p = Peminjaman.query.get(id_pinjam)
    if p and p.status == 'Dipinjam':
        p.tgl_kembali = datetime.now()
        p.status = 'Kembali'
        if p.tgl_kembali > p.tgl_tenggat:
            p.denda = (p.tgl_kembali - p.tgl_tenggat).days * 1000
        b = Buku.query.get(p.isbn)
        if b: b.stok += 1
        db.session.commit()
    return redirect(url_for('main.admin'))

@main_bp.route('/hapus_buku/<isbn>')
def hapus_buku(isbn):
    buku = Buku.query.get(isbn)
    if buku:
        db.session.delete(buku)
        db.session.commit()
    return redirect(url_for('main.admin'))

@main_bp.route('/hapus_mhs/<nim>')
def hapus_mhs(nim):
    mhs = Anggota.query.get(nim)
    if mhs:
        db.session.delete(mhs)
        db.session.commit()
    return redirect(url_for('main.admin'))

@main_bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('main.login'))