from random import randint, choice as rc
from faker import Faker
from app import db, app
from models import User, Owner, Pet, Adoption, Action, Stat, Strain

faker = Faker()

def delete_records():
    with app.app_context():
        Owner.query.delete()
        Pet.query.delete()
        Adoption.query.delete()
        Action.query.delete()
        db.session.commit()
        print("Records deleted")

def seed_users():
    with app.app_context():
        User.query.delete()
        users = [ User(username=faker.user_name(), email=faker.email(), password_hash='123456789a') for _ in range(4) ]
        db.session.add_all(users)
        db.session.commit()
        return users

def seed_strains():
    strains_dict = [
        {'name': 'rat', 'emoji': '🐀'},
        {'name': 'mouse', 'emoji': '🐁'},
        {'name': 'cow', 'emoji': '🐄'},
        {'name': 'rabbit', 'emoji': '🐇'},
        {'name': 'cat', 'emoji': '🐈'},
        {'name': 'snake', 'emoji': '🐍'},
        {'name': 'horse', 'emoji': '🐎'},
        {'name': 'chicken', 'emoji': '🐓'},
        {'name': 'dog', 'emoji': '🐕'},
        {'name': 'pig', 'emoji': '🐖'},
        {'name': 'ant', 'emoji': '🐜'},
        {'name': 'fish', 'emoji': '🐟'},
        {'name': 'bird', 'emoji': '🐦'},
        {'name': 'duck', 'emoji': '🦆'}
    ]
    strains = [Strain(name=s['name'], emoji=s['emoji']) for s in strains_dict]
    with app.app_context():
        Strain.query.delete()
        db.session.add_all(strains)
        db.session.commit()
        return strains

def create_owners(users):
    first_names = [faker.first_name() for _ in range(18)] + [
        'John', 'Jane', 'Jill', 'Joe', 'Jim', 'Jenny',
    ]
    last_names = [faker.last_name() for _ in range(18)] + [
        'Smith', 'Johnson', 'Williams', 'Brown', 'Jones',
    ]
    cities = [ faker.city() for _ in range(40)] + [
        'Houston',          'Dallas',           'Austin',           'San Antonio',      'Fort Worth',       'El Paso',
        'San Francisco',    'Los Angeles',      'San Diego',        'San Jose',         'Santa Barbara',    'Sacramento',
        'Denver',           'Boston',           'Chicago',          'New York City',    'Seattle',          'Portland',
        'New Orleans',      'Vancouver'
    ]
    profile_urls = [
        'https://i.pinimg.com/736x/92/88/d7/9288d7c4877729e84d4b0480440cb975.jpg',
        'https://wallpapercave.com/wp/wp10217326.jpg',
        'https://wallpapers.com/images/hd/aesthetic-profile-picture-death-star-1oymox9geh6mn2fv.jpg',
        'https://wallpaperaccess.com/full/4378170.jpg',
        'https://art.ngfiles.com/images/2961000/2961005_bezzathor_an-overly-simple-profile-picture-i-know-it-s-oversized.png?f1672592034',
        'https://i.pinimg.com/originals/1e/06/68/1e0668deaf1e84b8102795de9149a547.jpg',
        'https://e1.pxfuel.com/desktop-wallpaper/617/339/desktop-wallpaper-simple-aesthetic-tumblr-aesthetic-profile.jpg'
    ]
    with app.app_context():
        owners = [ Owner(bio=faker.sentence(), first_name=rc(first_names), last_name=rc(last_names), city=rc(cities), profile_url=rc(profile_urls), user_id=i+1) for i in range(6) ]
        db.session.add_all(owners)
        db.session.commit()
        return owners

def create_pets(strains):
    pet_names = [faker.first_name() for _ in range(18)] + [
        'Sidon',    'Teba',     'Riju',     'Yunobo',
        'Mipha',    'Revali',   'Urbosa',   'Daruk',
        'Impa',     'Paya',     'Purah',    'Robbie',
        'Arthur',   'Fronk',    'Giselle',  'Mei',
        'Bolson',   'Cado',     'Fyson',    'Cottla',
        'Jerrin',   'Dorian',   'Koko',     'Mia',   
    ]
    with app.app_context():
        pets = [Pet(name=rc(pet_names), strain_id=rc(range(len(strains)))+1, stat=Stat()) for _ in range(40)]
        db.session.add_all(pets)
        db.session.commit()
        return pets

def create_adoptions(owners, pets, quantity=12):
    with app.app_context():
        adoptions = [Adoption(owner_id=rc(range(len(owners))), pet_id=rc(range(len(pets)))) for _ in range(quantity) ]
        db.session.add_all(adoptions)
        db.session.commit()
        return adoptions

def create_actions(adoptions):
    names = ['wash', 'feed','sleep', 'play', 'groom', 'train', 'walk']
    with app.app_context():
        actions = [Action(name=rc(names), adoption_id=rc(range(len(adoptions)))+1) for _ in range(20)]
        db.session.add_all(actions)
        db.session.commit()
        return actions


def relate_users_and_owners(users, owners):
    with app.app_context():
        for user in users:
            user.owner = Owner.query.filter_by(user_id=user.owner.id).first()
        return users, owners
 
if __name__ == '__main__':
    with app.app_context():
        delete_records()
        print("seeding...")
        users = seed_users()
        owners = create_owners(users)
        # users, owners = relate_users_and_owners(users, owners)
        strains = seed_strains()
        pets = create_pets(strains)
        adoptions = create_adoptions(owners, pets)
        actions = create_actions(adoptions)