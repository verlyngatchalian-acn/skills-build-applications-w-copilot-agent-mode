from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Clear ManyToMany relationships first
        for workout in Workout.objects.all():
            workout.suggested_for.clear()

        # Delete dependent objects first
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        User.objects.all().delete()
        for workout in Workout.objects.all():
            if workout.id is not None:
                workout.delete()
        for team in Team.objects.all():
            if team.id is not None:
                team.delete()

        # Create Teams
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        # Create Users (super heroes)
        users = [
            User(email='ironman@marvel.com', name='Iron Man', team=marvel),
            User(email='captainamerica@marvel.com', name='Captain America', team=marvel),
            User(email='spiderman@marvel.com', name='Spider-Man', team=marvel),
            User(email='batman@dc.com', name='Batman', team=dc),
            User(email='superman@dc.com', name='Superman', team=dc),
            User(email='wonderwoman@dc.com', name='Wonder Woman', team=dc),
        ]
        for user in users:
            user.save()

        # Create Activities
        activities = [
            Activity(user=users[0], type='Running', duration=30),
            Activity(user=users[1], type='Cycling', duration=45),
            Activity(user=users[3], type='Swimming', duration=60),
        ]
        for activity in activities:
            activity.save()

        # Create Workouts and set suggested_for teams
        cardio = Workout.objects.create(name='Cardio Blast', description='High intensity cardio workout')
        strength = Workout.objects.create(name='Strength Training', description='Full body strength routine')
        cardio.suggested_for.set([marvel, dc])
        strength.suggested_for.set([marvel, dc])

        # Create Leaderboard
        Leaderboard.objects.create(team=marvel, points=150)
        Leaderboard.objects.create(team=dc, points=120)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data'))
