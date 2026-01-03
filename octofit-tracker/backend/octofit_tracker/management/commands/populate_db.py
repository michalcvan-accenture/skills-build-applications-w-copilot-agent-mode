from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models
from octofit_tracker import settings
from django.conf import settings as django_settings
from pymongo import MongoClient

# Models for demonstration (replace with real models if available)
class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    class Meta:
        app_label = 'octofit_tracker'

class Activity(models.Model):
    user = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    duration = models.IntegerField()
    class Meta:
        app_label = 'octofit_tracker'

class Leaderboard(models.Model):
    user = models.CharField(max_length=100)
    score = models.IntegerField()
    class Meta:
        app_label = 'octofit_tracker'

class Workout(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    class Meta:
        app_label = 'octofit_tracker'

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']
        # Drop collections if they exist
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()
        # Create unique index on email
        db.users.create_index('email', unique=True)
        # Insert test users
        users = [
            {"name": "Superman", "email": "superman@dc.com", "team": "DC"},
            {"name": "Batman", "email": "batman@dc.com", "team": "DC"},
            {"name": "Wonder Woman", "email": "wonderwoman@dc.com", "team": "DC"},
            {"name": "Iron Man", "email": "ironman@marvel.com", "team": "Marvel"},
            {"name": "Captain America", "email": "cap@marvel.com", "team": "Marvel"},
            {"name": "Black Widow", "email": "widow@marvel.com", "team": "Marvel"},
        ]
        db.users.insert_many(users)
        # Insert teams
        teams = [
            {"name": "Marvel"},
            {"name": "DC"},
        ]
        db.teams.insert_many(teams)
        # Insert activities
        activities = [
            {"user": "Superman", "type": "Flight", "duration": 120},
            {"user": "Batman", "type": "Martial Arts", "duration": 90},
            {"user": "Iron Man", "type": "Engineering", "duration": 100},
        ]
        db.activities.insert_many(activities)
        # Insert leaderboard
        leaderboard = [
            {"user": "Superman", "score": 1000},
            {"user": "Iron Man", "score": 950},
            {"user": "Batman", "score": 900},
        ]
        db.leaderboard.insert_many(leaderboard)
        # Insert workouts
        workouts = [
            {"name": "Hero HIIT", "description": "High intensity interval training for heroes."},
            {"name": "Power Yoga", "description": "Yoga for strength and flexibility."},
        ]
        db.workouts.insert_many(workouts)
        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
