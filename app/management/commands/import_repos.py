import csv
from django.core.management.base import BaseCommand
from app.models import Match, Referee, Team, Division
from app.utils import parse_date


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['csv_file']
        with open(path, 'r', encoding='utf-8') as f:
            reader = list(csv.DictReader(f))

        div_names = {row['Div'] for row in reader if row.get('Div')}
        team_names = {row['HomeTeam'] for row in reader if row.get('HomeTeam')} | \
                     {row['AwayTeam'] for row in reader if row.get('AwayTeam')}
        ref_names = {row['Referee'] for row in reader if row.get('Referee')}

        for name in div_names:
            Division.objects.get_or_create(name=name)
        for name in team_names:
            Team.objects.get_or_create(name=name)
        for name in ref_names:
            Referee.objects.get_or_create(name=name)

        divs = {d.name: d for d in Division.objects.all()}
        teams = {t.name: t for t in Team.objects.all()}
        refs = {r.name: r for r in Referee.objects.all()}

        match_buffer = []
        for item in reader:
            formatted_date = parse_date(item.get('Date'))

            match_buffer.append(Match(
                date=formatted_date,
                div=divs.get(item['Div']),
                home_team=teams.get(item['HomeTeam']),
                away_team=teams.get(item['AwayTeam']),
                referee=refs.get(item['Referee']),
                fthg=item.get('FTHG') or 0,
                ftag=item.get('FTAG') or 0,
                ftr=item.get('FTR') or 'D',
                hthg=item.get('HTHG') or 0,
                htag=item.get('HTAG') or 0,
                hs=item.get('HS') or 0,
                a_s=item.get('AS') or 0,
                hst=item.get('HST') or 0,
                ast=item.get('AST') or 0,
                hf=item.get('HF') or 0,
                af=item.get('AF') or 0,
                hc=item.get('HC') or 0,
                ac=item.get('AC') or 0,
                hy=item.get('HY') or 0,
                ay=item.get('AY') or 0,
                hr=item.get('HR') or 0,
                ar=item.get('AR') or 0,
            ))

        batch_size = 1000
        Match.objects.bulk_create(match_buffer, batch_size=batch_size)

        self.stdout.write(self.style.SUCCESS(f"✅ {len(match_buffer)} ta match muvaffaqiyatli saqlandi!"))
