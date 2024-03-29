#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def delete_matches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()

    c.execute("DELETE FROM matches")
    conn.commit()
    conn.close()


def delete_players():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()

    c.execute("DELETE FROM players")
    conn.commit()
    conn.close()


def count_players():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()

    c.execute("SELECT COUNT(*) as num FROM players")
    row = c.fetchone()
    conn.close()

    return row[0]


def register_player(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()

    c.execute("INSERT INTO players VALUES (%s)", (name,))
    conn.commit()
    conn.close()


def player_standings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    c = conn.cursor()

    c.execute("SELECT * FROM player_standings")
    rows = c.fetchall()
    standings = [(row[0], row[1], row[2], row[3]) for row in rows]
    conn.close()

    return standings


def report_match(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    c = conn.cursor()

    c.execute("INSERT INTO matches VALUES (%s, %s, %s)", (winner, loser, winner,))
    conn.commit()
    conn.close()
 
 
def swiss_pairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = player_standings()
    pairings = []

    # Pair up every two players according to the standings
    for x in range(0, len(standings), 2):
        pairing = (standings[x][0], standings[x][1], standings[x + 1][0], standings[x + 1][1])
        pairings.append(pairing)

    return pairings
