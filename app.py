from utils.logger import logger
from helpers.mongo_helper import db
from helpers.queue import queue

from flask import request, Flask, jsonify

PORT = 11000
api = Flask(__name__)


@api.route('/new_task', methods=['POST'])
def new_task():
    """
    Adds a new task to the database and to a queue.

    Args:

    Returns(dict):
        {'id': _id}

    """
    data = request.json
    cmd = data.get('cmd')
    if not cmd:
        return jsonify({'error': 'cmd field is not present'})
    _id = db.add_task(cmd)
    queue.add_task(cmd, _id)
    return jsonify({"id": str(_id)})


@api.route('/get_output/<_id>', methods=['GET'])
def get_output(_id):
    """
    Gets the output of a given index.

    Args:
        - _id(int)

    Returns(dict)
        {'output': output}

    """
    output = db.get_output(_id)
    if not output:
        return jsonify({'error': "id {} not found".format(_id)})
    return jsonify({"output": output.get('output')})


if __name__ == '__main__':
    logger.log_info("Running on localhost:{}".format(PORT))
    api.run(port=PORT, host='0.0.0.0')
