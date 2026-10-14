DROP TABLE IF EXISTS plats;
DROP TABLE IF EXISTS reservations;

CREATE TABLE plats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    prix REAL NOT NULL,
    categorie TEXT NOT NULL
);

CREATE TABLE reservations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    telephone TEXT NOT NULL,
    date TEXT NOT NULL,
    personnes INTEGER NOT NULL,
    service TEXT NOT NULL,
    remarques TEXT
);