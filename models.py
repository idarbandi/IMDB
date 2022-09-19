from peewee import SqliteDatabase, ForeignKeyField, \
    TextField, CharField, DateTimeField, BooleanField, \
    IntegerField, FloatField, Model

from khayyam.jalali_datetime import JalaliDatetime

db = SqliteDatabase("Posts.db")


class BaseModel(Model):
    created_time = DateTimeField(default=str(JalaliDatetime.now()))

    class Meta:
        database = db


class Genre(BaseModel):
    name = CharField()


class Movie(BaseModel):
    url = CharField(null=True)
    title = CharField(null=True)
    rate = FloatField(default=1.0)
    awards = CharField(null=True)
    year = IntegerField(null=True)
    platform = CharField(default='Movie')
    summary = TextField(null=True)
    is_completed = BooleanField(default=False)

    genre = ForeignKeyField(Genre, backref='movie')
