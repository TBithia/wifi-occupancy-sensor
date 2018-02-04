
from flask_restful import reqparse

def gen_parser(*args):
    parser = reqparse.RequestParser()
    for arg in args:
        parser.add_argument(**arg)
    return parser



