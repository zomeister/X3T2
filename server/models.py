from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.associationproxy import association_proxy
from config import db, bcrypt

class Message(db.Model, SerializerMixin):
    __tablename__ ='messages'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String)
    message = db.Column(db.String)
    thread_id = db.Column(db.Integer, db.ForeignKey('threads.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    @validates('status')
    def validate_status(self, key, new_status):
        if not 1 <= len(new_status) <= 100:
            raise ValueError('len(status):[1,100]')
        return new_status
    @validates('message')
    def validate_message(self, key, new_message):
        if not 1 <= len(new_message) <= 4000:
            raise ValueError('len(message):[1,4000]')
        return new_message
    serialize_rules = ( )
    def __repr__(self):
        return f"<Message(status: {self.status}, message: {self.message})>"

class Thread(db.Model, SerializerMixin):
    __tablename__ = 'threads'
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String, default='default subject')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    friendship_id = db.Column(db.Integer, db.ForeignKey('friendships.id'))
    @validates('subject')
    def validate_subject(self, key, new_subject):
        if not 1 <= len(new_subject) <= 80:
            return ValueError('len(subject):[1,80]')
    friendship = db.relationship('Friendship', backref='thread', uselist=False)
    messages = db.relationship('Message', backref='thread', lazy='dynamic')
    serialize_rules = ( )
    def __repr__(self):
        return f"<Thread(subject: {self.subject})>"

class Post(db.Model, SerializerMixin):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    status = db.Column(db.String)
    content = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    @validates('title')
    def validate_title(self, key, new_title):
        if not 1 <= len(new_title) <= 80:
            raise ValueError('len(title):[1,80]')
        return new_title
    @validates('status')
    def validate_status(self, key, new_status):
        if not 1 <= len(new_status) <= 100:
            raise ValueError('len(status):[1,100]')
        return new_status
    @validates('content')
    def validate_content(self, key, new_content):
        if not 1 <= len(new_content) <= 24000:
            raise ValueError('len(content):[1,24000]')
        return new_content
    serialize_rules = ( )
    def __repr__(self):
        return f"<Post(title: {self.title}, content: {self.content})>"

class Friendship(db.Model, SerializerMixin):
    __tablename__ = 'friendships'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    status = db.Column(db.String)
    req_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    rec_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    @validates('status')
    def validate_status(self, key, new_status):
        if not 1 <= len(new_status) <= 100:
            raise ValueError('len(status):[1,100]')
        return new_status
    serialize_rules = ( '-req_user', '-rec_user', )
    def __repr__(self):
        return f"<Friendship()>"
    
class User(db.Model, UserMixin, SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    _password_hash = db.Column(db.String)
    @hybrid_property
    def password_hash(self):
        return self._password_hash
    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')
    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))
    @validates('username')
    def validate_username(self, key, new_username):
        if not 3 <= len(new_username) <= 40:
            raise ValueError('len(username):[3,40]')
        return new_username
    @validates('email')
    def validate_name(self, key, new_email):
        if not 200 >= len(new_email) >= 4 and '@' in new_email and '.' in new_email:
            raise ValueError('len(email):[4,200], email must include @ and . characters')
        return new_email
    owner = db.relationship('Owner', backref='user', uselist=False)
    friend_reqs = db.relationship('Friendship', foreign_keys=[Friendship.req_user_id], backref='req_user', cascade='all, delete-orphan')
    friend_recs = db.relationship('Friendship', foreign_keys=[Friendship.rec_user_id], backref='rec_user', cascade='all, delete-orphan')
    threads = db.relationship('Thread', backref='user', lazy='dynamic')
    messages = db.relationship('Message', backref='author', lazy='dynamic')
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    reqs = association_proxy('friend_reqs', 'rec_user')
    recs = association_proxy('friend_recs', 'req_user')
    serialize_rules = ('-friend_reqs', '-friend_recs', '-posts.author', '-owner.user', )
    def __repr__(self):
        return f"<User(name:{self.username}, email:{self.email})>"

