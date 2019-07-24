DROP TABLE IF EXISTS artist cascade;
DROP TABLE IF EXISTS song cascade;
DROP TABLE IF EXISTS token cascade;
DROP TABLE IF EXISTS tfidf cascade;




CREATE TABLE artist (
	artist_id INTEGER PRIMARY KEY,
	artist_name VARCHAR(255)
);


CREATE TABLE token (
	song_id INTEGER,
	token VARCHAR(255),
	count INTEGER,
	PRIMARY KEY (song_id, token)
);

CREATE TABLE song (
	song_id INTEGER PRIMARY KEY,
	artist_id INTEGER REFERENCES artist(artist_id),
	song_name VARCHAR(255),
	page_link VARCHAR(1000)
	/* , FOREIGN KEY (artist_id) REFERENCES artist (artist_id) */
);

CREATE TABLE tfidf (
	song_id INTEGER,
	token VARCHAR(255),
	score FLOAT,
	PRIMARY KEY(song_id, token)
);

\copy artist FROM '/home/cs143/data/artist.csv' DELIMITER ',' QUOTE '"' CSV;
\copy song   FROM '/home/cs143/data/song.csv'   DELIMITER ',' QUOTE '"' CSV;
\copy token  FROM '/home/cs143/data/token.csv'  DELIMITER ',' QUOTE '"' CSV;



INSERT INTO  tfidf (song_id, token, score)

SELECT song_id, r.token, (count * IDF) as score FROM

(
SELECT token,log(57650.0/COUNT(song_id)) as IDF
FROM token
GROUP BY token
) r INNER JOIN token ON token.token = r.token
;




