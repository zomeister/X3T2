from flask import session, request, make_response, jsonify, abort
from flask_restful import Resource
from flask_login import login_user, logout_user, login_required, current_user
from config import db, app, api, login_manager, Migrate
from models import Message, Thread, Post, Friendship, Menu
from models import User, Owner, Pet, Adoption, Action, Stat, Strain
import traceback

@app.route('/')
def index():
    return '<h1>Welcome to the Xeo Pets!</h1>'
# -------- AUTH -------- () ---- #
@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=int(user_id)).first()
# -------- SIGNUP, LOGIN, LOGOUT -------- () ---- #
class Register(Resource):
    def post(self):
        userData = request.get_json()
        if not userData:
            return make_response({"error": "invalid user data"}, 400)
        try:
            new_user = User(
                username=userData['username'],
                email=userData['email'],
            )
            new_user.password_hash = userData['password']
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            return make_response(new_user.to_dict(), 201)
        except Exception as e:
            return make_response({"error": str(e)}, 500)
api.add_resource(Register, '/register')
class Login(Resource):
    def post(self):
        userData = request.get_json()
        if not userData:
            return make_response({"error": "invalid user data"}, 400)
        username = userData['username']
        password = userData['password']
        user = User.query.filter_by(username=username).first()
        if not user:
            return make_response({"error": "user not found"}, 404)
        elif user.authenticate(password):
            # login_user(new_user, remember=True)
            session['user_id'] = user.id
            return make_response(user.to_dict(rules=('-_password_hash',)), 200)
        else:
            return make_response({"error": "invalid username or password"}, 401)
api.add_resource(Login, '/login')
class Logout(Resource):
    @login_required
    def delete(self):
        try:
            session['user_id'] = None
            # logout_user()
            return make_response({}, 204)
        except Exception as e:
            return {"error": str(e)}, 500
api.add_resource(Logout, '/logout')
class CheckSession(Resource):
    def get(self):
        user = User.query.filter_by(id=session['user_id']).first()
        if not user:
            return make_response({"error": "user not in session"}, 404)
        else:
            return make_response(user.to_dict(), 200)
api.add_resource(CheckSession, '/check_session')
# -------- ALLPETS, MYPETS, MYPET -------- () ---- #
class Shelter(Resource):
    def get(self):
        shelter_pets = [p.to_dict() for p in Pet.query.filter(Pet.adoptions==None).all()]
        return make_response(shelter_pets, 200)
    def post(self):
        petData = request.get_json()
        if not petData:
            return make_response({'error': 'invalid pet data'}, 400)
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
api.add_resource(Shelter, '/shelter')
class MyPets(Resource):
    @login_required
    def get(self):
        user_id = session['user_id']
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return make_response({"error": "user not found"}, 404)
        else:
            my_pets = [a.pet.to_dict() for a in Adoption.query.filter(Adoption.owner_id==user.id).all()]
            return make_response(my_pets, 200)
api.add_resource(MyPets, '/mypets')
class MyPetsById(Resource):
    @login_required
    def get(self, id):
        user_id = session['user_id']
        user = User.query.filter_by(id=user_id).first()
        my_adoption = Adoption.query.filter((Adoption.owner_id==user_id) & (Adoption.pet_id==id)).first()
        if not user:
            return make_response({"error": "user not found"}, 404)
        elif not my_adoption:
            return make_response({"error": "adoption/pet not found"}, 404)
        else:
            return make_response(my_adoption.pet.to_dict(only=('adoptions.id', 'adoptions.actions', 'factor', 'strain', 'name', 'id', )), 200)
    @login_required
    def delete(self, id):
        user_id = session['user_id']
        user = User.query.filter_by(id=user_id).first()
        my_adoption = Adoption.query.filter((Adoption.owner_id==user_id) & (Adoption.pet_id==id)).first()
        if not user:
            return make_response({"error": "user not found"}, 404)
        elif not my_adoption:
            return make_response({"error": "adoption/pet not found"}, 404)
        else:
            try:
                db.session.delete(my_adoption)
                db.session.commit()
                return make_response({}, 204)
            except Exception as e:
                return make_response({"error": str(e)}, 500)
    @login_required
    def post(self, id):
        user_id = session['user_id']
        user = User.query.filter_by(id=user_id).first()
        adoptionData = request.get_json()
        if not user:
            return make_response({"error": "user not found"}, 404)
        elif not adoptionData:
            return make_response({"error": "invalid adoption data"}, 400)
        else:
            try:
                new_adoption = Adoption(
                    owner_id=user_id,
                    pet_id=id,
				)
                db.session.add(new_adoption)
                db.session.commit()
                return make_response(new_adoption.to_dict(), 201)
            except Exception as e:
                return make_response({"error": str(e)}, 500)
