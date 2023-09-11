from flask import session, request, make_response, jsonify, abort
from flask_restful import Resource
from flask_login import login_user, logout_user, login_required, current_user
from config import db, app, api, login_manager, Migrate
from models import User, Owner, Pet, Adoption, Action, Stat, Strain
import traceback

class Users(Resource):
	def get(self):
		users = [u.to_dict() for u in User.query.all()]
		return make_response(users, 200)
	def post(self):
		userData = request.get_json()
		if not userData:
			return make_response({"error": "invalid user data"}, 400)
		else:
			try:
				new_user = User(
					username=userData['username'],
					email=userData['email'],
					password_hash=userData['password']
				)
				db.session.add(new_user)
				db.session.commit()
				return make_response(new_user.to_dict(), 201)
			except Exception as e:
				return make_response({'error': str(e)}, 500)
api.add_resource(Users, '/users')
class UsersById(Resource):
	def get(self, id):
		user = User.query.filter_by(id=id).first()
		if not user:
			return make_response({"error": "user not found"}, 404)
		else:
			return make_response(user.to_dict(), 200)
	def delete(self, id):
		user = User.query.filter_by(id=id).first()
		if not user:
			return make_response({"error": "user not found"}, 404)
		else:
			db.session.delete(user)
			db.session.commit()
			return make_response({}, 204)
	def patch(self, id):
		user = User.query.filter_by(id=id).first()
		userData = request.get_json()
		if not user:
			return make_response({"error": "user not found"}, 404)
		elif not userData:
			return make_response({"error": "invalid user data"}, 400)
		else:
			try:
				for attr in userData:
					setattr(user, attr, userData[attr])
				db.session.commit()
				return make_response(user.to_dict(),202)
			except Exception as e:
				return make_response({'error':str(e)}, 500)
api.add_resource(UsersById, '/users/<int:id>')
class UsersByUsername(Resource):
	def get(self, username):
		user = User.query.filter_by(username=username).first()
		if not user:
			return make_response({'error': 'user not found'}, 404)
		else:
			return make_response(user.to_dict(), 200)
	def delete(self, username):
		user = User.query.filter_by(username=username).first()
		if not user:
			return make_response({'error': 'user not found'}, 404)
		else:
			db.session.delete(user)
			db.session.commit()
			return make_response({}, 204)
	def patch(self, username):
		user = User.query.filter_by(username=username).first()
		userData = request.get_json()
		if not user:
			return make_response({'error': 'user not found'}, 404)
		elif not userData:
			return make_response({'error': 'invalid user data'}, 400)
		else:
			try:
				for attr in userData:
					setattr(user, attr, userData[attr])
				db.session.commit()
				return make_response(user.to_dict(), 202)
			except Exception as e:
				return make_response({'error': str(e)}, 500)
api.add_resource(UsersByUsername, '/users/<string:username>')

class Owners(Resource):
	def get(self):
		owners = [o.to_dict() for o in Owner.query.all()]
		return make_response(owners, 200)
	def post(self):
		ownerData = request.get_json()
		if not ownerData:
			return make_response({"error": "invalid owner data"}, 400)
		else:
			try:
				new_owner = Owner(
					user_id=ownerData['user_id'],
					first_name=ownerData['first_name'],
					last_name=ownerData['last_name'],
					profile_url=ownerData['profile_url'],
					city=ownerData['city'],
					bio=ownerData['bio']
				)
				db.session.add(new_owner)
				db.session.commit()
				return make_response(new_owner.to_dict(), 201)
			except Exception as e:
				return make_response({'error': str(e)}, 500)
