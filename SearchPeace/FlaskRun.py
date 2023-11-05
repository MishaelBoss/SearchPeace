from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///basa.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class WebSites (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url_site = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    about = db.Column(db.Text, nullable=False)

@app.route('/')
@app.route('/home')
def index():
    q = request.args.get('q')

    if  q:
        webSites = WebSites.query.filter(WebSites.title.contains(q) | WebSites.about.contains(q))
        return render_template('search.html', data=webSites)
    else:
        webSites = WebSites.query.order_by(WebSites.title).all()
    return render_template('index.html', data=webSites)

@app.route('/search')
def search():
    q = request.args.get('q')

    if  q:
        webSites = WebSites.query.filter(WebSites.title.contains(q) | WebSites.about.contains(q))
        return render_template('search.html', data=webSites)
    else:
        webSites = WebSites.query.order_by(WebSites.title).all()

    return render_template('search.html', data=webSites)

@app.route('/add-site/<int:id>/del')
def site_delete(id):
    webSites = WebSites.query.get_or_404(id)

    try:
        db.session.delete(webSites)
        db.session.commit()
        return redirect('/')
    except:
        return "При удаление ароизошла ошибка"

@app.route('/add-site', methods=['POST', 'GET'])
def add_site():
    if request.method == 'POST':
        title = request.form['title']
        about = request.form['about']
        url_site = request.form['url_site']

        webSites = WebSites(title=title, about=about, url_site=url_site)

        try:
            db.session.add(webSites)
            db.session.commit()
            return redirect('/')
        except:
            return "Ошибка"
    return render_template('add-site.html')

if __name__ == '__main__':
    app.run(debug=True)