api.add_resource(MyPetsById, '/mypets/<int:id>')
class MyPetStats(Resource):
    @login_required
    def get(self, id):
        user_id = session['user_id']
        user = User.query.filter_by(id=user_id).first()
        my_adoption = Adoption.query.filter((Adoption.owner_id==user.id) & (Adoption.pet_id==id)).first()
        if not user:
            return make_response({"error": "user not found"}, 404)
        if not my_adoption:
            return make_response({"error": "adoption not found"}, 404)
        else:
            return make_response(my_adoption.pet.stat.to_dict(), 200)
    @login_required
    def patch(self, id):
        stat = Stat.query.filter_by(pet_id=id).first()
        statData = request.get_json()
        if not stat:
            return make_response({'error':'stat not found'}, 404)
        elif not statData:
            return make_response({'error': 'invalid stat data'}, 400)
        else:
            try:
                for attr in statData:
                    setattr(stat, attr, statData[attr])
                db.session.commit()
                return make_response(stat.to_dict(), 202)
            except Exception as e:
                return make_response({'error': str(e)}, 500)
api.add_resource(MyPetStats, '/mypets/stats/<int:id>')
class MyPetsStats(Resource):
    @login_required
    def get(self):
        user_id = session['user_id']
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return make_response({"error": "user not found"}, 404)
        else:
            my_petstats = [a.pet.stat.to_dict() for a in Adoption.query.filter(Adoption.owner_id==user.id).all()]
            return make_response(my_petstats, 200)
api.add_resource(MyPetsStats, '/mypets/stats')
class Profile(Resource):
    @login_required
    def get(self):
        user_id = session.get('user_id')
        owner = Owner.query.filter_by(id=user_id).first()
        if not owner:
            return make_response({"error": "user/owner not found"}, 404)
        else:
            return make_response(owner.to_dict(), 200)
    @login_required
    def post(self):
        user_id = session.get('user_id')
        ownerData = request.get_json()
        if not ownerData:
            return make_response({'error': 'invalid owner data'}, 400)
        try:
            new_owner = Owner(
				first_name=ownerData['first_name'],
				last_name=ownerData['last_name'],
                bio=ownerData['bio'],
                profile_url=ownerData['profile_url'],
                city=ownerData['city'],
                user_id=user_id
			)
            db.session.add(new_owner)
            db.session.commit()
            return make_response(new_owner.to_dict(), 201)
        except Exception as e:
            return make_response({'error': str(e)}, 500)
    @login_required
    def patch(self):
        user_id = session.get('user_id')
        owner = Owner.query.filter_by(user_id=user_id).first()
        ownerData = request.get_json()
        if not owner:
            return make_response({"error": "owner not found"}, 404)
        elif not ownerData:
            return make_response({'error': 'invalid owner data'}, 400)
        try:
            for attr in ownerData:
                setattr(owner, attr, ownerData[attr])
            db.session.commit()
            return make_response(owner.to_dict(), 202)
        except Exception as e:
            return make_response({'error': str(e)}, 500)
