from app import db
from datetime import datetime

class Add_stock(db.Model):
    __tablename__ = 'add_stock'
    id = db.Column(db.Integer, primary_key= True)
    inventory_id= db.Column(db.Integer, db.ForeignKey("new_inventories.id"), nullable= False)
    stock = db.Column(db.Float,nullable=False)
    created_on = db.Column(db.DateTime,default=datetime.utcnow)


    def add_stock(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def fetch_records(cls):
        inventory = cls.query.all()
        return inventory

    @classmethod
    def fetch_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

