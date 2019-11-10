import datetime

from app.models import db

class Show(db.Model):
    __tablename__ = "shows"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)
    dash_src_video_url = db.Column(db.String(128), nullable=False)
    hls_src_video_url = db.Column(db.String(128), nullable=False)

    def __init__(self, title, description, dash_src_video_url, hls_src_video_url, 
        created_at=datetime.datetime.utcnow()):
        self.created_at = created_at
        self.title = title
        self.description = description
        self.dash_src_video_url = dash_src_video_url
        self.hls_src_video_url = hls_src_video_url

    def save(self):
        db.session.add(self)
        db.session.commit()
