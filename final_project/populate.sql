-- Relation for the engine table, about 500 tuples
\copy engine FROM 'engine.csv' DELIMITER ';' CSV HEADER;

-- Relation for the game table, 50,000 tuples
\copy game FROM 'game.csv' DELIMITER ';' CSV HEADER;

-- Relation for company table, 10,000 tuples
\copy company FROM 'company.csv' DELIMITER ';' CSV HEADER;

-- Relation for platforms, only 158 exist
\copy platform FROM 'platform.csv' DELIMITER ';' CSV HEADER;

-- Relation for game modes, about 50,000 tuples
\copy mode FROM 'game_mode.csv' DELIMITER ';' CSV HEADER;

-- M:M Table for game and engines, about 4000 tuples
\copy game_engine FROM 'game_engine.csv' DELIMITER ';' CSV HEADER;

-- games and their publishing companies, about 26,000 tuples
\copy published FROM 'published.csv' DELIMITER ';' CSV HEADER;

-- game and their developing companies, about 20,000 tuples
\copy developed FROM 'developed.csv' DELIMITER ';' CSV HEADER;

-- engines deployed for specific platforms, about 400 tuples
\copy deployment_engines FROM 'engine_platforms.csv' DELIMITER ';' CSV HEADER;

-- release dates for games on multiple consoles, about 38,000 tuples
\copy release_dates FROM 'release_dates.csv' DELIMITER ';' CSV HEADER;

-- genres for each game, about 85,000 tuples
\copy genre FROM 'game_genre.csv' DELIMITER ';' CSV HEADER;

-- games released for specific platforms, about 86,000 tuples
\copy game_platform FROM 'game_plat.csv' DELIMITER ';' CSV HEADER;