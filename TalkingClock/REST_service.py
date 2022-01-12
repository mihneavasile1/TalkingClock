#!/usr/bin/env python
import argparse
from datetime import datetime
from flask import Flask
from flask_restful import Resource, Api

from TalkingClock.TalkClock import make_clock_talk

# if ModuleNotFoundError run:
# export PYTHONPATH="${PYTHONPATH}:~/TalkingClockLloyds/TalkingClock/"

app = Flask(__name__)

api = Api(app)


class HumanFriendlyTime(Resource):
    def get(self):
        return make_clock_talk(datetime.now(), json="on")


api.add_resource(HumanFriendlyTime, '/')

if __name__ == '__main__':
    app.run(debug=True)
