-- =========================================================================
-- Team Overall Standings (Matches Played, Wins, Losses, Ties, Win %)
-- Denominator rule: Excludes matches abandoned with no result
-- =========================================================================

WITH team_matches AS (
    SELECT 
        team1 AS team,
        CASE WHEN winner = team1 THEN 1 ELSE 0 END AS win,
        CASE WHEN is_result_declared AND winner != team1 THEN 1 ELSE 0 END AS loss,
        CASE WHEN result = 'tie' THEN 1 ELSE 0 END AS tie,
        CASE WHEN NOT is_result_declared THEN 1 ELSE 0 END AS no_result
    FROM matches
    
    UNION ALL
    
    SELECT 
        team2 AS team,
        CASE WHEN winner = team2 THEN 1 ELSE 0 END AS win,
        CASE WHEN is_result_declared AND winner != team2 THEN 1 ELSE 0 END AS loss,
        CASE WHEN result = 'tie' THEN 1 ELSE 0 END AS tie,
        CASE WHEN NOT is_result_declared THEN 1 ELSE 0 END AS no_result
    FROM matches
)
SELECT 
    team,
    COUNT(*) AS matches_played,
    SUM(win) AS wins,
    SUM(loss) AS losses,
    SUM(tie) AS ties,
    SUM(no_result) AS no_results,
    ROUND((SUM(win) / NULLIF(COUNT(*) - SUM(no_result), 0)) * 100, 2) AS win_percentage
FROM team_matches
GROUP BY team
ORDER BY wins DESC, win_percentage DESC;
