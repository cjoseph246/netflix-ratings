#!/bin/env python2.7

from __future__ import print_function
from flask import Flask, request, session, redirect, \
    render_template, flash
from flask_script import Manager, Server
from flask_sqlalchemy import SQLAlchemy
import datetime
import new_on_netflix as non
import rotten_tomatoes as rt


app = Flask(__name__)
app.config.update(dict(
    DEBUG='TRUE',
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='admin',
    SQLALCHEMY_DATABASE_URI='sqlite:///show.db'
))


db = SQLAlchemy(app)
manager = Manager(app)
db.echo = True


class Show(db.Model):
    __tablename__ = 'shows'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20))
    show = db.Column(db.String(40))
    critic_consensus = db.Column(db.Text)
    reviews_counted = db.Column(db.String(10))
    user_ratings = db.Column(db.String(10))
    tomatometer = db.Column(db.String(10))
    audience_rating = db.Column(db.String(10))
    rotten = db.Column(db.String(10))
    fresh = db.Column(db.String(10))
    average_rating = db.Column(db.String(10))

    def __init__(self, date=None, show=None, critic_consensus=None, reviews_counted=None,
                 user_ratings=None, tomatometer=None, audience_rating=None, rotten=None,
                 fresh=None, average_rating=None):
        self.date = date
        self.show = show
        self.critic_consensus = critic_consensus
        self.reviews_counted = reviews_counted
        self.user_ratings = user_ratings
        self.tomatometer = tomatometer
        self.audience_rating = audience_rating
        self.rotten = rotten
        self.fresh = fresh
        self.average_rating = average_rating


def show_attributes():
    # results = non.scrape()
    # non.write_cleaned(results)
    with open('new_on_netflix.txt') as f:
        for line in f:
            s = rt.Show()
            date, show = line.split(':', 1)
            month, day = date.split()
            date = datetime.date(2016, month=3, day=int(day)).strftime("%B %d")
            s.add_date(date)
            s.add_show(rt.scrape_ratings(show))
            populate_db(s.get_dict())


def populate_db(show_attrs):
    show = Show(**show_attrs)
    db.session.add(show)
    db.session.commit()


@app.route('/', methods=['GET'])
def show_entries():
    # show_attributes() #only needed every 2 weeks
    shows = Show.query.order_by('date').all()
    return render_template('ratings.html', shows=shows)


@app.route('/about', methods=['GET'])
def show_about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run()
    # db.create_all()
    # db.session.commit()
    # db.drop_all  # will destroy all data in db
    # db.session.delete(admin) # will delete admin, but only upon commit

