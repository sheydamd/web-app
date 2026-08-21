from app.database import SessionLocal, engine, Base
from app.models import Garage


Base.metadata.create_all(bind=engine)


db = SessionLocal()


garages = [
    Garage(
        name="تعمیرگاه علی",
        address="تهران، صادقیه",
        rating=4.5
    ),
    Garage(
        name="تعمیرگاه محمد",
        address="تهران، ستارخان",
        rating=4.2
    ),
]


db.add_all(garages)
db.commit()

db.close()

print("Garages added successfully!")