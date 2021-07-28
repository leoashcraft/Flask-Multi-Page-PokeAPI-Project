from flask import render_template, request, g
import requests
from app import app
from .forms import SearchForm

@app.route('/', methods=['GET'])
def index():
    form = SearchForm()
    g.form=form
    return render_template('index.html.j2')

@app.route('/pokemon', methods=['GET', 'POST'])
def pokemon():
    form = SearchForm()
    g.form=form
    if request.method == 'POST' and g.form.validate_on_submit():
        pokemon = form.search.data
        url = f'https://pokeapi.co/api/v2/pokemon/{pokemon}'
        response = requests.get(url)
        if response.ok:
            try:
                data = response.json().get("stats")
                spritedata = response.json()["sprites"]['other']['dream_world'].get("front_default")
            except:
                error_string=f'There is no info for {pokemon}'
                return render_template("pokemon.html.j2", form=form, error=error_string)
            all_stats = []
            for stat in data:
                stat_dict={
                    'poke_statbase':stat['base_stat'],
                    'poke_stateffort':stat['effort'],
                    'poke_statname':stat['stat']['name'],
                }
                all_stats.append(stat_dict)
            return render_template("pokemon.html.j2", form=form, stats=all_stats, sprite=spritedata, pokemon=pokemon.title())
        else:
            error_string="Invalid Pokemon name!"
            return render_template("pokemon.html.j2", form=form, error=error_string)
    return render_template("pokemon.html.j2", form=form)