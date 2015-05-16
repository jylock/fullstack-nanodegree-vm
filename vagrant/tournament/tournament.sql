-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Create tournament database
CREATE DATABASE tournament;

-- Connect to tournament database
\c tournament;

-- Create players table
CREATE TABLE players (
  name TEXT,
  id SERIAL PRIMARY KEY
);

-- Create matches table
CREATE TABLE matches (
  p1 INTEGER REFERENCES players (id),
  p2 INTEGER REFERENCES players (id),
  winner INTEGER REFERENCES players (id),
  PRIMARY KEY (p1, p2)
);