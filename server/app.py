
from flask import Flask, jsonify
from flask_migrate import Migrate

from models import db, Event, Session, Speaker, Bio


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///eventwise.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)


# GET all events
@app.route("/events", methods=["GET"])
def get_events():
    events = Event.query.all()

    return jsonify([
        {
            "id": event.id,
            "name": event.name,
            "location": event.location
        }
        for event in events
    ]), 200


# GET all sessions for an event
@app.route("/events/<int:id>/sessions", methods=["GET"])
def get_event_sessions(id):
    event = Event.query.get(id)

    if event is None:
        return jsonify({"error": "Event not found"}), 404

    return jsonify([
        {
            "id": session.id,
            "title": session.title,
            "start_time": session.start_time.isoformat()
        }
        for session in event.sessions
    ]), 200


# GET all speakers
@app.route("/speakers", methods=["GET"])
def get_speakers():
    speakers = Speaker.query.all()

    return jsonify([
        {
            "id": speaker.id,
            "name": speaker.name
        }
        for speaker in speakers
    ]), 200


# GET one speaker with their bio
@app.route("/speakers/<int:id>", methods=["GET"])
def get_speaker(id):
    speaker = Speaker.query.get(id)

    if speaker is None:
        return jsonify({"error": "Speaker not found"}), 404

    bio_text = (
        speaker.bio.bio_text
        if speaker.bio
        else "No bio available"
    )

    return jsonify({
        "id": speaker.id,
        "name": speaker.name,
        "bio_text": bio_text
    }), 200


# GET all speakers for a session
@app.route("/sessions/<int:id>/speakers", methods=["GET"])
def get_session_speakers(id):
    session = Session.query.get(id)

    if session is None:
        return jsonify({"error": "Session not found"}), 404

    return jsonify([
        {
            "id": speaker.id,
            "name": speaker.name,
            "bio_text": (
                speaker.bio.bio_text
                if speaker.bio
                else "No bio available"
            )
        }
        for speaker in session.speakers
    ]), 200


if __name__ == "__main__":
    app.run(port=5555, debug=True)