api.add_resource(Profile, '/profile')
class Friends(Resource):
    @login_required
    def get(self):
        user_id = session.get('user_id')
        friendships = [f.to_dict() for f in Friendship.query.filter(Friendship.req_user_id==user_id or Friendship.rec_user_id==user_id).all()]
        return make_response(friendships, 200)
    @login_required
    def post(self):
        user_id = session.get('user_id')
        user = User.query.filter_by(id=user_id).first()
        friendshipData = request.get_json()
        if not user:
            return make_response({"error": "user not found"}, 404)
        elif not friendshipData:
            return make_response({"error": "invalid friendship data"}, 400)
        try:
            new_friendship = Friendship(
                req_user_id=user_id,
                rec_user_id=friendshipData['rec_user_id'],
                status=friendshipData['status']
			)
            db.session.add(new_friendship)
            db.session.commit()
            return make_response(new_friendship.to_dict(), 201)
        except Exception as e:
            return make_response({'error': str(e)}, 500)
api.add_resource(Friends, '/friends')
class Friend(Resource):
    @login_required
    def get(self, username):
        user_id = session.get('user_id')
        friendship = Friendship.query.filter((Friendship.req_user_id==user_id or Friendship.rec_user_id==user_id) and (Friendship.req_user.username==username or Friendship.rec_user.username==username)).first()
        if not friendship:
            return make_response({"error": "friendship not found"}, 404)
    @login_required
    def delete(self, username): # remove friend
        user_id = session.get('user_id')
        friendship = Friendship.query.filter((Friendship.req_user_id==user_id or Friendship.rec_user_id==user_id) and (Friendship.req_user.username==username or Friendship.rec_user.username==username)).first()
        if not friendship:
            return make_response({"error": "friendship not found"}, 404)
        else:
            db.session.delete(friendship)
            db.session.commit()
            return make_response({}, 204)
api.add_resource(Friend, '/friends/<string:username>')

class Threads(Resource):
    @login_required
    def get(self):
        pass
    @login_required
    def post(self):
        pass
api.add_resource(Threads, '/threads')
class FriendThread(Resource):
    @login_required
    def get(self, username):
        pass
    @login_required
    def patch(self, username):
        pass
api.add_resource(FriendThread, '/threads/<string:username>')






class Messages(Resource):
    def get(self, username):
        pass
    def post(self, username):
        pass
api.add_resource(Messages, '/messages/<string:username>')






class MenusById(Resource):
    def get(self, id):
        pass
api.add_resource(MenusById, '/menus/<int:id>')


class MyAdoptions(Resource):
    def get(self):
        pass
    def post(self):
        pass
api.add_resource(MyAdoptions, '/my_adoptions')
class MyAdoptionsById(Resource):
    def get(self, id):
        pass
    def delete(self, id):
        pass
    def patch(self, id):
        pass
api.add_resource(MyAdoptionsById, '/my_adoptions/<int:id>')

# -------- GENERAL -------- () ---- #
class Users(Resource): # DONE (get)
	def get(self):
		users = [u.to_dict() for u in User.query.all()]
		return make_response(users, 200)
api.add_resource(Users, '/users')
class UsersById(Resource): # DONE (get, delete, patch)
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
class UsersByUsername(Resource): # DONE (delete, patch)
	def get(self, username):
		user = User.query.filter_by(username=username).first()
		if not user:
			return make_response({"error": "user not found"}, 404)
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
api.add_resource(UsersByUsername, '/<string:username>/user')

class Owners(Resource): # DONE (get)
	def get(self):
		owners = [o.to_dict() for o in Owner.query.all()]
		return make_response(owners, 200)

