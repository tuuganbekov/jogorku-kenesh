import peewee
from decouple import config

db = peewee.PostgresqlDatabase(config('DB_NAME'), host=config('HOST'), port=config('PORT'),
                               user=config('DBUSER'), password=config('PASSWORD'))


class Person(peewee.Model):
    name = peewee.TextField()
    info = peewee.TextField()
    phone = peewee.TextField()
    image_link = peewee.TextField()

    class Meta:
        database = db
        db_table = 'deputies'

db.create_tables([Person])
