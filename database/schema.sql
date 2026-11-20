BEGIN;

DROP TABLE IF EXISTS videos CASCADE;
DROP TABLE IF EXISTS images CASCADE;
DROP TABLE IF EXISTS articles CASCADE;
DROP TABLE IF EXISTS spices CASCADE;
DROP TABLE IF EXISTS categories CASCADE;

-- Категории специй
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT
);

-- Основная таблица специй
CREATE TABLE spices (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    slug VARCHAR(120) NOT NULL UNIQUE,
    description TEXT NOT NULL,
    origin VARCHAR(150),
    usage TEXT,
    category_id INTEGER NOT NULL REFERENCES categories(id)
        ON DELETE RESTRICT
);

-- Статьи о специях
CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    title VARCHAR(250) NOT NULL,
    description TEXT,
    content TEXT,
    source_name VARCHAR(150),
    source_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    spice_id INTEGER NOT NULL REFERENCES spices(id)
        ON DELETE CASCADE
);

-- Изображения специй
CREATE TABLE images (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    image_url VARCHAR(500) NOT NULL,
    source_url VARCHAR(500),
    spice_id INTEGER NOT NULL REFERENCES spices(id)
        ON DELETE CASCADE
);

-- Видеоматериалы о специях
CREATE TABLE videos (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    video_url VARCHAR(500) NOT NULL,
    source_name VARCHAR(150),
    spice_id INTEGER NOT NULL REFERENCES spices(id)
        ON DELETE CASCADE
);

-- Индексы для ускорения поиска и соединения таблиц
CREATE INDEX idx_spices_name ON spices (name);
CREATE INDEX idx_spices_slug ON spices (slug);
CREATE INDEX idx_spices_category ON spices (category_id);
CREATE INDEX idx_articles_spice ON articles (spice_id);
CREATE INDEX idx_images_spice ON images (spice_id);
CREATE INDEX idx_videos_spice ON videos (spice_id);

COMMIT;
