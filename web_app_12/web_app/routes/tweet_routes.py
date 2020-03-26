from flask import Blueprint, jsonify, request, render_template, flash, redirect
import random
from web_app.services.twitter_service import twitter_api_client
from web_app.services.basilica_service import basilica_api_client

from web_app.models import db, Tweet, User, parse_records

tweet_routes = Blueprint("tweet_routes", __name__)

@tweet_routes.route("/tweets")
def list_tweets():
    tweet_records = Tweet.query.all()
    return render_template("tweets.html", message="Here's some tweets", tweets=tweet_records)

@tweet_routes.route("/tweets/users")
def list_users():
    #if request.path.endswith(".json"):
    #    return some json
    #else:
    #    render a template
    db_users = User.query.all()
    users = parse_records(db_users)
    return jsonify(users)

@tweet_routes.route("/tweets/new")
def new_tweet():
    return render_template("new_tweet.html")

@tweet_routes.route("/tweets/create", methods=["POST"])
def create_tweet():
    print("FORM DATA:", dict(request.form))

    if db.session.query(User).filter_by(id = request.form["poster_id"]).count() < 1: #Testing if our User already exists
        new_user = User(id = request.form["poster_id"],name=request.form['name'])
        print("New User Added", new_user)
        db.session.add(new_user)
    new_tweet = Tweet(id = random.randint(1,100000), text=request.form["text"], poster_id=request.form["poster_id"])


    print(new_tweet)
    db.session.add(new_tweet)
    db.session.commit()

    # return jsonify({
    #    "message": "BOOK CREATED OK",
    #    "book": dict(request.form)
    # })
    # flash(f"Book '{new_book.title}' created successfully!", "success")
    return redirect("/tweets")


def store_twitter_user_data(screen_name):
    print(screen_name)

    api = twitter_api_client()
    twitter_user = api.get_user(screen_name)
    statuses = api.user_timeline(screen_name, tweet_mode="extended", count=150)

    db_user = User.query.get(twitter_user.id) or User(id=twitter_user.id)
    db_user.screen_name = twitter_user.screen_name
    db_user.name = twitter_user.name
    db_user.location = twitter_user.location
    db_user.followers_count = twitter_user.followers_count
    db.session.add(db_user)
    db.session.commit()

    print("STATUS COUNT:", len(statuses))
    basilica_api = basilica_api_client()
    all_tweet_texts = [status.full_text for status in statuses]
    embeddings = list(basilica_api.embed_sentences(all_tweet_texts, model="twitter"))
    print("NUMBER OF EMBEDDINGS", len(embeddings))
    counter = 0
    for status in statuses:
        print(status.full_text)
        print("----")
        # print(dir(status))

        # Find or create database tweet:
        db_tweet = Tweet.query.get(status.id) or Tweet(id=status.id)
        db_tweet.user_id = status.author.id  # or db_user.id
        db_tweet.full_text = status.full_text
        # embedding = basilica_client.embed_sentence(status.full_text, model="twitter") # todo: prefer to make a single request to basilica with all the tweet texts, instead of a request per tweet
        embedding = embeddings[counter]
        print(len(embedding))
        db_tweet.embedding = embedding
        db.session.add(db_tweet)
        counter += 1
    db.session.commit()

    return db_user, statuses




@tweet_routes.route("/users/<screen_name>")
def get_user(screen_name=None):

    db_user, statuses = store_twitter_user_data(screen_name)
    #breakpoint()
    #return f"OK - Got user {screen_name}"
    return render_template("user.html", user=db_user, tweets=statuses) # tweets=db_tweets
