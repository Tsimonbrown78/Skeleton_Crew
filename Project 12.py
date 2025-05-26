from flask import Flask, request, redirect, url_for
import openai

app = Flask(__name__)

#OpenAI key
client = openai.OpenAI(
    api_key='your key here'
)

# Store temporary game state
games = {}


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        adventure_type = request.form['adventure']
        return redirect(url_for('setup', adventure_type=adventure_type))
    
    return '''
        <h1>Choose Your Adventure</h1>
        <form method="POST">
            <button type="submit" name="adventure" value="Fantasy">Fantasy Adventure</button>
            <button type="submit" name="adventure" value="Sci-Fi">Sci-Fi Adventure</button>
        </form>
    '''

@app.route('/setup', methods=['GET', 'POST'])
def setup():
    adventure_type = request.args.get('adventure_type')
    
    if request.method == 'POST':
        hero_name = request.form['hero_name']
        special_skill = request.form['special_skill']
        goal = request.form['goal']
        
        game_id = str(len(games) + 1)
        games[game_id] = {
            'adventure_type': adventure_type,
            'hero_name': hero_name,
            'special_skill': special_skill,
            'goal': goal,
            'history': ""
        }
        return redirect(url_for('play', game_id=game_id))
    
    return f'''
        <h1>Setup Your {adventure_type} Adventure</h1>
        <form method="POST">
            Hero Name: <input type="text" name="hero_name"><br><br>
            Special Skill: <input type="text" name="special_skill"><br><br>
            Goal: <input type="text" name="goal"><br><br>
            <button type="submit">Start Adventure</button>
        </form>
    '''


@app.route('/exit')
def exit_game():
    return '''
        <h1>Thanks for playing!</h1>
        <p>Your adventure has ended.</p>
        <a href="/">Return to Home</a>
    '''


@app.route('/play', methods=['GET', 'POST'])
def play():
    game_id = request.args.get('game_id')
    game = games.get(game_id)
    
    if not game:
        return "<h1>Game not found. Please start a new adventure.</h1>"
    
    if request.method == 'POST':
        player_action = request.form['action']
        game['history'] += f"\nPlayer: {player_action}\n"

    # Build the prompt
    prompt = f"""
You are narrating a {game['adventure_type']} text-based adventure game.

The hero's name is {game['hero_name']}.
Their special skill is {game['special_skill']}.
Their ultimate goal is {game['goal']}.

Story so far:
{game['history']}

Describe what happens next and ask the player what they want to do.
"""

    #Calling GPT to respond to player has chosen
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    story = response.choices[0].message.content
    game['history'] += f"Narrator: {story}\n"
    
    return f'''
    <h1>Adventure: {game['adventure_type']}</h1>
    <h2>{game['hero_name']} - {game['special_skill']}</h2>
    <p><b>Goal:</b> {game['goal']}</p>
    <hr>
    <div style="white-space: pre-wrap;">{story}</div>
    <hr>
    <form method="POST">
        Your Action: <input type="text" name="action">
        <button type="submit">Continue</button>
    </form>
    <br>
    <form action="/exit" method="GET">
        <button type="submit">Quit Adventure</button>
    </form>
'''

if __name__ == '__main__':
    app.run(debug=True)

