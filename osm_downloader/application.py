import logging
import json

import flask
from flask import request, Response

import boto3

application = flask.Flask(__name__)
application.config.from_object('default_config')

@application.route('/download-feature', methods=['POST'])
    def download_feature():
        print(request.json)


if __name__ == '__main__':
    application.run(host='0.0.0.0')