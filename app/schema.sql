DROP TABLE IF EXISTS room;
DROP TABLE IF EXISTS playing;
CREATE TABLE room (
    id VARCHAR PRIMARY KEY,
    room_name VARCHAR NOT NULL,
    room_size INTEGER NOT NULL,
    room_type BOOLEAN NOT NULL,
    engaged_place INTEGER NOT NULL,
    playing_status BOOLEAN NOT NULL
);

CREATE TABLE playing (
    id VARCHAR NOT NULL
);
