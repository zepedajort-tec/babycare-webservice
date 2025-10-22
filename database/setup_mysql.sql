-- Crear base de datos
CREATE DATABASE IF NOT EXISTS babycare CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE babycare;

-- ===========================================
-- TABLAS
-- ===========================================
CREATE TABLE IF NOT EXISTS baby_profiles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age_months INT NOT NULL,
    weight FLOAT,
    height FLOAT
    );

CREATE TABLE IF NOT EXISTS parents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20),
    relation VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS health_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    baby_id INT,
    date DATE,
    vaccine VARCHAR(100),
    notes TEXT,
    FOREIGN KEY (baby_id) REFERENCES baby_profiles(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS development_tips (
    id INT AUTO_INCREMENT PRIMARY KEY,
    age_range VARCHAR(50),
    category VARCHAR(50),
    tip_text TEXT
);

-- ===========================================
-- PROCEDIMIENTOS ALMACENADOS CRUD
-- ===========================================

-- ========================
-- BABY_PROFILES
-- ========================
DELIMITER $$

CREATE PROCEDURE sp_create_baby(IN p_name VARCHAR(100), IN p_age INT, IN p_weight FLOAT, IN p_height FLOAT)
BEGIN
INSERT INTO baby_profiles (name, age_months, weight, height)
VALUES (p_name, p_age, p_weight, p_height);
END$$

CREATE PROCEDURE sp_read_baby(IN p_id INT)
BEGIN
SELECT * FROM baby_profiles as bp where bp.id = p_id;
END$$

CREATE PROCEDURE sp_read_babies()
BEGIN
SELECT * FROM baby_profiles;
END$$

CREATE PROCEDURE sp_update_baby(IN p_id INT, IN p_name VARCHAR(100), IN p_age INT, IN p_weight FLOAT, IN p_height FLOAT)
BEGIN
UPDATE baby_profiles
SET name = p_name, age_months = p_age, weight = p_weight, height = p_height
WHERE id = p_id;
END$$

CREATE PROCEDURE sp_delete_baby(IN p_id INT)
BEGIN
DELETE FROM baby_profiles WHERE id = p_id;
END$$

-- ========================
-- PARENTS
-- ========================
CREATE PROCEDURE sp_create_parent(IN p_name VARCHAR(100), IN p_email VARCHAR(100), IN p_phone VARCHAR(20), IN p_relation VARCHAR(50))
BEGIN
INSERT INTO parents (name, email, phone, relation)
VALUES (p_name, p_email, p_phone, p_relation);
END$$

CREATE PROCEDURE sp_read_parents()
BEGIN
SELECT * FROM parents;
END$$

CREATE PROCEDURE sp_update_parent(IN p_id INT, IN p_name VARCHAR(100), IN p_email VARCHAR(100), IN p_phone VARCHAR(20), IN p_relation VARCHAR(50))
BEGIN
UPDATE parents
SET name = p_name, email = p_email, phone = p_phone, relation = p_relation
WHERE id = p_id;
END$$

CREATE PROCEDURE sp_delete_parent(IN p_id INT)
BEGIN
DELETE FROM parents WHERE id = p_id;
END$$

-- ========================
-- HEALTH_RECORDS
-- ========================
CREATE PROCEDURE sp_create_health(IN p_baby_id INT, IN p_date DATE, IN p_vaccine VARCHAR(100), IN p_notes TEXT)
BEGIN
INSERT INTO health_records (baby_id, date, vaccine, notes)
VALUES (p_baby_id, p_date, p_vaccine, p_notes);
END$$

CREATE PROCEDURE sp_read_health()
BEGIN
SELECT h.*, b.name AS baby_name
FROM health_records h
         JOIN baby_profiles b ON b.id = h.baby_id;
END$$

CREATE PROCEDURE sp_update_health(IN p_id INT, IN p_date DATE, IN p_vaccine VARCHAR(100), IN p_notes TEXT)
BEGIN
UPDATE health_records
SET date = p_date, vaccine = p_vaccine, notes = p_notes
WHERE id = p_id;
END$$

CREATE PROCEDURE sp_delete_health(IN p_id INT)
BEGIN
DELETE FROM health_records WHERE id = p_id;
END$$

-- ========================
-- DEVELOPMENT_TIPS
-- ========================
CREATE PROCEDURE sp_create_tip(IN p_age_range VARCHAR(50), IN p_category VARCHAR(50), IN p_tip_text TEXT)
BEGIN
INSERT INTO development_tips (age_range, category, tip_text)
VALUES (p_age_range, p_category, p_tip_text);
END$$

CREATE PROCEDURE sp_read_tips()
BEGIN
SELECT * FROM development_tips;
END$$

CREATE PROCEDURE sp_update_tip(IN p_id INT, IN p_age_range VARCHAR(50), IN p_category VARCHAR(50), IN p_tip_text TEXT)
BEGIN
UPDATE development_tips
SET age_range = p_age_range, category = p_category, tip_text = p_tip_text
WHERE id = p_id;
END$$

CREATE PROCEDURE sp_delete_tip(IN p_id INT)
BEGIN
DELETE FROM development_tips WHERE id = p_id;
END$$

DELIMITER ;

-- ===========================================
-- FIN DEL SCRIPT
-- ===========================================
