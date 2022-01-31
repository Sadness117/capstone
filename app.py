import os
import requests
from flask import Flask, render_template, request, flash, redirect, session, g, abort
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, FavoritePokemon
from forms import SearchPokemon, AddUser

# referenced warbler project some in this project from springboard


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///capstone-app'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)



@app.route('/')
def home():
    """this goes to the login page"""
    form = AddUser()
    return render_template('login_page.html', form = form)

@app.route('/logout')
def logout():
    """logs user out"""
    session.pop('USER_KEY')
    return redirect('/')

@app.route('/favorite/<int:id>', methods = ['POST'])
def favorite(id):
    """add a pokemon to favorites database"""
    pokemon = requests.get(f"https://pokeapi.co/api/v2/pokemon/{session['CURR_POKEMON']}").json()
    pokemon_id = id
    pokemon_name = pokemon['name']
    current_user = User.query.get(session['USER_KEY'])
    new_favorite = FavoritePokemon(pokemon_name = session['CURR_POKEMON'], poke_id = pokemon_id, pokemon_link = f"https://pokeapi.co/api/v2/pokemon/{session['CURR_POKEMON']}", poke_user = session['USER_KEY'], pokemon_img = pokemon['sprites']['front_default'])
    try:
        db.session.add(new_favorite)
        db.session.commit()
        return 'favorited'
    except:
        db.session.rollback()
        return 'already favorited'

@app.route('/favorites')
def favorite_list():
    """brings up a list of the current users favorite pokemon
    and renders the favorites page"""
    favorites = FavoritePokemon.query.filter_by(poke_user = session['USER_KEY'])
    return render_template('favorites.html', favorites = favorites)

@app.route('/login', methods = ['POST'])
def login():
    """checks for account and will log user in or else it will
    redirect back to login page"""
    form = AddUser()
    if form.validate_on_submit():
        check_user = User.authenticate(username=form.username.data, password=form.password.data)
        if check_user:
            current_user = User.query.filter_by(username = form.username.data).first()
            session['USER_KEY'] = current_user.id
            return redirect('/pokedex_page')
        else:
            return redirect('/')

@app.route('/signup', methods = ['POST'])
def signup():
    """this will create a user for the database and 
    then the user will now have access to the pokedex"""
    form = AddUser()
    if form.validate_on_submit():
        new_user = User.signup(username = form.username.data, password = form.password.data)
        print(new_user)
        db.session.add(new_user)
        db.session.commit()
        current_user = User.query.filter_by(username = form.username.data).first()
        session['USER_KEY'] = current_user.id
        return redirect('/pokedex_page')
    else: 
        return redirect('/signup')
@app.route('/fix')
def fix():
    session['CURR_POKEMON'] = 'golurk'
    return redirect('pokedex_page')
@app.route('/signup')
def signup_page():
    """this brings the user to the sign up page to create an account"""
    form = AddUser()
    return render_template('signup.html', form = form)

@app.route('/pokedex_page')
def pokedex():
    """this displays the pokedex page
    defaults to nothing and user has to seach for pokemon"""
    if session.get('USER_KEY'):
        current_user = User.query.get(session['USER_KEY'])
    else:
        return redirect('/')
    if current_user:
        form = SearchPokemon()
        if session.get('CURR_POKEMON') != None:
            pokemon = requests.get(f"https://pokeapi.co/api/v2/pokemon/{session['CURR_POKEMON']}").json()
            evolution_get = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{pokemon['id']}/").json()
            encounters = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{session['CURR_POKEMON']}").json()
            return render_template('home.html', response = pokemon, form = form, encounters = encounters, current_user = current_user)
        else:
            return render_template('home.html', form = form, current_user = current_user)
    else:
        return redirect('/')

