import sys
from flask import Flask, request, json
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
api = Api(app)
Base = declarative_base()

class Item(Base):
    __tablename__ = 'item'
    __table_args__ = {'sqlite_autoincrement': True}

    id = Column(Integer, primary_key=True)
    key = Column(String(250))
    value = Column(String(250))

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def toJSON(self):
        return {"key": self.key, "value": self.value}

Session = sessionmaker()

@app.route("/get")
@app.route("/get/<key>")
def getItem(key=None):
    session = Session()
    if key:
        item = session.query(Item).filter_by(key=key).first()
        return json_response(item.toJSON())
    else:
        items = session.query(Item).all()
        return json_response([item.toJSON() for item in items])

@app.route("/set", methods=["POST"])
def setItem():
    session = Session()
    key = request.form.get("key")
    value = request.form.get("value")

    if key:
        item = session.query(Item).filter_by(key=key).first()

        if item:
            item.value = value
            session.add(item)
            session.commit()
            return json_response({'success': 'item updated successfully'}, 200)
        else:
            item = Item(key=key, value=value)
            session.add(item)
            session.commit()
            return json_response({'success': 'item added successfully'}, 200)
    else:
        return json_response({'error': 'missing parameter: key'}, 404)

@app.route("/delete", methods=["DELETE"])
def deleteItem():
    session = Session()
    key = request.form.get("key")

    if key:
        item = session.query(Item).filter_by(key=key).first()
        if item:
            session.delete(item)
            session.commit()
            return json_response({'success': 'item deleted successfully'}, 200)
        else:
            return json_response({'error': 'item does not exist'}, 404)
        
    else:
        return json_response({'error': 'missing parameter: key'}, 404)

def json_response(payload, status=200):
    return (json.dumps(payload), status, {'content-type': 'application/json'})


def main():
    if (len(sys.argv) < 2):
        print("Missing required parameters >>> python <main.py> <database.sqlite>")
        return

    db_name = sys.argv[1]
    engine = create_engine('sqlite:///' + db_name)
    Base.metadata.create_all(engine)
    Session.configure(bind=engine)
    app.run(port='11211')

if __name__ == '__main__': main()     