PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "User" (
	user_id INTEGER NOT NULL, 
	username VARCHAR, 
	password_hash VARCHAR, 
	PRIMARY KEY (user_id)
);
CREATE TABLE IF NOT EXISTS "Site" (
	site_id INTEGER NOT NULL, 
	site VARCHAR, 
	login VARCHAR, 
	password VARCHAR, 
	user_id INTEGER, 
	PRIMARY KEY (site_id), 
	FOREIGN KEY(user_id) REFERENCES "User" (user_id)
);
COMMIT;
