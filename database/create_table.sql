CREATE TABLE dungeon.users (
	id INT auto_increment NOT NULL,
	username varchar(32) NOT NULL,
	password varchar(160) NOT NULL,
	status INT DEFAULT 1,
	data json NOT NULL,
	PRIMARY KEY (id)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8
COLLATE=utf8_general_ci;