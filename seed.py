# TODO: populate with location and user starter data

from app import app
from models import db, User, Listing


db.drop_all()
db.create_all()


l1 = Listing(
            title="pool",
            description="Backyard pool to escape the heat",
            location="San Francisco, CA",
            price=200,
            image_url="https://leisurepoolsusa.com/wp-content/uploads/2020/06/best-type-of-swimming-pool-for-my-home_2.jpg"
        )

db.session.add_all([l1])
db.session.commit()