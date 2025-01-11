from flask import Flask, request, render_template, redirect, url_for, flash
import os
import re

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Dibutuhkan untuk flash messages

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Pastikan folder uploads ada
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def get_unique_filename(folder, base_filename):
    """
    Menghasilkan nama file unik di folder tertentu.
    Jika file dengan nama base_filename sudah ada, tambahkan angka di akhir.
    """
    base_name, extension = os.path.splitext(base_filename)
    counter = 1
    new_filename = base_filename

    while os.path.exists(os.path.join(folder, new_filename)):
        new_filename = f"{base_name}{counter}{extension}"
        counter += 1

    return new_filename

def extract_user_pass(input_file, output_folder):
    """
    Ekstrak user:pass dari file input dan simpan ke file output dengan nama unik.
    """
    # Tentukan nama file output unik
    output_filename = get_unique_filename(output_folder, 'output.txt')
    output_path = os.path.join(output_folder, output_filename)

    # Membuka file input untuk membaca dengan encoding utf-8
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Membuka file output untuk menulis hasilnya
    with open(output_path, 'w', encoding='utf-8') as f:
        for line in lines:
            parts = re.split(r'[:/ ]+', line.strip())
            if len(parts) >= 2:
                user_pass = parts[-2] + ":" + parts[-1]
                f.write(user_pass + '\n')

    return output_filename  # Kembalikan nama file output

@app.route('/')
def index():
    """
    Halaman utama untuk mengunggah file.
    """
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Endpoint untuk menangani unggahan file.
    """
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file:
        # Simpan file input
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(input_path)

        # Proses file untuk ekstraksi user:pass
        output_filename = extract_user_pass(input_path, app.config['UPLOAD_FOLDER'])

        # Tampilkan pesan sukses dengan nama file
        flash(f'File berhasil diproses! File hasil: {output_filename}. Silakan cek folder uploads.')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=3000)
