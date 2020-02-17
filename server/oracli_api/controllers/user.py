from flask import jsonify, make_response, request
from flask_restful import Resource
from bson import json_util
from bson import ObjectId
import json
from pymongo import ReturnDocument

from oracli_api.utils.auth import token_required

import oracli_api


class User(Resource):
    # will get information about the token passed in
    @token_required
    def get(self, data, token):
        # get the current users id
        user_id = {'_id': ObjectId(data.get('_id'))}
        # get the user from the db
        user = oracli_api.mentees.find_one(user_id)
        if user is None:
            user = oracli_api.mentors.find_one(user_id)

        return jsonify(json.loads(json_util.dumps(user)))

    @token_required
    def post(self, data, token):
        # get the current users id
        user_id = {'_id': ObjectId(data.get('_id'))}

        # check to see if the current user is a mentee, and update if so
        updated_user = oracli_api.mentees.find_one_and_update(
            user_id, {'$set': request.get_json()}, return_document=ReturnDocument.AFTER)

        # if they are not a mentee, check if they are a mentor so we can update them accordingly
        if updated_user is None:
            updated_user = oracli_api.mentors.find_one_and_update(
                user_id, {'$set': request.get_json()}, return_document=ReturnDocument.AFTER)

        # if they were not found, return an error message
        if updated_user is None:
            return jsonify({'message': 'user does not exist'})

        # user update was successful, so we can return success message and the updated user
        return jsonify({'message': 'success', 'updated_user': json.loads(json_util.dumps(updated_user))})

    @token_required
    def delete(self, data, token):
        # get the current sessions user id
        user_id = {'_id': ObjectId(data.get('_id'))}

        user = oracli_api.mentees.find_one_and_delete(user_id)

        if user is None:
            user = oracli_api.mentors.find_one_and_delete(user_id)

        if user is None:
            return jsonify({'message': 'user does not exist'})

        return jsonify({'message': 'success', 'deleted_user': json.loads(json_util.dumps(user))})