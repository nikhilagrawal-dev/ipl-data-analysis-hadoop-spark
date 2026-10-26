-- =========================================================================
-- Top Wicket Takers with Economy, Average, Strike Rate
-- Strictly excludes run outs, retired out/hurt from bowler wickets
-- Excludes fielding byes/legbyes from bowler conceded runs
-- =========================================================================

SELECT 
    bowler,
    COUNT(DISTINCT match_id) AS matches_bowled,
    SUM(CASE WHEN extras_type NOT IN ('wides', 'noballs') THEN 1 ELSE 0 END) AS legal_balls,
    ROUND(SUM(CASE WHEN extras_type NOT IN ('wides', 'noballs') THEN 1 ELSE 0 END) / 6.0, 1) AS overs,
    SUM(CASE WHEN dismissal_kind IN ('bowled', 'caught', 'caught and bowled', 'lbw', 'stumped', 'hit wicket') THEN 1 ELSE 0 END) AS wickets,
    SUM(CASE WHEN extras_type IN ('byes', 'legbyes') THEN batsman_runs ELSE total_runs END) AS runs_conceded,
    ROUND(SUM(CASE WHEN extras_type IN ('byes', 'legbyes') THEN batsman_runs ELSE total_runs END) / (SUM(CASE WHEN extras_type NOT IN ('wides', 'noballs') THEN 1 ELSE 0 END) / 6.0), 2) AS economy,
    ROUND(SUM(CASE WHEN extras_type IN ('byes', 'legbyes') THEN batsman_runs ELSE total_runs END) / NULLIF(SUM(CASE WHEN dismissal_kind IN ('bowled', 'caught', 'caught and bowled', 'lbw', 'stumped', 'hit wicket') THEN 1 ELSE 0 END), 0), 2) AS bowling_avg,
    ROUND(SUM(CASE WHEN extras_type NOT IN ('wides', 'noballs') THEN 1 ELSE 0 END) / NULLIF(SUM(CASE WHEN dismissal_kind IN ('bowled', 'caught', 'caught and bowled', 'lbw', 'stumped', 'hit wicket') THEN 1 ELSE 0 END), 0), 2) AS strike_rate
FROM deliveries
GROUP BY bowler
HAVING SUM(CASE WHEN dismissal_kind IN ('bowled', 'caught', 'caught and bowled', 'lbw', 'stumped', 'hit wicket') THEN 1 ELSE 0 END) >= 50
ORDER BY wickets DESC, bowling_avg ASC
LIMIT 25;
