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

-- Find the number of wins for each player
CREATE VIEW player_wins AS
SELECT players.id, COUNT(matches.winner) AS wins
FROM players LEFT JOIN matches
ON players.id = matches.winner
GROUP BY players.id
ORDER BY wins DESC;

-- Find the number of matches each player has played
CREATE VIEW player_matches_played AS
SELECT players.id, COUNT(matches.*) AS matches_played
FROM players LEFT JOIN matches
ON players.id = matches.p1 OR players.id = matches.p2
GROUP BY players.id
ORDER BY matches_played DESC;

-- Player standings
CREATE VIEW player_standings AS
SELECT players.id, players.name, player_wins.wins, player_matches_played.matches_played
FROM players, player_wins, player_matches_played
WHERE players.id = player_wins.id AND players.id = player_matches_played.id
ORDER BY player_wins.wins DESC, player_matches_played.matches_played, players.id;