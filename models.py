from peewee import PostgresqlDatabase, Model, CharField, IntegerField, BooleanField, ForeignKeyField, fn # type: ignore

#  Database Configuration 
db = PostgresqlDatabase(
    'testdb',  # Replace with your database name
    user='postgres',
    password='',  # Add if needed
    host='localhost',
    port=5432
)

# Define Models 
class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    first_name = CharField()
    last_name = CharField()
    street_address = CharField(null=True)
    city = CharField(null=True)
    state = CharField(null=True)
    zip_code = CharField(null=True)
    volunteer = BooleanField(null=True)

class Need(BaseModel):
    type = CharField()
    priority = IntegerField()
    requester = ForeignKeyField(User, backref='needs')

class Resource(BaseModel):
    description = CharField()
    provider = ForeignKeyField(User, backref='resources')
    type = CharField()
    street_address = CharField()
    city = CharField()
    state = CharField()
    zip_code = CharField()

class Service(BaseModel):
    type = CharField()
    availability = IntegerField()
    provider = ForeignKeyField(User, backref='services')