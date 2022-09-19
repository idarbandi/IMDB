from models import db, Genre, Movie


def create_table():
    db.create_tables([Genre, Movie])