api.add_resource(Owners, '/owners')
class OwnersById(Resource): # DONE (get, delete, patch)
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
api.add_resource(OwnersById, '/owners/<int:id>')
class OwnersByUsername(Resource): # DONE (get)
    def get(self, username):
        user = User.query.filter_by(username=username).first()
        if not user:
            return make_response({'errror': 'user not found'}, 404)
        else:
            owner = Owner.query.filter_by(id=user.id).first()
            try:
                return make_response(owner.to_dict(), 200)
            except Exception as e:
                return make_response({'error': str(e)}, 500)
api.add_resource(OwnersByUsername, '/<string:username>/owner')

class Pets(Resource): # DONE (get)
	def get(self):
		pets = [p.to_dict() for p in Pet.query.all()]
		return make_response(pets, 200)
api.add_resource(Pets, '/pets')
class PetsById(Resource): # DONE (get, delete, patch)
	def get(self, id):
		pet = Pet.query.filter_by(id=id).first()
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
class PetsByUsername(Resource): # DONE (get)
    def get(self, username):
        user = User.query.filter_by(username=username).first()
        if not user:
            return make_response({'error': 'user not found'}, 404)
        else:
            owner = Owner.query.filter_by(id=user.id).first()
            try:
                adoption_pets = [a.pet.to_dict() for a in Adoption.query.filter_by(owner_id=owner.id).all()]
                return make_response(adoption_pets, 200)
            except Exception as e:
                return make_response({'error': str(e)}, 500)
api.add_resource(PetsByUsername, '/<string:username>/pets')

class Stats(Resource): # DONE (get, post)
	def get(self):
		stats = [s.to_dict() for s in Stat.query.all()]
		return make_response(stats, 200)
	def post(self):
		statData = request.get_json()
		if not statData:
			return make_response({'error': 'invalid stat data'}, 400)
		else:
			try:
				stat = Stat(
					happiness=statData['happiness'],
					health=statData['health'],
					hunger=statData['hunger'],
					pet_id=statData['pet_id']
				)
				db.session.add(stat)
				db.session.commit()
				return make_response(stat.to_dict(), 201)
			except Exception as e:
				return make_response({'error': str(e)}, 500)
api.add_resource(Stats, '/stats')
class StatsById(Resource): # DONE (delete)
    def delete(self, id):
        stat = Stat.query.filter_by(id=id).first()
        if not stat:
            return make_response({'error':'stat not found'}, 404)
        else:
            db.session.delete(stat)
            db.session.commit()
            return make_response({}, 204)
api.add_resource(StatsById, '/stats/<int:id>')

class Strains(Resource): # DONE (get, post)
    def get(self):
        strains = [s.to_dict() for s in Strain.query.all()]
        return make_response(strains, 200)
    def post(self):
        strainData = request.get_json()
        if not strainData:
            return make_response({'error': 'invalid strain data'}, 400)
        else:
            try:
                strain = Strain(name=strainData['name'], emoji=strainData['emoji'])
                db.session.add(strain)
                db.session.commit()
                return make_response(strain.to_dict(), 201)
            except Exception as e:
                return make_response({'error': str(e)}, 500)
api.add_resource(Strains, '/strains')
class StrainsById(Resource): # DONE (get, delete, patch)
	def get(self, id):
		strain = Strain.query.filter_by(id=id).first()
		if not strain:
			return make_response({'error': 'strain not found'}, 404)
		else:
			return make_response(strain.to_dict(), 200)
	def delete(self, id):
		strain = Strain.query.filter_by(id=id).first()
		if not strain:
			return make_response({'error': 'strain not found'}, 404)
		else:
			db.session.delete(strain)
			db.session.commit()
			return make_response({}, 204)
	def patch(self, id):
		strain = Strain.query.filter_by(id=id).first()
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
api.add_resource(StrainsById, '/strains/<int:id>')
class StrainsByName(Resource): # DONE (get, delete, patch)
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

