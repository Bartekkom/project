from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import date, time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tickets.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model bazy danych
class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    match_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    available_tickets = db.Column(db.Integer, nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    date = db.Column(db.Date, nullable=False)  # Nowa kolumna na datę
    time = db.Column(db.Time, nullable=False)  # Nowa kolumna na godzinę
    
    def __repr__(self):
        return f"<Ticket {self.match_name}, Available: {self.available_tickets}>"

@app.route('/')
def home():
    # Pobierz wszystkie bilety z bazy danych
    tickets = Ticket.query.all()
    return render_template('index.html', tickets=tickets)  # Przekaż dane do szablonu

@app.route('/match/<slug>')
def match_details(slug):
    ticket = Ticket.query.filter_by(slug=slug).first_or_404()

    # Calculate sector prices
    price_a = round(ticket.price * 1.25, 2)  # 125% za sektor A
    price_b = ticket.price                   # Bazowa cena za sektor B
    price_c = ticket.price                   # Bazowa cena za sektor C
    price_d = round(ticket.price * 1.25, 2)  # 125% za sektor D

    return render_template(
        'match_details.html',
        ticket=ticket,
        price_a=price_a,
        price_b=price_b,
        price_c=price_c,
        price_d=price_d
    )

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Tworzy tabele w bazie danych, jeśli jeszcze nie istnieją
    app.run(debug=True)