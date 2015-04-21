-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

create table players (
    player_id serial primary key,
    name text
);

create table matches (
    winner integer references players(player_id),
    loser integer references players(player_id),
    draw boolean
);

-- this view shows the scores of matches including half points for draws
create view match_scores as
    select winner as player1,
        loser as player2,
        case when draw=false then 1
            else 0.5
        end as score1,
        case when draw=false then 0
            else 0.5
        end as score2
    from matches;

-- this view shows the scores of the players (1 for wins, 0.5 for draws, 0 for lose).
create view players_scores as
    select player_id, coalesce(sum(a.score),0) as total
    from (
        select player1 as player, score1 as score
        from match_scores
        union all
        select player2, score2
        from match_scores) as a
        right join
        players
    on player_id=player
    group by player_id
    order by total desc;

-- this view has a player id column and a number of matches played column
create view matches_played as
    select players.player_id, count(b.player_id) as matches_played
    from players
    left join
        (select player_id
        from players, matches
        where player_id = winner or player_id = loser) as b
    on players.player_id = b.player_id
    group by players.player_id;
    
-- this view has a player id column, a name column and the number of wins for this player    
create view matches_won as
    select player_id, name, count(winner) as wins
    from players left join matches
    on player_id = winner
    group by player_id
    order by wins desc;
    
-- this view has a row for each match each player has played and its opponent   
create view oppo as
    select a.player_id, b.player_id as oppo
    from players as a, players as b, matches
    where (b.player_id = winner and a.player_id = loser)
    or (b.player_id = loser and a.player_id = winner);    
    
-- this view has each player and the sum of the wins of his opponents    
create view omw as
    select a.player_id, sum(matches_won.wins) as omw
    from matches_won
    right join
        (select players.player_id, oppo.oppo
        from players
        left join oppo
        on players.player_id = oppo.player_id) as a
    on a.oppo = matches_won.player_id
    group by a.player_id
    order by omw desc;