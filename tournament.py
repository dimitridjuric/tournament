#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("delete from matches;")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("delete from players;")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    c.execute("select count(*) from players;")
    count = c.fetchall()[0][0]
    db.close()
    return count


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    
    # clean the data befor inserting into the DB
    name = bleach.clean(name, tags={}, strip=True)
    
    db = connect()
    c = db.cursor()
    c.execute("insert into players (name) values(%s);", (name,))
    db.commit()
    db.close()


def playerStandings():
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
    db = connect()
    c = db.cursor()
    c.execute("""select matches_played.player_id, name, wins, matches_played
              from matches_played, matches_won
              where matches_played.player_id = matches_won.player_id
              order by wins desc;""")
    result = c.fetchall()
    db.close()
    return result


def playerStandingsDraw():
    """Returns a list of the players and their win records, sorted by score.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, score, matches):
        id: the player's unique id (assigned by the database)
        score: the player gets 1 for each wins, 0.5 for a draw, and 0 for a loss
        matches: the number of matches the player has played
    """
    db = connect()
    c = db.cursor()
    c.execute("""select matches_played.player_id, total, matches_played
              from matches_played, players_scores
              where matches_played.player_id = players_scores.player_id
              order by total desc;""")
    result = c.fetchall()
    db.close()
    return result


def reportMatch(winner, loser, draw=False):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
      draw: True if the match is a draw
    """
    db = connect()
    c = db.cursor()
    c.execute("insert into matches (winner, loser, draw) values(%s,%s,%s);",
              (str(winner), str(loser), draw))
    db.commit()
    db.close()

 
def swissPairings():
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
    standings = playerStandings()
    pairings = [(standings[i][0], standings[i][1], standings[i+1][0],
                 standings[i+1][1]) for i in range(0, len(standings)-1, 2)]
    return pairings

def swissPairingsDraw():
    """Returns a list of pairs of players for the next round of a match. this
    version works when the result of a match can be a draw.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal score record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, score1, id2, score2)
    """
    standings = playerStandingsDraw()
    pairings = [(standings[i][0], standings[i][1], standings[i+1][0],
                 standings[i+1][1]) for i in range(0, len(standings)-1, 2)]
    return pairings


def playerStandingsOMW():
    """Returns a list of the players and their win records, sorted by wins,
    and if the wins score is equals it sorts by opponents match wins

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie. If 2 players have the same
    win record they will be ordered by opponemt match win average.

    Returns:
      A list of tuples, each of which contains (id, wins, opponent match wins avg):
        id: the player's unique id (assigned by the database)
        wins: the number of matches the player has won
        omw: I'm using an average of the wins here. if a player plays twice against
        the same opponent that win will be counted twice in the average.
    """
    db = connect()
    c = db.cursor()
    c.execute("""select matches_won.player_id, wins, omw
              from matches_won, omw
              where matches_won.player_id = omw.player_id
              order by wins desc, omw desc;""")
    result = c.fetchall()
    db.close()
    return result


def swissPairingsOMW():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, id2)
        id1: the first player's unique id
        id2: the second player's unique id
    """
    standings = playerStandingsOMW()
    pairings = [(standings[i][0],
                 standings[i+1][0]) for i in range(0, len(standings)-1, 2)]
    return pairings