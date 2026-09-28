CREATE TABLE player (
    id INT PRIMARY KEY AUTO_INCREMENT,
    Co2_Max DECIMAL(10,2) DEFAULT 10000,
    Co2_consumed DECIMAL(10,2) DEFAULT 0,
    screen_name VARCHAR(50),
    current_airport VARCHAR(40),
    Destination VARCHAR(40),
    Total_fuel DECIMAL(10,2) DEFAULT 3000.00,
    Total_fuel_consumed DECIMAL(10,2) DEFAULT 0.00,
    Goal_points INT DEFAULT 0,

    FOREIGN KEY (current_airport) REFERENCES airport(ident),
    FOREIGN KEY (Destination) REFERENCES airport(ident)
) ENGINE=InnoDB
  DEFAULT CHARSET=latin1
  COLLATE=latin1_swedish_ci;



