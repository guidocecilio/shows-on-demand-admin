from app import current_app
from app.models import db
from app.models.user import User
from app.models.show import Show
from app.api.helpers.db import get_or_create

def create_shows():
    get_or_create(
        Show, 
        title='Cyclist',
        description='The cyclist that needed to change his bike',
        hls_src_video_url="https://content.jwplatform.com/manifests/yp34SRmf.m3u8",
        dash_src_video_url=""
    )

def create_users():
    get_or_create(User, username='guidocecilio', email='guidocecilio@gmail.com', password='test')
    get_or_create(User, username='guidoenmanuel', email='guidoenmanuel@gmail.com', password='test')


def populate():
    """
    Create default Users and Shows.
    """
    create_users()
    create_shows()

    db.session.commit()