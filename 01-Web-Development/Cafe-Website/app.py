from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# The SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    seats = db.Column(db.String(50), nullable=False)
    coffee_price = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Cafe {self.name}>'

# Create the tables
with app.app_context():
    db.create_all()

# Display all cafes
@app.route('/')
def index():
    cafes = Cafe.query.all()
    return render_template('index.html', cafes=cafes)

# Add a new cafe
@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    if request.method == 'POST':
        new_cafe = Cafe(
            name=request.form['name'],
            map_url=request.form['map_url'],
            img_url=request.form['img_url'],
            location=request.form['location'],
            has_sockets=request.form.get('has_sockets') == 'on',
            has_wifi=request.form.get('has_wifi') == 'on',
            can_take_calls=request.form.get('can_take_calls') == 'on',
            seats=request.form['seats'],
            coffee_price=request.form['coffee_price']
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_cafe.html')

# Delete a cafe
@app.route('/delete/<int:id>')
def delete_cafe(id):
    cafe = Cafe.query.get_or_404(id)
    db.session.delete(cafe)
    db.session.commit()
    return redirect(url_for('index'))

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
