CREATE TABLE `player` (
  `id` varchar(50) NOT NULL,
  `Co2_Max` decimal(10,2) DEFAULT '5000.00',
  `Co2_consumed` decimal(10,2) DEFAULT '0.00',
  `screen_name` varchar(50) DEFAULT NULL,
  `current_airport` varchar(40) DEFAULT NULL,
  `destination` varchar(40) DEFAULT NULL,
  `Total_fuel` decimal(10,2) DEFAULT '3000.00',
  `Total_fuel_consumed` decimal(10,2) DEFAULT '0.00',
  `Goal_points` int DEFAULT '0',
  `distance` decimal(10,2) DEFAULT '0.00',
  `Flights_completed` int DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `current_airport` (`current_airport`),
  KEY `Destination` (`destination`),
  CONSTRAINT `1` FOREIGN KEY (`current_airport`) REFERENCES `airport` (`ident`),
  CONSTRAINT `2` FOREIGN KEY (`destination`) REFERENCES `airport` (`ident`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1



