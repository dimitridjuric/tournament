Notes on the Tournament Project


Setup:

A database named tournament must be created in Postgres

=>CREATE DATABASE TOURNAMENT;

then connect to this database and import tournament.sql
with the commands

=>\c tournament
=>\i tournament.sql

This creates all the tables and views necessary to run the python files.
The tournament.py file is the module with the functions described at the
end of this file.
tournament_test.py is the test file for these functions. I have added a few
test/demo functions for two functions from the extra credit list:
playerStandingOMW and swissPairingsOMW implement the opponent match wins when
two players have the same number of wins.
playerStandingsDraw and swissPairingsDraw allow the possibility of a draw as
the result of a match.
reportMatch has a third optional argument to allow draws. 



List of functions in tournament.py with their docstrings

connect()
deleteMatches()
    """Remove all the match records from the database."""
deletePlayers()
    """Remove all the player records from the database."""
countPlayers()
    """Returns the number of players currently registered."""
registerPlayer(name)
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
playerStandings()
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
playerStandingsDraw()
    """Returns a list of the players and their win records, sorted by score.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, score, matches):
        id: the player's unique id (assigned by the database)
        score: the player gets 1 for each wins, 0.5 for a draw, and 0 for a loss
        matches: the number of matches the player has played
    """
reportMatch(winner, loser, draw=False)
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
      draw: True if the match is a draw
    """
swissPairings()
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
swissPairingsDraw()
    """Returns a list of pairs of players for the next round of a match. this
    version works when the result of a match can be a draw.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal score record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, score1, id2, score2)
    """
playerStandingsOMW()
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
swissPairingsOMW()
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
