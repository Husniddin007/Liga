from django.db.models import Sum, Count, Q

from app.models import Match


def get_team_season_stats(team, season):
    home = Match.objects.filter(home_team=team, season=season).aggregate(
        home_played = Count("id"),
        home_gf = Sum("fthg"),
        home_ga = Sum("ftag"),
        home_wins = Count("id", filter=Q(ftr="H")),
        home_draws = Count("id", filter=Q(ftr="D")),
        home_losses = Count("id", filter=Q(ftr="A")),
        home_shots = Sum("hs"),
        home_sot = Sum("hst"),
        home_fouls = Sum("hf"),
        home_yellows = Sum("hy"),
        home_reds = Sum("hr"),
    )

    away = Match.objects.filter(away_team=team, season=season).aggregate(
        away_played = Count("id"),
        away_gf = Sum("ftag"),
        away_ga = Sum("fthg"),
        away_wins = Count("id", filter=Q(ftr="A")),
        away_draws = Count("id", filter=Q(ftr="D")),
        away_losses = Count("id", filter=Q(ftr="H")),
        away_shots = Sum("a_s"),
        away_sot = Sum("ast"),
        away_fouls = Sum("af"),
        away_yellows= Sum("ay"),
        away_reds = Sum("ar"),
    )

    played  = home["home_played"] + away["away_played"]
    gf = (home["home_gf"] or 0) + (away["away_gf"] or 0)
    ga = (home["home_ga"] or 0) + (away["away_ga"] or 0)
    wins = (home["home_wins"] or 0) + (away["away_wins"] or 0)
    draws = (home["home_draws"] or 0) + (away["away_draws"] or 0)
    losses = (home["home_losses"] or 0) + (away["away_losses"] or 0)
    points = wins * 3 + draws

    return {
        "team": str(team),
        "played": played,
        "wins": wins,
        "draws": draws,
        "losses": losses,
        "goals_for": gf,
        "goals_against": ga,
        "goal_diff": gf - ga,
        "points": points,
        "shots": (home["home_shots"] or 0) + (away["away_shots"] or 0),
        "shots_on_target": (home["home_sot"] or 0) + (away["away_sot"] or 0),
        "fouls": (home["home_fouls"] or 0) + (away["away_fouls"] or 0),
        "yellow_cards":(home["home_yellows"] or 0) + (away["away_yellows"] or 0),
        "red_cards": (home["home_reds"] or 0) + (away["away_reds"] or 0),
        "form": get_team_form(team, season),
    }

def get_team_form(team, season):
    last_matches = Match.objects.filter(
        Q(home_team=team) | Q(away_team=team),
        season=season
    ).order_by('-date')[:5]

    form = []
    for match in reversed(last_matches):
        if match.ftr == 'D':
            form.append('D')
        elif (match.home_team == team and match.ftr == 'H') or \
             (match.away_team == team and match.ftr == 'A'):
            form.append('W')
        else:
            form.append('L')
    return " ".join(form)


