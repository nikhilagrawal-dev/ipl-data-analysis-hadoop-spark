-- =========================================================================
-- Top Run Scorers with Average, Strike Rate, 4s, 6s, 50s, 100s
-- Wides excluded from balls faced per cricket rules
-- =========================================================================

WITH match_runs AS (
    SELECT 
        batter,
        match_id,
        SUM(batsman_runs) AS match_total
    FROM deliveries
    GROUP BY batter, match_id
),
milestones AS (
    SELECT 
        batter,
        MAX(match_total) AS highest_score,
        SUM(CASE WHEN match_total >= 100 THEN 1 ELSE 0 END) AS hundreds,
        SUM(CASE WHEN match_total >= 50 AND match_total < 100 THEN 1 ELSE 0 END) AS fifties
    FROM match_runs
    GROUP BY batter
),
dismissals AS (
    SELECT 
        batter,
        COUNT(*) AS dismissals
    FROM deliveries
    WHERE player_dismissed = batter
      AND dismissal_kind NOT IN ('retired hurt', 'none')
    GROUP BY batter
),
batting_agg AS (
    SELECT 
        batter,
        COUNT(DISTINCT match_id) AS matches_batted,
        SUM(batsman_runs) AS total_runs,
        SUM(CASE WHEN extras_type != 'wides' THEN 1 ELSE 0 END) AS balls_faced,
        SUM(is_four) AS fours,
        SUM(is_six) AS sixes,
        SUM(is_dot_ball) AS dot_balls
    FROM deliveries
    GROUP BY batter
    HAVING SUM(batsman_runs) >= 1000
)
SELECT 
    b.batter,
    b.matches_batted,
    b.total_runs,
    b.balls_faced,
    COALESCE(m.highest_score, 0) AS highest_score,
    ROUND(b.total_runs / NULLIF(COALESCE(d.dismissals, 0), 0), 2) AS batting_avg,
    ROUND((b.total_runs / NULLIF(b.balls_faced, 0)) * 100, 2) AS strike_rate,
    COALESCE(m.hundreds, 0) AS hundreds,
    COALESCE(m.fifties, 0) AS fifties,
    b.fours,
    b.sixes
FROM batting_agg b
LEFT JOIN milestones m ON b.batter = m.batter
LEFT JOIN dismissals d ON b.batter = d.batter
ORDER BY b.total_runs DESC
LIMIT 25;
