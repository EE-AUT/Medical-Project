CREATE TYPE user_types AS ENUM ('Doctor', 'Ordinary person');
CREATE TYPE register_types AS ENUM ('App', 'Web');


CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) NOT NULL,
  FirstName  VARCHAR(255) NOT NULL,
  LastName  VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL,
  phone VARCHAR(255) not NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  user_type user_types NOT NULL,
  regester_type register_types,
  doctor_id VARCHAR(255),
  UNIQUE(email),
  UNIQUE(phone)
);



CREATE TABLE notverified (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) NOT NULL,
  FirstName  VARCHAR(255) NOT NULL,
  LastName  VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL,
  phone VARCHAR(255) not NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  user_type user_types NOT NULL,
  regester_type register_types,
  doctor_id VARCHAR(255) NOT NULL,
  UNIQUE(email),
  UNIQUE(phone)
);

CREATE TABLE Img(
  id_pic SERIAL PRIMARY KEY,
  owner_id INTEGER NOT NULL,
  data_pic bytea NOT NULL,
  format_pic VARCHAR(255) NOT NULL,
  upload_at TIMESTAMP NOT NULL,

  FOREIGN KEY (owner_id) REFERENCES users(id)
);



insert into users(email, password, phone, created_at, updated_at, user_type, regester_type, doctor_id) 
	values('mahdi.sabour@aut.ac.ir', '0021639450', '09145178976', now(), now(), 'Doctor', 'App', NULL);

