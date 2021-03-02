from utils.logger import logger
from helpers.mongo_helper import db

import time
import threading
import subprocess

MAX_THREADS = 5


class Queue:

    def __init__(self):
        """
        Inits the queue and a thread pool.

        Args:

        Returns(None):

        """
        self.queue = []
        self.thread_pool = []
        self.lock = threading.Lock()
        threading.Thread(target=self._start_watcher, daemon=True).start()

    def add_task(self, task, index):
        """
        Adds a task to the queue.

        Args:
            - task(tupple): (cmd to execute, index).
            - index(str): Index on the mongodb to save the result.

        Returns(None):

        """
        logger.log_info("Adding task {} to the queue".format(task))
        self.queue.append((task, index))

    def execute_task(self, cmd, index):
        """
        Executes a given task from the queue and saves the result.

        Args:
            - cmd(str):
            - index(str):

        Returns(None):

        """
        logger.log_info("Executing cmd {}".format(cmd))
        output = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        res = "{}\n{}".format(output.stdout, output.stderr)
        logger.log_info("Output is {}".format(res))

        self.lock.acquire()
        logger.log_info("Saving result to db")
        db.save_output(res, index)

        logger.log_info("Destroying thread")
        self.thread_pool.pop()
        self.lock.release()

    def _start_watcher(self):
        """
        Start a process that watch for new tasks to be executed

        Args:

        Returns(None):

        """
        while True:
            if len(self.thread_pool) > MAX_THREADS:
                logger.log_error("Max threads limit {} reached. "
                                 "Waiting".format(MAX_THREADS))
                time.sleep(1)
                continue
            elif len(self.queue) == 0:
                time.sleep(1)
                continue
            task = self.queue.pop(0)
            t = threading.Thread(target=self.execute_task,
                                 args=(task[0],
                                       task[1],),
                                 daemon=True)
            self.thread_pool.append(t)
            t.start()
            time.sleep(0.2)


queue = Queue()
