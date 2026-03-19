import csv
from django.core.management.base import BaseCommand
from app.models import Match, Referee, Team, Season
from app.utils import parse_date


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['csv_file']
        with open(path, 'r', encoding='utf-8') as f:
            reader = list(csv.DictReader(f))

        for row in reader:
            date_parts = row['Date'].split('/')
            year = int("20" + date_parts[2]) if len(date_parts[2]) == 2 else int(date_parts[2])

            Season.objects.get_or_create(
                name=f"{year}-{year + 1}",
                division=row['Div'],
                defaults={'start_year': year, 'end_year': year + 1}
            )
            Team.objects.get_or_create(name=row['HomeTeam'])
            Team.objects.get_or_create(name=row['AwayTeam'])
            if row.get('Referee'):
                Referee.objects.get_or_create(name=row['Referee'])

        seasons = {(s.name, s.division): s for s in Season.objects.all()}
        teams = {t.name: t for t in Team.objects.all()}
        refs = {r.name: r for r in Referee.objects.all()}

        match_buffer = []
        for item in reader:
            formatted_date = parse_date(item.get('Date'))
            year = formatted_date.year
            season_key = (f"{year}-{year + 1}", item['Div'])

            match_buffer.append(Match(
                season=seasons.get(season_key),
                date=formatted_date,
                home_team=teams.get(item['HomeTeam']),
                away_team=teams.get(item['AwayTeam']),
                referee=refs.get(item['Referee']),
                fthg=int(item.get('FTHG', 0)),
                ftag=int(item.get('FTAG', 0)),
                ftr=item.get('FTR', 'D'),
                hthg=int(item.get('HTHG', 0)) if item.get('HTHG') else None,
                htag=int(item.get('HTAG', 0)) if item.get('HTAG') else None,
                hs=int(item.get('HS', 0)),
                a_s=int(item.get('AS', 0)),
                hst=int(item.get('HST', 0)),
                ast=int(item.get('AST', 0)),
                hf=int(item.get('HF', 0)),
                af=int(item.get('AF', 0)),
                hc=int(item.get('HC', 0)),
                ac=int(item.get('AC', 0)),
                hy=int(item.get('HY', 0)),
                ay=int(item.get('AY', 0)),
                hr=int(item.get('HR', 0)),
                ar=int(item.get('AR', 0)),
            ))

        Match.objects.bulk_create(match_buffer, batch_size=100)
        self.stdout.write(self.style.SUCCESS(f"✅ {len(match_buffer)} ta match saqlandi!"))
