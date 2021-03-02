from utils.logger import logger

from pymongo import MongoClient
from bson.objectid import ObjectId


class MyMongo:

    def __init__(self, name='cmds', collection='tasks'):
        """
        Inits a MongoDb db. Is the db already exists, does nothing.

        Args:
            - name(str): Database name.
            - collection(str): Collections name.

        Returns(None):

        """
        logger.log_info("Creating database {}".format(name))
        self.client = MongoClient()
        logger.log_info("Client: {}".format(self.client))
        self.db = self.client[name]
        self.collection = self.db[collection]

    def add_task(self, cmd):
        """
        Add a new task to the database.

        Args:
            - cmd(str): cmd to add to the database.

        Returns(str):
            Returns the index of the new entry.

        """
        logger.log_info("Inserting new cmd: {}".format(cmd))
        new_entry = {'cmd': cmd}
        res = self.collection.insert_one(new_entry)
        index = res.inserted_id

        logger.log_info("New entry {} created with index {}".format(new_entry,
                                                                    index))
        return index

    def save_output(self, output, index):
        """
        Add the output of an specific cmd on the database.

        Args:
            - output(str):
            - index(str): Index of the saved task

        Returns(None):

        """
        logger.log_info("Saving output {} with index {}".format(output, index))
        self.collection.find_one_and_update({"_id": ObjectId(index)},
                                            {"$set": {"output": output}})

    def get_output(self, index):
        """
        Returns the output of an specific cmd based on the index.

        Args:
            - index(str):

        Returns(dict| None):
            {"output": output}

        """
        logger.log_info("Finding element {}".format(index))
        try:
            return self.collection.find_one({"_id": ObjectId(index)})
        except Exception as e:
            logger.log_error("Error getting output: {}".format(e))
            return None


db = MyMongo()