api.add_resource(Owners, '/owners')
class OwnersById(Resource):
	def get(self, id):
		owner = Owner.query.filter_by(id=id).first()
		if not owner:
			return make_response({'error': 'owner not found'}, 404)
		else:
			return make_response(owner.to_dict(), 200)
	def delete(self, id):
		owner = Owner.query.filter_by(id=id).first()
		if not owner:
			return make_response({'error': 'owner not found'}, 404)
		else:
			db.session.delete(owner)
			db.session.commit()
			return make_response({}, 204)
	def patch(self, id):
		owner = Owner.query.filter_by(id=id).first()
		ownerData = request.get_json()
		if not owner:
			return make_response({'error': 'owner not found'}, 404)
		elif not ownerData:
			return make_response({'error': 'invalid owner data'}, 400)
		else:
			try:
				for attr in ownerData:
					setattr(owner, attr, ownerData[attr])
				db.session.commit()
				return make_response(owner.to_dict(), 202)
			except Exception as e:
				return make_response({'error': str(e)}, 500)
api.add_resource(OwnersById, '/owners/<int:id>')
# class OwnersByUserId(Resource):
#     def get(self, user_id):
#         owner = User.query.filter_by(id=user_id).first.owner
#         if not owner:
#             return make_response({'errror': 'owner not found'}, 404)
#         else:
#             return make_response(owner.to_dict(), 200)
# api.add_resource(OwnersByUserId, '/owners/<string:username>')

class Pets(Resource):
	def get(self):
		pets = [p.to_dict() for p in Pet.query.all()]
		return make_response(pets, 200)
	def post(self):
		petData = request.get_json()
		if not petData:
			return make_response({'error': 'invalid pet data'}, 400)
		else:
			try:
				new_pet = Pet(
					name=petData['name'],
					factor=petData['factor'],
					strain_id=petData['strain_id'],
				)
				db.session.add(new_pet)
				db.session.commit()
				return make_response(new_pet.to_dict(), 201)
			except Exception as e:
				return make_response({'error': str(e)}, 500)
api.add_resource(Pets, '/pets')
class PetsById(Resource):
	def get(self, id):
		pet = pet.query.filter_by(id=id).first()
		if not pet:
			return make_response({'error': 'pet not found'}, 404)
		else:
			return make_response(pet.to_dict(), 200)
	def delete(self, id):
		pet = pet.query.filter_by(id=id).first()
		if not pet:
			return make_response({'error': 'pet not found'}, 404)
		else:
			db.session.delete(pet)
			db.session.commit()
			return make_response({}, 204)
	def patch(self, id):
		pet = Pet.query.filter_by(id=id)
		petData = request.get_json()
		if not pet:
			return make_response({'error': 'pet not found'}, 404)
		elif not petData:
			return make_response({'error': 'invalid pet data'}, 400)
		else:
			try:
				for attr in petData:
					setattr(pet, attr, petData[attr])
				db.session.commit()
				return make_response(pet.to_dict(), 202)
			except Exception as e:
				return make_response({'error': str(e)}, 500)
api.add_resource(PetsById, '/pets/<int:id>')

class StrainsByName(Resource):
	def get(self, name):
		strain = Strain.query.filter_by(name=name).first()
		if not strain:
			return make_response({'error': 'strain not found'}, 404)
		else:
			return make_response(strain.to_dict(), 200)
	def delete(self, name):
		strain = Strain.query.filter_by(name=name).first()
		if not strain:
			return make_response({'error': 'strain not found'}, 404)
		else:
			db.session.delete(strain)
			db.session.commit()
			return make_response({}, 204)
	def patch(self, name):
		strain = Strain.query.filter_by(name=name).first()
		strainData = request.get_json()
		if not strain:
			return make_response({'error': 'strain not found'}, 404)
		elif not strainData:
			return make_response({'error': 'invalid strain data'}, 400)
		else:
			try:
				for attr in strainData:
					setattr(strain, attr, strainData[attr])
				db.session.commit()
				return make_response(strain.to_dict, 202)
			except Exception as e:
				return make_response({'error': str(e)}, 500)
api.add_resource(StrainsByName, '/strains/<string:name>')




if __name__ == '__main__':
    app.run(port=5656, debug=True)