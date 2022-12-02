# TODO: populate with location and user starter data

from app import db
from models import Listing, User


db.drop_all()
db.create_all()

u1 = User(
            username="testuser",
            password='password',
            email="user@email.com",
            first_name='First',
            last_name='Last',
            bio='bio is here',
            is_host=True,
)
db.session.add_all([u1])
db.session.commit()

l1 = Listing(
            title="Hauntingly Isolated",
            object_name='lakehouse',
            description="Remote",
            location="The lake",
            price=200,
            user_id=1,
            rating=5,
            image_url="https://kestrelbucket.s3.amazonaws.com/scarebnb/lakehouse.jpg"
        )

db.session.add_all([l1])
db.session.commit()