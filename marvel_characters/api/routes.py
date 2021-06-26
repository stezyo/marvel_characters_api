from flask import Blueprint, request, jsonify
from marvel_characters.helpers import token_required
from marvel_characters.models import db, User, Hero, hero_schema, heroes_schema

api = Blueprint('api', __name__, url_prefix = '/api')

@api.route('/getdata')
@token_required
def getdata(current_user_token):
    return { 'some': 'value'}


# CREATE DRONE ENDPOINT
@api.route('/heroes', methods = ['POST'])
@token_required
def create_hero(current_user_token):
    name = request.json['name']
    alias = request.json['alias']
    affiliation = request.json['affiliation']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    hero = Hero(name, alias, affiliation, user_token = user_token )

    db.session.add(hero)
    db.session.commit()

    response = hero_schema.dump(hero)
    return jsonify(response)




# RETRIEVE ALL DRONEs ENDPOINT
@api.route('/heroes', methods = ['GET'])
@token_required
def get_heroes(current_user_token):
    owner = current_user_token.token
    hero = Hero.query.filter_by(user_token = owner).all()
    response = heroes_schema.dump(hero)
    return jsonify(response)


# RETRIEVE ONE Drone ENDPOINT
@api.route('/heroes/<id>', methods = ['GET'])
@token_required
def get_hero(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        hero = Hero.query.get(id)
        response = hero_schema.dump(hero)
        return jsonify(response)
    else:
        return jsonify({"message": "Valid Token Required"}),401



# UPDATE DRONE ENDPOINT
@api.route('/heroes/<id>', methods = ['POST','PUT'])
@token_required
def update_hero(current_user_token,id):
    hero = Hero.query.get(id) # GET DRONE INSTANCE
    hero.name = request.json['name']
    hero.alias = request.json['alias']
    hero.affiliation = request.json['affiliation']
    hero.user_token = current_user_token.token
    db.session.commit()
    response = hero_schema.dump(hero)
    return jsonify(response)


# DELETE DRONE ENDPOINT
@api.route('/heroes/<id>', methods = ['DELETE'])
@token_required
def delete_hero(current_user_token, id):
    hero = Hero.query.get(id)
    db.session.delete(hero)
    db.session.commit()
    response = hero_schema.dump(hero)
    return jsonify(response)