from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.associationproxy import association_proxy
from config import db, bcrypt

class Friendship(db.Model, SerializerMixin):
    __tablename__ = 'friendships'
    id = db.Column(db.Integer, primary_key=True)
    req_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    rec_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    status = db.Column(db.String)
    
class User(db.Model, UserMixin, SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    # local columns
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    _password_hash = db.Column(db.String)
    # foreign keys
    # serialize
    serialize_rules = ( )
    # represent
    def __repr__(self):
        return f"<User(name:{self.username}, email:{self.email})>"
    # relate
    friend_reqs = db.relationship('Friendship', foreign_keys=[Friendship.req_user_id], backref='req_user', cascade='all, delete-orphan')
    friend_recs = db.relationship('Friendship', foreign_keys=[Friendship.rec_user_id], backref='rec_user', cascade='all, delete-orphan')
    owner = db.relationship('Owner', back_populates='user')
    req = association_proxy('friend_reqs', 'rec_user')
    rec = association_proxy('friend_recs', 'req_user')
    # validate
    @validates('username')
    def validate_username(self, key, new_username):
        if not 3 <= len(new_username) <= 30:
            raise ValueError('username length domain: [3, 30]')
        return new_username
    @validates('email')
    def validate_name(self, key, new_email):
        if not len(new_email) > 4 and '@' in new_email and '.' in new_email:
            raise ValueError('email must include @ and . characters')
        return new_email
    # auth
    @hybrid_property
    def password_hash(self):
        return self._password_hash
        
    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))

    

class Owner(db.Model, SerializerMixin):
    __tablename__ = 'owners'
    id = db.Column(db.Integer, primary_key=True)
    # local columns
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    # username = db.Column(db.String, unique=True)
    profile_url = db.Column(db.String)
    city = db.Column(db.String)
    bio = db.Column(db.String)
    # foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # serialize
    serialize_rules = ('-user', '-adoptions.owner', )
    # represent
    def __repr__(self):
        return f"<Owner(username:{self.username}, name: {self.first_name} {self.last_name}, loc:{self.city}, bio{self.bio})>"
    # relate
    user = db.relationship('User', back_populates='owner', uselist=False)
    adoptions = db.relationship('Adoption', back_populates='owner', cascade='all, delete-orphan')
    pets = association_proxy('adoptions', 'pet')
    # validate
    @validates('first_name', 'last_name')
    def validate_name(self, key, new_name):
        if not 1 <= len(new_name) <= 16:
            raise ValueError('name length domain: [1:16]')
        return new_name
    @validates('profile_url')
    def validate_url(self, key, new_url):
        if not 1 <= len(new_url) <= 4000:
            raise ValueError('photo url too long')
        return new_url
    @validates('bio')
    def validate_bio(self, key, new_bio):
        if not 1 <= len(new_bio) <= 4000:
            raise ValueError('bio too long')
        return new_bio

class Pet(db.Model, SerializerMixin):
    __tablename__ = 'pets'
    id = db.Column(db.Integer, primary_key=True)
    # local columns
    name = db.Column(db.String, nullable=False)
    factor = db.Column(db.Integer, nullable=False, default=100)
    # foreign keys
    strain_id = db.Column(db.Integer, db.ForeignKey('strains.id'))
    # serialize
    serialize_rules = ('-stat', '-strain.pets', '-adoptions.pet', )
    # represent
    def __repr__(self):
        return f"<Pet(name:{self.name}, factor:{self.factor})>"
    # relate
    stat = db.relationship('Stat', back_populates='pet', uselist=False)
    strain = db.relationship('Strain', back_populates='pets')
    adoptions = db.relationship('Adoption', back_populates='pet', cascade='all, delete-orphan')
    owners = association_proxy('adoptions', 'owner')
    # validate
    @validates('name')
    def validate_name(self, key, new_name):
        if not 1 <= len(new_name) <= 16:
            raise ValueError('name length domain: [1:16]')
        return new_name
    @validates('factor')
    def validate_factor(self, key, new_factor):
        if not 1 <= int(new_factor) <= 100:
            raise ValueError('Factor domain: [1:100]')
        return new_factor
    
class Adoption(db.Model, SerializerMixin):
    __tablename__ = 'adoptions'
    id = db.Column(db.Integer, primary_key=True)
    # local columns
    username = db.Column(db.String)
    # foreign keys
    owner_id = db.Column(db.Integer, db.ForeignKey('owners.id'))
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'))
    # serialize
    serialize_rules = ('-actions.adoption', '-owner.adoptions', '-pet.adoptions', )
    # represent
    def __repr__(self):
        return f"<>"
    # relate
    actions = db.relationship('Action', back_populates='adoption')
    owner = db.relationship('Owner', back_populates='adoptions')
    pet = db.relationship('Pet', back_populates='adoptions')
    # validate
    
class Action(db.Model, SerializerMixin):
    __tablename__ = 'actions'
    id = db.Column(db.Integer, primary_key=True)
    # local columns
    name = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String)
    # foreign keys
    adoption_id = db.Column(db.Integer, db.ForeignKey('adoptions.id'))
    # serialize
    serialize_rules = ('-adoption', )
    # represent
    def __repr__(self):
        return f"<>"
    # relate
    adoption = db.relationship('Adoption', back_populates='actions')
    # validate
    @validates('name')
    def validate_name(self, key, new_name):
        if not 1 <= len(new_name) <= 40:
            raise ValueError('name length domain: [1, 40]')
        return new_name
    @validates('image_url')
    def validate_url(self, key, new_url):
        if not 1 <= len(new_url) <= 4000:
            raise ValueError('url length too long')
        return new_url
    
class Stat(db.Model, SerializerMixin):
    __tablename__ = 'stats'
    id = db.Column(db.Integer, primary_key=True)
    # local columns
    happiness = db.Column(db.Integer, nullable=False, default=100)
    health = db.Column(db.Integer, nullable=False, default=100)
    hunger = db.Column(db.Integer, nullable=False, default=100)
    # foreign keys
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'))
    # serialize
    serialize_rules = ('-pet', )
    # represent
    def __repr__(self):
        return f"<stat: (happiness){self.happiness} (health){self.hunger} (hunger){self.hunger}>"
    # relate
    pet = db.relationship('Pet', back_populates='stat')
    # validate: domain: [0, 100]
    @validates('happiness', 'health', 'hunger')
    def validate_stat(self, key, new_val):
        if not 0 <= int(new_val) <= 100:
            raise ValueError('PetStat domain: [0, 100]')
        return new_val
    
class Strain(db.Model, SerializerMixin):
    __tablename__ = 'strains'
    id = db.Column(db.Integer, primary_key=True)
    # local columns
    name = db.Column(db.String, nullable=False, unique=True)
    emoji = db.Column(db.String, nullable=False)
    # foreign keys
    # serialize
    serialize_rules = ('-pets', )
    # represent
    def __repr__(self):
        return f"<Strain(name:{self.name}, emoji:{self.emoji})>"
    # relate
    pets = db.relationship('Pet', back_populates='strain')
    # validate
    @validates('name', 'emoji')
    def validate_info(self, key, new_info):
        if not 1 <= len(new_info) <= 80:
            raise ValueError('info length domain: [1:80]')
        return new_info