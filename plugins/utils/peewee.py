# -*- coding: utf-8 -*-
from handler.base_plugin import BasePlugin

import peewee
import peewee_async

""" peewee_async
Docs: https://peewee-async.readthedocs.io/en/latest/

peewee
Docs: http://docs.peewee-orm.com/en/latest/
"""


class PeeweePlugin(BasePlugin):
    __slots__ = ("database", "manager", "models")

    def __init__(self, dbname, dbuser, dbpassword, dbhost, custom_driver=None, **kwargs):
        """Adds self to messages and event's `data` field.
        Through this instance you can access peewee_async.Manager instance (data["peewee_async"].manager).
        This plugin should be included first!
        """

        super().__init__()

        # You can replace PostgresqlDatabase with MysqlDatabase or pass driver you want tot use in custom_driver argument

        if custom_driver is None:
            driver = peewee_async.PostgresqlDatabase
        else:
            driver = custom_driver

        self.database = driver(dbname, user=dbuser, password=dbpassword, host=dbhost, **kwagrs)

        self.models = []

        self.create_models()

        self.manager = peewee_async.Manager(self.database)

        database.set_allow_sync(False)

    def create_models(self):
        class TestModel(peewee.Model):
            text = peewee.CharField()

            class Meta:
                database = self.database

        TestModel.create_table(True)
        TestModel.create(text="Yo, I can do it sync!")

        self.models.append(TestModel)

        self.database.close()

    async def global_before_message_checks(self, msg):
        msg.data["peewee_async"] = self

    async def global_before_event_checks(self, evnt):
        evnt.data["peewee_async"] = self
