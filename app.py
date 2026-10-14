import sqlite3
import os
import re
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

app = Flask(__name__)
app.secret_key = "secret_flask_restaurant"

def get_db():
    conn = sqlite3.connect('instance/restaurant.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    os.makedirs('instance', exist_ok=True)
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        
        # Insertion de tous les plats (y compris le poisson braisé)
        plats_init = [
            ('Salade tropicale', 3500, 'entree'),
            ('Beignets de plantain', 2000, 'entree'),
            ('Poulet DG', 8500, 'plat'),
            ('Ndolé royal', 7000, 'plat'),
            ('Poisson braisé', 9000, 'plat'),
            ('Jus de Bissap', 1000, 'boisson'),
            ('Eau minérale', 500, 'boisson')
        ]
        db.executemany("INSERT INTO plats (nom, prix, categorie) VALUES (?, ?, ?)", plats_init)
        db.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/reserver', methods=['GET', 'POST'])
def reserver():
    if request.method == 'POST':
        nom = request.form.get('nom', '').strip()
        telephone = request.form.get('telephone', '').strip().replace(' ', '')
        date = request.form.get('date', '').strip()
        personnes = request.form.get('personnes', '').strip()
        service = request.form.get('service', 'midi').strip()
        remarques = request.form.get('remarques', '').strip()

        erreurs = []
        if not nom: erreurs.append("Le nom est obligatoire.")
        if not re.match(r'^6\d{8}$', telephone): erreurs.append("Téléphone invalide (9 chiffres commençant par 6).")

        try:
            nb_p = int(personnes)
            if not (1 <= nb_p <= 20): raise ValueError()
        except ValueError:
            erreurs.append("Nombre de personnes entre 1 et 20 requis.")

        try:
            date_res = datetime.strptime(date, '%Y-%m-%d').date()
            if date_res < datetime.now().date(): erreurs.append("La date ne peut pas être dans le passé.")
        except ValueError:
            erreurs.append("Date invalide.")

        if erreurs:
            for err in erreurs: flash(err, 'danger')
            return render_template('reserver.html')

        db = get_db()
        db.execute(
            'INSERT INTO reservations (nom, telephone, date, personnes, service, remarques) VALUES (?, ?, ?, ?, ?, ?)',
            (nom, telephone, date, nb_p, service, remarques)
        )
        db.commit()
        flash('Réservation enregistrée avec succès !', 'success')
        return redirect(url_for('lister_reservations'))

    return render_template('reserver.html')

@app.route('/reservations', methods=['GET', 'POST'])
def lister_reservations():
    db = get_db()
    if request.method == 'POST':
        res_id = request.form.get('id')
        db.execute('DELETE FROM reservations WHERE id = ?', (res_id,))
        db.commit()
        flash('Réservation annulée.', 'info')
        return redirect(url_for('lister_reservations'))

    reservations = db.execute('SELECT * FROM reservations ORDER BY date ASC').fetchall()
    return render_template('reservations.html', reservations=reservations)

@app.route('/api/menu')
def api_menu():
    db = get_db()
    plats = db.execute('SELECT nom, prix, categorie FROM plats').fetchall()
    return jsonify([dict(plat) for plat in plats])

if __name__ == '__main__':
    # Initialise ou réinitialise la base proprement si elle n'a pas les tables
    with app.app_context():
        db = get_db()
        tables = db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='reservations'").fetchone()
        if not tables:
            init_db()
    app.run(debug=True)