@app.route('/pokemon/id', methods = ['POST'])
def search_by_id():
    """this will be the function to search for a pokemon by id"""
    id = request.form['id']
    next_pokemon = requests.get(f"https://pokeapi.co/api/v2/pokemon/{id}").json()
    session['CURR_POKEMON'] = next_pokemon['name']
    return redirect('/pokedex_page')

@app.route('/pokemon/<int:id>')
def change_pokemon(id):
    """this will change to the next pokemon in the api by 1
    and not specific, it will go to the next pokeomon in 
    the api list"""
    next_pokemon = requests.get(f"https://pokeapi.co/api/v2/pokemon/{id}").json()
    session['CURR_POKEMON'] = next_pokemon['name']
    return redirect('/pokedex_page')

@app.route('/pokedex_page', methods = ['POST'])
def search_pokemon():
    """this searches a pokemon and will display 
    the pokemons info if its a valid pokemon"""
    form = SearchPokemon()

    if form.validate_on_submit():
        try:
            pokemon = requests.get(f"https://pokeapi.co/api/v2/pokemon/{form.pokemon.data}").json()
        except:
            return redirect('/pokedex_page')
        session['CURR_POKEMON'] = form.pokemon.data
        return redirect('/pokedex_page')





@app.route('/info/<id>', methods = ['POST'])
def change_info(id):
    '''this handles the call for the screen updates'''
    pokemon = requests.get(f"https://pokeapi.co/api/v2/pokemon/{session['CURR_POKEMON']}").json()
    change = pokemon
    if id == 'Weight:':
        change = pokemon['weight']/10
        return f'{change}kg'

    elif id == 'Type:':
        change = pokemon['types']
        many_types = ''
        for element in change:
            many_types = many_types + ' ' + element['type']['name']
        return many_types

    elif id == 'Habitat:':
        # not all pokemon have a habitat, so it has some error handling
        try:
            encounters = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{session['CURR_POKEMON']}").json()
            change = encounters['habitat']['name']
            return change
        except:
            return 'None'

    elif id == 'Name:':
        change = pokemon['name']
        return change

    elif id == 'Height:':
        change = pokemon['height']/10
        return f'{change}m'

    elif id == 'Moves:':
        change = pokemon['moves'][0]['move']['name']
        return change

    elif id == 'Items:':
        # not all pokemon have items so it has some error handling
        try:
            change = pokemon['held_items'][0]['item']['name']
            return change
        except:
            return 'None'
            
    elif id == 'Games:':
        change = pokemon['game_indices'][0]['version']['name']
        return change


@app.route('/diff_item/<int:num>')
def diff_item(num):
    curr_pokemon = requests.get(f"https://pokeapi.co/api/v2/pokemon/{session['CURR_POKEMON']}").json()
    try:
        diff_item = curr_pokemon['held_items'][num]['item']['name']
        return diff_item
    except:
        return 'none'
@app.route('/diff_move/<int:num>')
def diff_move(num):
    """cycles through the list of moves for the user"""
    curr_pokemon = requests.get(f"https://pokeapi.co/api/v2/pokemon/{session['CURR_POKEMON']}").json()
    try:    
        diff_move = curr_pokemon['moves'][num]['move']['name']
        return diff_move
    except:
        return 'none'

@app.route('/diff_game/<int:num>')
def diff_game(num):
    """cycles through the list of games for the user"""
    curr_pokemon = requests.get(f"https://pokeapi.co/api/v2/pokemon/{session['CURR_POKEMON']}").json()
    try:    
        diff_game = curr_pokemon['game_indices'][num]['version']['name']
        return diff_game
    except:
        return 'none'

@app.route('/remove_fav/<pokemon>', methods = ['POST'])
def remove_fav(pokemon):
    """removes the users favorite pokemon from the database"""
    curr_user = session['USER_KEY']
    fav_pokemon = FavoritePokemon.query.filter_by(pokemon_name = pokemon, poke_user = curr_user).first()
    db.session.delete(fav_pokemon)
    db.session.commit()
    return 'ok'
