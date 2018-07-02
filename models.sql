CREATE DATABASE dailywebherald CHARACTER SET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
--ALTER DATABASE dailywebherald CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci; --	Unicode/generic
--ALTER DATABASE dailywebherald CHARACTER SET utf8mb4 COLLATE utf8mb4;
--ALTER DATABASE dailywebherald CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;
USE dailywebherald;
SET NAMES utf8mb4;

CREATE TABLE websites(
	id INT AUTO_INCREMENT PRIMARY KEY,
	url VARCHAR(1024) NOT NULL,
	updateTime TIMESTAMP DEFAULT "1970-01-01 00:00:01",
	count INT DEFAULT 0,
	download BOOLEAN DEFAULT TRUE
);
SHOW WARNINGS;

CREATE TABLE articles(
	id INT AUTO_INCREMENT PRIMARY KEY,
	site INT NOT NULL,
	content TEXT,
	summary TEXT,
	title NVARCHAR(512) NOT NULL,
	url VARCHAR(2048) NOT NULL,
	publisher NVARCHAR(256),
	date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	display BOOLEAN DEFAULT TRUE,
	views INT DEFAULT 0,
	rating INT DEFAULT 5,  --  Values from 1 to 5
	language VARCHAR(8) DEFAULT "en",
	FOREIGN KEY (site) REFERENCES websites(id)
) DEFAULT CHARSET=utf8mb4;
SHOW WARNINGS;

CREATE TABLE users(
	id INT AUTO_INCREMENT PRIMARY KEY,
	email VARCHAR(256) DEFAULT "",
	name VARCHAR(256) NOT NULL,
	password VARCHAR(1024) NOT NULL,
	salt VARCHAR(64) NOT NULL,
	registrationdDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
SHOW WARNINGS;

CREATE TABLE subscriptions(
	id INT AUTO_INCREMENT PRIMARY KEY,
	user INT,
	site INT,
	time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY(user) REFERENCES users(id),
	FOREIGN KEY(site) REFERENCES websites(id)
);
SHOW WARNINGS;

CREATE TABLE pageRequests(
	id INT AUTO_INCREMENT PRIMARY KEY,
	method VARCHAR(8) DEFAULT "GET",
	page VARCHAR(1024),
	ip VARCHAR(256),
	environ VARCHAR(4098),
	appName VARCHAR(512),
	appVersion VARCHAR(512),
	userAgent VARCHAR(512),
	appCodeName VARCHAR(512),
	date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
SHOW WARNINGS;

CREATE TABLE rawArticles(
	id INT AUTO_INCREMENT PRIMARY KEY,
	feed TEXT NOT NULL
);
SHOW WARNINGS;

CREATE TABLE rawFeeds(
    id INT AUTO_INCREMENT PRIMARY KEY,
	feed TEXT NOT NULL
);
SHOW WARNINGS;

CREATE TABLE stdErrors(
	id INT AUTO_INCREMENT PRIMARY KEY,
	description TEXT NOT NULL
);
SHOW WARNINGS;

CREATE TABLE errorInstances(
	id INT AUTO_INCREMENT PRIMARY KEY,
	number INT NOT NULL,
	dump TEXT,
	time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
SHOW WARNINGS;

CREATE TABLE contactMessages(
    id INT AUTO_INCREMENT PRIMARY KEY,
    message TEXT NOT NULL,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    email VARCHAR(256) NOT NULL,
    sender VARCHAR(64) NOT NULL,
    subject VARCHAR(256) DEFAULT "",
    respond BOOLEAN DEFAULT FALSE
);
SHOW WARNINGS;

CREATE TABLE articleViews(
    id INT AUTO_INCREMENT PRIMARY KEY,
    article INT,
    user INT,
    viewed BOOLEAN DEFAULT FALSE,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(article) REFERENCES articles(id),
    FOREIGN KEY(user) REFERENCES users(id)
);
SHOW WARNINGS;

CREATE TABLE bookmarks(
    id INT AUTO_INCREMENT PRIMARY KEY,
    article INT,
    user INT,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(article) REFERENCES articles(id),
    FOREIGN KEY(user) REFERENCES users(id)
);
SHOW WARNINGS;

CREATE TABLE loginAttempts(
    id INT AUTO_INCREMENT PRIMARY KEY,
    user INT NOT NULL,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user) REFERENCES users(id)
);
SHOW WARNINGS;

CREATE TABLE logins(
    id INT AUTO_INCREMENT PRIMARY KEY,
    user INT NOT NULL,
    loginTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    logoutTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user) REFERENCES users(id)
);
SHOW WARNINGS;

--   Change to ROW_FORMAT=dynamic when compression is undesired
--ALTER TABLE articles ROW_FORMAT=compressed;
ALTER TABLE articles ROW_FORMAT=compact;
SHOW WARNINGS;

--ALTER TABLE rawArticles ROW_FORMAT=compressed;
ALTER TABLE rawArticles ROW_FORMAT=compact;
SHOW WARNINGS;

--ALTER TABLE pageRequests ROW_FORMAT=compressed;
ALTER TABLE pageRequests ROW_FORMAT=compact;
SHOW WARNINGS;

--  Set websites to UNIX epoch
--UPDATE websites SET updateTime = ("1970-1-1 00:00:01");

--	Get URL of subscriptions
--SELECT url FROM websites INNER JOIN subscriptions ON subscriptions.site = websites.id;
