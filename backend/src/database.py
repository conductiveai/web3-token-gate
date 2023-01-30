import datetime

from peewee import Model, PostgresqlDatabase

from settings import settings

db = PostgresqlDatabase(
    database=settings.database_name,
    user=settings.database_user,
    password=settings.database_password.get_secret_value(),
    host=settings.database_host,
    port=settings.database_port,
)


class BaseModel(Model):

    class Meta:
        database = db

    def save(self, force_insert=False, only=None):

        if 'updated_at' in self.__data__:
            self.updated_at = datetime.datetime.now()

        return super().save(force_insert=force_insert, only=only)

    @classmethod
    def update(cls, __data=None, **update):
        if hasattr(cls, 'updated_at') and 'updated_at' not in update:
            update['updated_at'] = datetime.datetime.now()

        return super().update(__data, **update)