class Owner(db.Model, SerializerMixin):
    __tablename__ = 'owners'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    city = db.Column(db.String)
    bio = db.Column(db.String)
    profile_url = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    @validates('first_name', 'last_name')
    def validate_name(self, key, new_name):
        if not 1 <= len(new_name) <= 16:
            raise ValueError('len(name):[1,16]')
        return new_name
    @validates('city')
    def validate_city(self, key, new_city):
        if not 1 <= len(new_city) <= 120:
            raise ValueError('len(city):[1,120]')
        return new_city
    @validates('bio')
    def validate_bio(self, key, new_bio):
        if not 1 <= len(new_bio) <= 4000:
            raise ValueError('len(bio):[1,4000]')
        return new_bio
    @validates('profile_url')
    def validate_profile_url(self, key, new_profile_url):
        if not 1 <= len(new_profile_url) <= 2800:
            raise ValueError('len(profile_url):[1,2800]')
        return new_profile_url
    adoptions = db.relationship('Adoption', backref='owner', cascade='all, delete-orphan')
    pets = association_proxy('adoptions', 'pet')
    serialize_rules = ('-user.owner', '-adoptions.owner', )
    def __repr__(self):
        return f"<Owner(username:{self.username}, name: {self.first_name} {self.last_name}, loc:{self.city}, bio{self.bio})>"

class Stat(db.Model, SerializerMixin):
    __tablename__ = 'stats'
    id = db.Column(db.Integer, primary_key=True)
    happiness = db.Column(db.Integer, nullable=False, default=100)
    health = db.Column(db.Integer, nullable=False, default=100)
    hunger = db.Column(db.Integer, nullable=False, default=100)
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'))
    @validates('happiness', 'health', 'hunger')
    def validate_val(self, key, new_val):
        if not 0 <= int(new_val) <= 100:
            raise ValueError('petstats:[0,100]')
        return new_val
    serialize_rules = ( )
    def __repr__(self):
        return f"<stat: (happiness){self.happiness} (health){self.hunger} (hunger){self.hunger}>"

class Pet(db.Model, SerializerMixin):
    __tablename__ = 'pets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    factor = db.Column(db.Integer, nullable=False, default=100)
    strain_id = db.Column(db.Integer, db.ForeignKey('strains.id'))
    @validates('name')
    def validate_name(self, key, new_name):
        if not 1 <= len(new_name) <= 16:
            raise ValueError('len(name):[1,16]')
        return new_name
    @validates('factor')
    def validate_factor(self, key, new_factor):
        if not 1 <= int(new_factor) <= 100:
            raise ValueError('factor:[1,100]')
        return new_factor
    strain = db.relationship('Strain', backref='pets', uselist=False)
    stat = db.relationship('Stat', backref='pet', uselist=False)
    adoptions = db.relationship('Adoption', backref='pet', cascade='all, delete-orphan')
    owners = association_proxy('adoptions', 'owner')
    serialize_rules = ('-stat', '-strain.pets', '-adoptions.pet', )
    def __repr__(self):
        return f"<Pet(name:{self.name}, factor:{self.factor})>"

class Adoption(db.Model, SerializerMixin):
    __tablename__ = 'adoptions'
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('owners.id'))
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'))
    actions = db.relationship('Action', backref='adoption', cascade='all, delete-orphan')
    serialize_rules = ('-actions.adoption', '-owner.adoptions', '-pet.adoptions', )
    def __repr__(self):
        return f"<>"
    
class Action(db.Model, SerializerMixin):
    __tablename__ = 'actions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String)
    adoption_id = db.Column(db.Integer, db.ForeignKey('adoptions.id'))
    menu_id = db.Column(db.Integer, db.ForeignKey('menus.id'))
    @validates('name')
    def validate_name(self, key, new_name):
        if not 1 <= len(new_name) <= 40:
            raise ValueError('len(name):[1,40]')
        return new_name
    @validates('image_url')
    def validate_image_url(self, key, new_image_url):
        if not 1 <= len(new_image_url) <= 2800:
            raise ValueError('len(image_url):[1,2800]')
        return new_image_url
    serialize_rules = ('-adoption', '-menu.actions', )
    def __repr__(self):
        return f"<Action(name: {self.name})>"

class Menu(db.Model, SerializerMixin):
    __tablename__ = 'menus'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    emoji = db.Column(db.String, nullable=False, unique=True)
    @validates('name', 'emoji')
    def validate_info(self, key, new_info):
        if not 1 <= len(new_info) <= 80:
            raise ValueError('len(info):[1,80]')
        return new_info
    actions = db.relationship('Action', backref='menu', cascade='all, delete-orphan')
    serialize_rules = ('-actions.menu', '-actions.adoption', )
    def __repr__(self):
        return f"<Menu(name:{self.name}, emoji:{self.emoji})>"
    
class Strain(db.Model, SerializerMixin):
    __tablename__ = 'strains'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    emoji = db.Column(db.String, nullable=False)
    @validates('name', 'emoji')
    def validate_info(self, key, new_info):
        if not 1 <= len(new_info) <= 80:
            raise ValueError('len(info):[1,80]')
        return new_info
    serialize_rules = ( )
    def __repr__(self):
        return f"<Strain(name:{self.name}, emoji:{self.emoji})>"
    