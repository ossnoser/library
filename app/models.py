from app import db
from datetime import datetime


class BookTitles:
    titles = [
        'Understanding The Linux Kernel',
        'OSGi In Action',
        'String Theory',
        'Change By Design',
        'QED',
        'Introduction to Electrodynamics',
        'Deep Learning with Python'
    ]


class BookRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True)
    title = db.Column(db.String(100), index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<BookRequest {}'.format(self.title)

    def from_dict(self, data):
        for field in ['email', 'title']:
            if field in data:
                setattr(self, field, data[field])

    def to_dict(self):
        data = {
            'id': self.id,
            'email': self.email,
            'title': self.title,
            'timestamp': self.timestamp,
        }

        return data

    def to_collection_list(query):
        data = [item.to_dict() for item in query.all()]
        return data
