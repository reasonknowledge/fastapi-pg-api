-- Structure de la base de données pour FastAPI PostgreSQL API
-- Database: fastapisqlmodelpostgres (ou school_db si Docker)

-- Table des administrateurs
CREATE TABLE IF NOT EXISTS admin (
    id VARCHAR(36) PRIMARY KEY,
    nom VARCHAR(50) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(10) DEFAULT 'admin',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index sur l'email pour recherche rapide
CREATE INDEX IF NOT EXISTS idx_admin_email ON admin(email);

-- Table des étudiants
CREATE TABLE IF NOT EXISTS student (
    id VARCHAR(36) PRIMARY KEY,
    nom VARCHAR(50) NOT NULL,
    prenom VARCHAR(50) NOT NULL,
    filiere VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    annee DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index sur l'email pour recherche rapide
CREATE INDEX IF NOT EXISTS idx_student_email ON student(email);

-- Trigger pour mettre à jour automatiquement updated_at (PostgreSQL)
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger pour la table admin
DROP TRIGGER IF EXISTS update_admin_updated_at ON admin;
CREATE TRIGGER update_admin_updated_at
    BEFORE UPDATE ON admin
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger pour la table student
DROP TRIGGER IF EXISTS update_student_updated_at ON student;
CREATE TRIGGER update_student_updated_at
    BEFORE UPDATE ON student
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Note: SQLModel gère automatiquement la création des tables
-- Ce fichier est fourni à titre de référence pour la structure
-- ou pour une création manuelle si nécessaire
