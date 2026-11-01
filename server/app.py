
from flask import Flask, jsonify, request

app = Flask(__name__)


# Event class
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title
        }


# In-memory events list
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]


# Helper function to find an event
def find_event(event_id):
    for event in events:
        if event.id == event_id:
            return event
    return None


# HOME ROUTE
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Events API"}), 200


# GET ALL EVENTS
@app.route("/events", methods=["GET"])
def get_events():
    return jsonify([event.to_dict() for event in events]), 200


# GET ONE EVENT
@app.route("/events/<int:event_id>", methods=["GET"])
def get_event(event_id):
    event = find_event(event_id)

    if event is None:
        return jsonify({"error": "Event not found"}), 404

    return jsonify(event.to_dict()), 200


# CREATE EVENT
@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()

    if not data or not data.get("title"):
        return jsonify({"error": "Title is required"}), 400

    new_id = max([event.id for event in events], default=0) + 1

    new_event = Event(new_id, data["title"])
    events.append(new_event)

    return jsonify(new_event.to_dict()), 201


# UPDATE EVENT
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    event = find_event(event_id)

    if event is None:
        return jsonify({"error": "Event not found"}), 404

    data = request.get_json()

    if not data or not data.get("title"):
        return jsonify({"error": "Title is required"}), 400

    event.title = data["title"]

    return jsonify(event.to_dict()), 200


# DELETE EVENT
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = find_event(event_id)

    if event is None:
        return jsonify({"error": "Event not found"}), 404

    events.remove(event)

    return "", 204


if __name__ == "__main__":
    app.run(debug=True)