class Adoptions(Resource): # DONE (get, post)
	def get(self):
		adoptions = [a.to_dict() for a in Adoption.query.all()]
		return make_response(adoptions, 200)
	def post(self):
		adoptionData = request.get_json()
		if not adoptionData:
			return make_response({'error': 'invalid adoption data'}, 400)
		try:
			new_adoption = Adoption(
				owner_id=adoptionData['owner_id'],
				pet_id=adoptionData['pet_id']
			)
			db.session.add(new_adoption)
			db.session.commit()
			return make_response(new_adoption.to_dict(), 201)
		except Exception as e:
			return make_response({'error': str(e)}, 500)
api.add_resource(Adoptions, '/adoptions')
class AdoptionsById(Resource): # DONE (get, delete, patch)
	def get(self, id):
		adoption = Adoption.query.filter_by(id=id).first()
		if not adoption:
			return make_response({'error':'adoption not found'}, 404)
		else:
			return make_response(adoption.to_dict() , 200)
	def delete(self, id):
		adoption = Adoption.query.filter_by(id=id).first()
		if not adoption:
			return make_response({'error':'adoption not found'}, 404)
		else:
			db.session.delete(adoption)
			db.session.commit()
			return make_response({} , 204)
	def patch(self, id):
		adoption = Adoption.query.filter_by(id=id).first()
		adoptionData = request.get_json()
		if not adoption:
			return make_response({'error':'adoption not found'}, 404)
		elif not adoptionData:
			return make_response({'error': 'invalid adoption data'}, 400)
		else:
			try:
				for attr in adoptionData:
					setattr(adoption, attr, adoptionData[attr])
				db.session.commit()
				return make_response({} , 204)
			except Exception as e:
				return make_response({'error': str(e)}, 500)
api.add_resource(AdoptionsById, '/adoptions/<int:id>')
class AdoptionsByUsername(Resource): # DONE (get)
    def get(self, username):
        user = User.query.filter_by(username=username).first()
        if not user:
            return make_response({'error': 'user not found'}, 404)
        else:
            owner = Owner.query.filter_by(id=user.id).first()
            try:
                adoptions = [a.to_dict() for a in Adoption.query.filter_by(owner_id=owner.id).all()]
                return make_response(adoptions, 200)
            except Exception as e:
                return make_response({'error': str(e)}, 500)
api.add_resource(AdoptionsByUsername, '/<string:username>/adoptions')

class Actions(Resource): # DONE (get, post)
	def get(self):
		actions = [a.to_dict() for a in Action.query.all()]
		return make_response(actions, 200)
	def post(self):
		actionData = request.get_json()
		if not actionData:
			return make_response({'error': 'invalid action data'}, 400)
		try:
			new_action = Action(
				name=actionData['name'],
                adoption_id=actionData['adoption_id']
			)
			db.session.add(new_action)
			db.session.commit()
			return make_response(new_action.to_dict(), 201)
		except Exception as e:
			return make_response({'error': str(e)}, 500)
api.add_resource(Actions, '/actions')
class ActionsById(Resource): # DONE (get, delete, patch)
	def get(self, id):
		action = Action.query.filter_by(id=id).first()
		if not action:
			return make_response({'error':'action not found'}, 404)
		else:
			return make_response(action.to_dict() , 200)
	def delete(self, id):
		action = Action.query.filter_by(id=id).first()
		if not action:
			return make_response({'error':'action not found'}, 404)
		else:
			db.session.delete(action)
			db.session.commit()
			return make_response({} , 204)
	def patch(self, id):
		action = Action.query.filter_by(id=id).first()
		actionData = request.get_json()
		if not action:
			return make_response({'error':'action not found'}, 404)
		elif not actionData:
			return make_response({'error': 'invalid action data'}, 400)
		else:
			try:
				for attr in actionData:
					setattr(action, attr, actionData[attr])
				db.session.commit()
				return make_response({} , 204)
			except Exception as e:
				return make_response({'error': str(e)}, 500)
api.add_resource(ActionsById, '/actions/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)