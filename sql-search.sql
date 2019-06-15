CREATE TABLE `community_users3` (
  `nick` varchar(50) NOT NULL,
  `password_plaintext` varchar(40) NOT NULL,
  `realname` varchar(50) DEFAULT NULL,
  `regdate` datetime DEFAULT NULL,
  PRIMARY KEY (`nick`)
);
INSERT INTO community_users3 VALUES('einbenutzer','beispielpasswort','Echter Benutzer','1980-05-14 21:57:47');
INSERT INTO community_users3 VALUES('admin','Admini$tratorPa$$wort','Admin I. Strator','0000-00-00 00:00:00');
INSERT INTO community_users3 VALUES('NochJemand','geheimesPasswort','Guido Knopp','1964-05-11 21:52:47');
INSERT INTO community_users3 VALUES('XuserX1234','passwort1234','B. Nutzerr','1912-01-08 03:21:41');
