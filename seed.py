# TODO: populate with location and user starter data

from app import app
from models import db, User, Listing


db.drop_all()
db.create_all()


# c2 = Cupcake(
#     flavor="chocolate",
#     size="small",
#     rating=9,
#     image="https://www.bakedbyrachel.com/wp-content/uploads/2018/01/"
#           "chocolatecupcakesccfrosting1_bakedbyrachel.jpg"
# )

# db.session.add_all([c1, c2])
# db.session.commit()