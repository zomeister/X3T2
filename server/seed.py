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
    
def create_pets(strains):
    pet_names = [faker.first_name() for _ in range(18)] + [
        'Sidon',    'Teba',     'Riju',     'Yunobo',
        'Mipha',    'Revali',   'Urbosa',   'Daruk',
        'Impa',     'Paya',     'Purah',    'Robbie',
        'Arthur',   'Fronk',    'Giselle',  'Mei',
        'Bolson',   'Cado',     'Fyson',    'Cottla',
        'Jerrin',   'Dorian',   'Koko',     'Mia',   
    ]
    pets = [Pet(name=rc(pet_names), strain_id=rc(range(len(strains))), stat=Stat()) for _ in range(40)]
    with app.app_context():
        db.session.add_all(pets)
        db.session.commit()
        return pets
    
if __name__ == '__main__':
    with app.app_context():
        delete_records()
        print("seeding...")
        strains = seed_strains()
        pets = create_pets(strains)