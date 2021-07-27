import peewee as pw
from playhouse.mysql_ext import MySQLConnectorDatabase
import config


class BaseModel(pw.Model):
    class Meta:
        database = MySQLConnectorDatabase(
                host = config.db_host,
                user = config.db_user,
                password = config.db_password,
                database = config.db_name,
            )


class Stocks(BaseModel):
    chat_id = pw.IntegerField(column_name='chat_id')
    ticker = pw.CharField(max_length= 10, column_name='ticker')
    needed_price = pw.FloatField(column_name='needed_price')

    class Meta:
        primary_key = pw.CompositeKey('chat_id', 'ticker')
        table_name = 'Stocks'
