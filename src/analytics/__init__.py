"""Analytics Package for IPL Performance Insights"""
from .team_analytics import (
    get_team_overall_performance,
    get_team_season_performance,
    get_team_head_to_head,
)
from .player_analytics import (
    get_top_run_scorers,
    get_top_wicket_takers,
    get_player_of_match_counts,
)
from .season_analytics import (
    get_season_summary,
    get_over_phase_analytics,
)
from .venue_analytics import (
    get_venue_summary,
    get_team_performance_by_venue,
)
from .toss_analytics import (
    get_toss_decision_summary,
    get_toss_trends_by_season,
)

__all__ = [
    "get_team_overall_performance",
    "get_team_season_performance",
    "get_team_head_to_head",
    "get_top_run_scorers",
    "get_top_wicket_takers",
    "get_player_of_match_counts",
    "get_season_summary",
    "get_over_phase_analytics",
    "get_venue_summary",
    "get_team_performance_by_venue",
    "get_toss_decision_summary",
    "get_toss_trends_by_season",
]
