from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import base64
import os

app = Flask(__name__)
app.secret_key = 'informatika'

# Fungsi untuk memuat kunci dari file
def load_key():
    return open("secret.key", "rb").read()

key = load_key()


def encrypt(data, key):
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data) + padder.finalize()
    iv = os.urandom(12) 
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    encrypted_data = iv + encryptor.tag + ciphertext
    return base64.b64encode(encrypted_data).decode('utf-8')

# Fungsi untuk mendekripsi data
def decrypt(encrypted_data, key):
    # Decode dari base64
    encrypted_data = base64.b64decode(encrypted_data)
    
    # Ekstrak iv, tag, dan ciphertext
    iv = encrypted_data[:12]
    tag = encrypted_data[12:28]
    ciphertext = encrypted_data[28:]
    
    # Buat cipher
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    
    # Dekripsi data
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()
    
    # Unpad data
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    
    return data

# Koneksi database
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='1234',
        database='dna_database'
    )

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM users WHERE username=%s AND password=%s"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    
    if user:
        session['user_id'] = user['id']
        session['role'] = user['role']
        
        if user['role'] == 'researcher':
            return redirect(url_for('input_data'))
        else:
            return redirect(url_for('view_data'))
    else:
        flash('Invalid username or password')
        return redirect(url_for('login'))

@app.route('/input_data')
def input_data():
    if 'role' in session and session['role'] == 'researcher':
        return render_template('input_data.html')
    else:
        return redirect(url_for('login'))

@app.route('/submit_data', methods=['POST'])
def submit_data():
    if 'role' in session and session['role'] == 'researcher':
        name = request.form['name']
        dna_sequence = request.form['dna_sequence']
        encrypted_dna = encrypt(dna_sequence.encode(), key)
        
        db = get_db_connection()
        cursor = db.cursor()
        query = "INSERT INTO dna_data (name, dna_sequence) VALUES (%s, %s)"
        cursor.execute(query, (name, encrypted_dna))
        db.commit()
        
        flash('Data berhasil diinput')
        return redirect(url_for('input_data'))
    else:
        return redirect(url_for('login'))

@app.route('/view_data')
def view_data():
    if 'role' in session and session['role'] == 'user':
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM dna_data")
        dna_data = cursor.fetchall()
        
        decrypted_data = []
        for data in dna_data:
            try:
                decrypted_dna = decrypt(data['dna_sequence'], key).decode()
                decrypted_data.append({
                    'id': data['id'],
                    'name': data['name'],
                    'dna_sequence': decrypted_dna
                })
            except Exception as e:
                flash('Failed to decrypt data: {}'.format(e))
        
        return render_template('view_data.html', dna_data=decrypted_data)
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    flash('Anda berhasil logout')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
