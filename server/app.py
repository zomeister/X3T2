from flask import session, request, make_response, jsonify, abort
from flask_restful import Resource
from flask_login import login_user, logout_user, login_required, current_user
from config import db, app, api, login_manager, Migrate
from models import User, Owner, Pet, Adoption, Action, Stat, Strain
import traceback

if __name__ == '__main__':
    app.run(port=5555, debug=True)