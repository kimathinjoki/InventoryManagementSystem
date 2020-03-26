from app import db

class New_inventory(db.Model):
    __tablename__ = 'new_inventories'
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(40), nullable = False)
    type = db.Column(db.String(10), nullable= False)
    buying_price = db.Column(db.Float, nullable= False)
    selling_price = db.Column(db.Float, nullable= False)
    sales = db.relationship('New_sale', backref = 'inventory', lazy =True)
    stock = db.relationship("Add_stock", backref= "inventory", lazy = True)







    # adding inventories

    def add_inventory(self):
        db.session.add(self)
        db.session.commit()
    #
    # session.add - adds record
    # session.commit - send record to the db

    # fetch all records from databasa
    @classmethod
    def fetch_records(cls):
        inventory = cls.query.all()
        return inventory

    #fetch records id
    @classmethod
    def fetch_by_id(cls,id):
        return cls.query.filter_by(id=id).first()
