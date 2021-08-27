
-- transactional: false
-- TODO: sqlite doesn't suport enum structure for the role.
-- come up with a clean way to constrain role
CREATE TABLE User(
    id INTEGER,
    email VARCHAR(40) NOT NULL UNIQUE,
    role VARCHAR(40) NOT NULL,
    password_hash VARCHAR(40) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE UserSession(
  id INTEGER,
  token VARCHAR(40) UNIQUE,
  creation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  user_id INTEGER,
  PRIMARY KEY (id),
  FOREIGN KEY (user_id) REFERENCES User(id)
);

CREATE TABLE Instructor(
   id INTEGER,
   PRIMARY KEY (id),
   FOREIGN KEY (id) REFERENCES User(id)
);

CREATE TABLE DemandPattern(
    id INTEGER,
    weeks INTEGER NOT NULL,
    name VARCHAR(40) NOT NULL,
    encoded_data VARCHAR(200) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE Game(
    id INTEGER,
    session_length INTEGER,
    retailer_present BOOLEAN,
    wholesaler_present BOOLEAN,
    holding_cost FLOAT,
    backlog_cost FLOAT,
    instructor_id INTEGER NOT NULL,
    active BOOLEAN,
    demand_pattern_id INTEGER,
    starting_inventory INTEGER,
    info_delay INTEGER,
    info_sharing BOOLEAN,
    factory_id INTEGER UNIQUE,
    distributor_id INTEGER UNIQUE,
    retailer_id INTEGER UNIQUE,
    wholesaler_id INTEGER UNIQUE,
    PRIMARY KEY (id),
    FOREIGN KEY (instructor_id) REFERENCES User(id),
    FOREIGN KEY (demand_pattern_id) REFERENCES DemandPattern(id)

    FOREIGN KEY (factory_id) REFERENCES Player(id),
    FOREIGN KEY (distributor_id) REFERENCES Player(id),
    FOREIGN KEY (retailer_id) REFERENCES Player(id),
    FOREIGN KEY (wholesaler_id) REFERENCES Player(id)
);

CREATE TABLE Player(
    id INTEGER,
    current_game_id INTEGER,
    role VARCHAR(40) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (id) REFERENCES User(id),
    FOREIGN KEY (current_game_id) REFERENCES Game(id)
);

CREATE TABLE InstructorGames(
    game_id INTEGER,
    instructor_id INTEGER,
    PRIMARY KEY (instructor_id, game_id),
    FOREIGN KEY (game_id) REFERENCES Game(id),
    FOREIGN KEY (instructor_id)  REFERENCES Instructor(id)
);

CREATE TABLE GameState(
    id INTEGER,
    game_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    week INTEGER NOT NULL,
    order_amount INTEGER NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (game_id) REFERENCES Game(id),
    FOREIGN KEY (student_id) REFERENCES Game(id)
);
