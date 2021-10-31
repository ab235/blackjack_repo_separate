from flask import Flask, render_template, request, redirect, url_for, session
from blackjack import Card, Deck, Player, Game
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.secret_key = 'dfghjiouhgdashswevnohshshshidnasiodn'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)
player = Player('none')
game = Game(player)

class User(db.Model):
    uname = db.Column(db.String(80), unique=True, nullable=False, primary_key = True)
    pswrd = db.Column(db.String(80), nullable=False)
    money = db.Column(db.Integer)

    def __repr__(self): #print user
        return '{}: ${}'.format(self.uname, self.money)

    @staticmethod
    def save_db(user, db): #adding new users to database
        db.session.add(user)
        db.session.commit()
    @staticmethod
    def update(user, db): #updating information of users
        puser = User.query.filter_by(uname=user.uname).first()
        puser.uname = user.uname
        puser.pswrd = user.pswrd
        puser.money = user.money
        db.session.commit()

    @staticmethod
    def get_user(username, db): #return user from database
        return User.query.filter_by(uname=username).first()
                

@app.route('/', methods = ['GET', 'POST'])
def index():
    session['user'] = False #forces a log-in to access dashboard
    return render_template('index.jinja')
@app.route('/register', methods = ['GET', 'POST'])
def register():
    message = "Register"
    if (request.method == 'POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        cpassword = request.form.get('confirm password')
        if (User.get_user(username, db)):
            message = "This username is already taken. Please try again."
        else:
            if (password == cpassword):
                user = User()
                user.uname = username
                user.pswrd = password
                user.money = 0
                session['user'] = user.uname
                User.save_db(user, db)
                message = "User registered successfully."
                return redirect(url_for('dashboard', username = username))
            else:
                message = "Password and Confirm Password do not match. User not registered."


    return render_template('register.jinja', message = message)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    message = "Login"
    if (request.method == 'POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.get_user(username, db)
        if (user):
            if (password == user.pswrd):
                session['user'] = user.uname
                return redirect(url_for('dashboard', username = username))
            else:
                message = 'Password does not match.'
        else:
            message = "User does not exist."

        

    return render_template('login.jinja', message = message)
@app.route('/dashboard/<username>', methods = ['GET', 'POST'])
def dashboard(username):
    session['runs'] = 1
    user = User.get_user(username, db)
    message = ''
    user.money = float(user.money)
    if (session['user']):
        if (request.method == 'POST'):
            if (request.form.get("deposit")):
                try:
                    nmoney = float(request.form.get("amount"))
                    if (nmoney > 0):
                        user.money += nmoney
                        User.update(user, db)
                    else:
                        message = "Please deposit a positive amount."
                except ValueError:
                    message = "This is not a depositable number."
            if (request.form.get("withdraw")):
                try:
                    nmoney = float(request.form.get("amount"))
                    if (nmoney > 0 and (user.money - nmoney) >= 0):
                        user.money -= nmoney
                        User.update(user, db)
                    elif (nmoney < 0):
                        message = "Please withdraw a positive amount of money."
                    else:
                        message = "You can't afford this withdrawal."
                except ValueError:
                    message = "This is not a withdrawable number."
            if (request.form.get("change_password")):
                npass = request.form.get("new_password")
                cpass = request.form.get("confirm_password")
                if (npass == cpass):
                    user.pswrd = npass
                    User.update(user, db)
                else:
                    message = "Passwords do not match."
            if (request.form.get("play")):
                return redirect(url_for('blackjack', username = username))
            if (request.form.get("logout")):
                session['user'] = False
                return redirect(url_for('index'))
        return render_template('dashboard.jinja', user = str(user), message = message)
    else:
        return redirect(url_for('index'))

@app.route('/blackjack/<username>', methods = ['GET', 'POST'])
def blackjack(username):
    if (session['user']):
        session['message'] = ""
        user = User.get_user(username, db)
        user.money = float(user.money)
        next_card = True
        player.name = username
        if (user.money >= 300):
            session['message'] += 'Do you want to take a card: <br>'
            if (request.form.get("exit")):
                return redirect(url_for('end_game', username = username))
            if (request.form.get("next")):
                session['message'] += game.turn() + "<br>"
                return redirect(url_for('catch1', username = username))
        else:
            session['message'] = "You don't have enough funds."
            if (request.form.get("exit")):
                return redirect(url_for('dashboard', username = username))
        return render_template('blackjack.jinja', user = str(user), message = session['message'])
    else:
        return redirect(url_for('index'))
@app.route('/catch1/<username>', methods = ['GET', 'POST'])
def catch1(username): #recursive function that keeps running until the game ends
    if (session['user']):
        if (not game.game_over()):
            user = User.get_user(username, db)
            session['message'] += 'Do you want to take a card: <br>'
            if (request.form.get("exit")):
                return redirect(url_for('end_game', username = username))
            elif (request.form.get("next")): 
                session['message'] += game.turn() + "<br>" #game.turn returns the players hand after dealing a card
                return redirect(url_for('catch1', username = username)) #if next is clicked, refresh the page and begin the turn again
        else:
            return redirect(url_for('end_game', username = username))
        return render_template('blackjack.jinja', user = str(user), message = session['message'])
    else:
        return redirect(url_for('index'))
@app.route('/end_game/<username>', methods = ['GET', 'POST'])
def end_game(username):
    if (session['user']):
        payoff = game.stop()
        if (payoff-100 < 0):
            session['message'] += 'You lost: $' + str(100 - payoff) + '<br>'
        else:
            session['message'] += 'You won: $' + str(payoff-100) + '<br>'
        user = User.get_user(username, db)
        user.money = float(user.money)
        user.money += payoff - 50
        User.update(user,db)
        player.cards = []
        game.__init__(player)
        session['message'] += ('do you want to play another game: <br>')
        if (request.form.get("exit")):
            return redirect(url_for('dashboard', username = username))
        elif (request.form.get("next")):
            return redirect(url_for('blackjack', username = username))
        return render_template('blackjack.jinja', user = str(user), message = session['message'])
    else:
        return redirect(url_for('index'))
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    if (request.method == 'POST'):
        return redirect(url_for('index'))
    return render_template('404.jinja'), 404
if __name__ == '__main__':
    app.run(use_reloader=False)
