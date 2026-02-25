USE chess_data;

SELECT
    game_id,
    (white_rating - black_rating) AS rating_diff,
    turns,
    victory_status
FROM games
WHERE winner IN ('white', 'black')
  AND victory_status IN ('mate', 'resign', 'outoftime');



SELECT
    CASE
        WHEN (white_rating + black_rating) / 2 < 1200 THEN '1. Novice (<1200)'
        WHEN (white_rating + black_rating) / 2 BETWEEN 1200 AND 1499 THEN '2. Intermediate (1200-1499)'
        WHEN (white_rating + black_rating) / 2 BETWEEN 1500 AND 1799 THEN '3. Advanced (1500-1799)'
        ELSE '4. Master (1800+)'
    END AS rating_tier,
    winner,
    COUNT(*) as game_count
FROM games
GROUP BY 1, 2;


WITH TopOpenings AS (
    SELECT opening_name, COUNT(*) as total_games
    FROM games
    GROUP BY opening_name
    ORDER BY total_games DESC
    LIMIT 15
)
SELECT
    c.opening_name,
    c.winner,
    COUNT(*) as outcome_count,
    t.total_games
FROM games c
JOIN TopOpenings t ON c.opening_name = t.opening_name
GROUP BY c.opening_name, c.winner, t.total_games;


SELECT
    CASE
        WHEN (white_rating + black_rating) / 2 < 1200 THEN '1. Novice (<1200)'
        WHEN (white_rating + black_rating) / 2 BETWEEN 1200 AND 1499 THEN '2. Intermediate (1200-1499)'
        WHEN (white_rating + black_rating) / 2 BETWEEN 1500 AND 1799 THEN '3. Advanced (1500-1799)'
        ELSE '4. Master (1800+)'
    END AS rating_tier,
    opening_ply
FROM games;


SELECT
    ABS(white_rating - black_rating) AS rating_gap,
    CASE
        WHEN (white_rating > black_rating AND winner = 'black') THEN 'Upset (Lower Rated Won)'
        WHEN (black_rating > white_rating AND winner = 'white') THEN 'Upset (Lower Rated Won)'
        ELSE 'Expected (Higher Rated Won)'
    END AS outcome_type
FROM games
WHERE winner IN ('white', 'black');


SELECT
    time_increment,
    victory_status,
    COUNT(*) as game_count
FROM games
GROUP BY time_increment, victory_status;
