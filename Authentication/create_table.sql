-- MYSQL statements for table creation
-- password and username must match


CREATE DATABASE `authentication` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;


CREATE TABLE `user` (
  `email` varchar(100) NOT NULL,
  `password` varchar(45) NOT NULL,
  `code` char(10) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `session` char(10) DEFAULT NULL,
  `first` varchar(45) NOT NULL,
  `last` varchar(45) NOT NULL,
  `phone` char(15) NOT NULL,
  `ssn` char(4) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;
