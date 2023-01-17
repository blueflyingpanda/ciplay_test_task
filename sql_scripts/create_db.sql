CREATE TABLE ciplay_stats (
    stat_id SERIAL PRIMARY KEY,
    date DATE NOT NULL UNIQUE ,
    views BIGINT,
    clicks BIGINT,
    cost DECIMAL(12,2)
);