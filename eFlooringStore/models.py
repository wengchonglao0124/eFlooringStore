from . import db


class FlooringType(db.Model):
    __tablename__ = 'flooringTypes'
    id = db.Column(db.String(10), primary_key=True)
    type = db.Column(db.String(25), unique=True, nullable=False)
    floorings = db.relationship('Flooring', backref='type', cascade="all, delete-orphan")
    project_photos = db.relationship('ProjectPhoto', backref='type', cascade="all, delete-orphan")

    def __repr__(self):
        return f"ID: {self.id}\nType: {self.type}"


class Specification(db.Model):
    __tablename__ = 'specifications'
    id = db.Column(db.String(10), primary_key=True)
    size = db.Column(db.String(25), nullable=False)
    component = db.Column(db.String(100))
    area_per_box = db.Column(db.Float, nullable=False)
    pieces_per_box = db.Column(db.Integer, nullable=False)
    floorings = db.relationship('Flooring', backref='specification', cascade="all, delete-orphan")

    def __repr__(self):
        return f"ID: {self.id}\nSize: {self.size}\nComponent: {self.component}\nArea per Box: {self.area_per_box}\nPieces per Box: {self.pieces_per_box}"


flooringdetails = db.Table('flooringdetails', 
    db.Column('flooring_id', db.String(10), db.ForeignKey('floorings.id'), nullable=False),
    db.Column('project_photo_image', db.String(60), db.ForeignKey('projectPhotos.image'), nullable=False),
    db.PrimaryKeyConstraint('flooring_id', 'project_photo_image'))


class ProjectPhoto(db.Model):
    __tablename__ = 'projectPhotos'
    image = db.Column(db.String(60), primary_key=True)
    type_id = db.Column(db.String(10), db.ForeignKey('flooringTypes.id'), nullable=False)

    def __repr__(self):
        return f"Image: {self.image}\nType: {self.type_id}"


class Flooring(db.Model):
    __tablename__ = 'floorings'
    id = db.Column(db.String(10), primary_key=True)
    type_id = db.Column(db.String(10), db.ForeignKey('flooringTypes.id'), nullable=False)
    subtype = db.Column(db.String(25), nullable=False)
    colour = db.Column(db.String(25), nullable=False)
    specification_id = db.Column(db.String(10), db.ForeignKey('specifications.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Float, default=1)
    image = db.Column(db.String(60), unique=True, nullable=False)
    project_photos = db.relationship("ProjectPhoto", secondary=flooringdetails, backref="floorings")
    orderdetails = db.relationship('OrderDetail', backref='flooring', cascade="all, delete-orphan")

    def __repr__(self):
        return f"ID: {self.id}\nType: {self.type_id}\nSubtype: {self.subtype}\nColour: {self.colour}\nSpecification: {self.specification_id}\nPrice: {self.price}\nDiscount: {self.discount}\nImage: {self.image}"


class OrderDetail(db.Model):
    __tablename__ = 'orderdetails'
    order_id = db.Column('order_id', db.Integer, db.ForeignKey('orders.id'), primary_key=True)
    flooring_id = db.Column('flooring_id', db.String(10), db.ForeignKey('floorings.id'), primary_key=True)
    quantity = db.Column('quantity', db.Integer, nullable=False, default=1)

    def __repr__(self):
        return f"Order ID: {self.order_id}\nFlooring ID: {self.flooring_id}\nQuantity: {self.quantity}"


class Order(db.Model):
    __tablename__='orders'
    id = db.Column(db.Integer, primary_key=True)
    order_status = db.Column(db.Boolean, default=False)
    date = db.Column(db.DateTime)
    total_price = db.Column(db.Float)
    customer_id = db.Column(db.Integer, db.ForeignKey('customerDetails.id'))
    orderdetails = db.relationship('OrderDetail', backref='order', cascade="all, delete-orphan")
    
    def __repr__(self):
        text = "ID:{}\n, Order Status:{}\n, Date:{}\n, Products:{}\n, Total Price:{}\n, Customer:{}"
        text = str.format(self.id, self.order_status, self.date, self.products, self.total_price, self.customer_id)
        return text 
     
    
class CustomerDetail(db.Model):
    __tablename__='customerDetails'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(32), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    orders = db.relationship('Order', backref='customer', cascade="all, delete-orphan")

    def __repr__(self):
        text = "ID:{}\n, Firstname:{}\n, Lastname:{}\n, Email:{}\n, Phone:{}\n, Shipping Address:{}"
        text = str.format( self.id, self.firstname, self.lastname, self.email, self.phone, self.address)
        return text

