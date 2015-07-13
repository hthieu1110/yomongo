# -*- coding: utf-8 -*-
from exceptions import ClientError, DbError
from pymongo.mongo_client import MongoClient


class _ConnectedDbs(dict):
    """Custom dict for holding connected DBs

    :raise: YoDbError if DB not found in connection DBs
    :return: (object) A Mongo Database instance
    """
    def __getitem__(self, item):
        if item in self:
            return super(_ConnectedDbs, self).__getitem__(item)
        raise DbError("Db '{}' is not defined".format(item))


class Client(object):
    """Main entry point of YoMongo, this class must be instantiated
    before definition of models.
    """
    default_db_name = None
    default_db = None
    connected_databases = _ConnectedDbs()

    def __init__(self, config):
        """Initialize YoClient

        :param config: config for Mongo DBs
        :type config: dict
        """
        self.config = config
        self._connect_dbs()

    def _connect_dbs(self):
        """Connect to defined DBs
        If only one DB is defined then it's the default DB
        If many DBs are defined then we must precised which one is default

        TODO: lazy connect when db is called
        """
        for db, conf in self.config.items():
            if db not in self.connected_databases:
                host = conf['host']
                ssl = conf.get('ssl', False)
                mongo_client = MongoClient(host=host, ssl=ssl, tz_aware=True)
                db_cursor = mongo_client[db]

                # Authenticate
                if conf['user'] and conf['password']:
                    db_cursor.logout()
                    db_cursor.authenticate(name=conf['user'], password=conf['password'])

                if len(self.config) == 1 or conf.get('default'):
                    self.__class__.default_db = db_cursor
                    self.__class__.default_db_name = db
                self.__class__.connected_databases[db] = db_cursor

        if not self.default_db:
            raise ClientError('You must define one default DB in case of multi DBs')

    def list_dbs(self):
        """List all the defined DBs

        :return: (list) list of defined DBs
        """
        return self.config.keys()

    def list_collections(self, db_name=None, include_system_collections=False):
        """List all the collections of a given DB

        :param db_name: database in use for listing collections,
                        if db_name is not precised then take the default DB
        :type db_name: str

        :param include_system_collections: list system collections or not
        :type include_system_collections: bool

        :return: (list) list of collections names
        """
        return self.__class__.connected_databases[db_name or self.default_db_name]\
            .collection_names(include_system_collections)
