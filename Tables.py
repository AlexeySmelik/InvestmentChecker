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

class Stocks(BaseModel):
    chat_id = pw.IntegerField(column_name='chat_id')
    ticker = pw.CharField(max_length= 4, column_name='ticker')
    needed_price = pw.FloatField(column_name='needed_price')

    class Meta:
        primary_key = pw.CompositeKey('chat_id', 'ticker')
        table_name = 'Stocks'
        