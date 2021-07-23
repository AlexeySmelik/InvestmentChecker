import peewee as pw
from playhouse.mysql_ext import MySQLConnectorDatabase
import config

class BaseModel(pw.Model):
    class Meta:
        database = MySQLConnectorDatabase(
                host = "localhost",
                user = config.user,
                password = config.password,
                database = "uroki",
            )

class Ticker(BaseModel):
    id = pw.IntegerField(column_name='id')
    code = pw.CharField(max_length= 4, column_name='code')
    cost = pw.FloatField(column_name='cost')

    class Meta:
        primary_key = pw.CompositeKey('id', 'code')
        table_name = 'tickers'

class Code(BaseModel):
    code = pw.CharField(max_length=4, column_name='code', primary_key=True)
    count = pw.IntegerField(column_name='count')

    class Meta:
        table_name = 'codes'