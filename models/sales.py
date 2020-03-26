from app import db


class sales(db.Model):
    __tablename__ = 'new_buying_price'
    id = db.Column(db.Integer, primary_key= True)
    inventory_id= db.Column(db.Float, nullable= False)
    quantity = db.Column(db.Float,nullable=False)
    created_on = db.Column(db.Float,nullable=False)


    def sales(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def fetch_records(cls):
        inventory = cls.query.all()
        return inventory