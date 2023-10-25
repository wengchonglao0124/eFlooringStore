from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from .models import FlooringType, Specification, ProjectPhoto, Flooring, Order, OrderDetail, CustomerDetail
from .forms import CheckoutForm
from . import db
from datetime import datetime


bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    home_project_photos = db.session.scalars(db.select(ProjectPhoto).filter(ProjectPhoto.image.in_(["p503.png", "p105.png", "p201.png"])).order_by(ProjectPhoto.image.desc())).all()

    order = getOrder()
    orderdetails = db.session.scalars(db.select(OrderDetail).where(OrderDetail.order==order).order_by(OrderDetail.quantity.desc())).all()

    return render_template('index.html', homeActive = "active", home_project_photos = home_project_photos, orderdetails = orderdetails)


@bp.route('/search')
def search():
    search = request.args.get('search')
    search_like = '%{}%'.format(search)

    query1 = Flooring.query.join(FlooringType, Flooring.type_id == FlooringType.id).filter(FlooringType.type.like(search_like))
    query2 = Flooring.query.filter(Flooring.subtype.like(search_like))
    query3 = Flooring.query.filter(Flooring.colour.like(search_like))
    query4 = Flooring.query.join(Specification, Flooring.specification_id == Specification.id).filter(Specification.size.like(search_like))
    query5 = Flooring.query.join(Specification, Flooring.specification_id == Specification.id).filter(Specification.component.like(search_like))

    products = query1.union(query2, query3, query4, query5).all()

    return render_template('search.html', floorings=products, keyword=search)


@bp.route('/floorings')
def floorings():

    natural_type = db.session.scalars(db.select(FlooringType).where(FlooringType.type=='Natural')).first()
    natural_floorings = db.session.scalars(db.select(Flooring).where(Flooring.type_id==natural_type.id).order_by(Flooring.id)).all()

    hybrid_type = db.session.scalars(db.select(FlooringType).where(FlooringType.type=='Hybrid')).first()
    hybrid_floorings = db.session.scalars(db.select(Flooring).where(Flooring.type_id==hybrid_type.id).order_by(Flooring.id)).all()

    laminate_type = db.session.scalars(db.select(FlooringType).where(FlooringType.type=='Laminate')).first()
    laminate_floorings = db.session.scalars(db.select(Flooring).where(Flooring.type_id==laminate_type.id).order_by(Flooring.id)).all()

    vinyl_type = db.session.scalars(db.select(FlooringType).where(FlooringType.type=='Vinyl')).first()
    vinyl_floorings = db.session.scalars(db.select(Flooring).where(Flooring.type_id==vinyl_type.id).order_by(Flooring.id)).all()

    order = getOrder()
    orderdetails = db.session.scalars(db.select(OrderDetail).where(OrderDetail.order==order).order_by(OrderDetail.quantity.desc())).all()

    return render_template('floorings.html', flooringsActive = "active", natural_floorings = natural_floorings, hybrid_floorings = hybrid_floorings, laminate_floorings = laminate_floorings, vinyl_floorings = vinyl_floorings, orderdetails = orderdetails)


@bp.route('/tiles')
def tiles():

    tile_type = db.session.scalars(db.select(FlooringType).where(FlooringType.type=='Tile')).first()
    tile_floorings = db.session.scalars(db.select(Flooring).where(Flooring.type_id==tile_type.id).order_by(Flooring.id)).all()
    
    order = getOrder()
    orderdetails = db.session.scalars(db.select(OrderDetail).where(OrderDetail.order==order).order_by(OrderDetail.quantity.desc())).all()

    return render_template('tiles.html', tilesActive = "active", tile_floorings = tile_floorings, orderdetails = orderdetails)


@bp.route('/special')
def specialDiscount():

    order = getOrder()
    orderdetails = db.session.scalars(db.select(OrderDetail).where(OrderDetail.order==order).order_by(OrderDetail.quantity.desc())).all()
    
    special_discount_floorings = db.session.scalars(db.select(Flooring).where(Flooring.discount<1).order_by(Flooring.discount)).all()
    return render_template('specialDiscount.html', specialActive = "active", special_discount_floorings = special_discount_floorings, orderdetails = orderdetails)


@bp.route('/details/<string:flooring_id>')
def details(flooring_id):
    
    try:
        product = db.session.scalars(db.select(Flooring).where(Flooring.id==flooring_id)).first()
        
        order = getOrder()
        orderdetails = db.session.scalars(db.select(OrderDetail).where(OrderDetail.order==order).order_by(OrderDetail.quantity.desc())).all()

        return render_template('details.html', flooring = product, orderdetails = orderdetails)
    except:
        return render_template('error.html', error="Item not found")
    

@bp.route('/redirect/<string:flooring_type>')
def redirect_route(flooring_type):

    if flooring_type.lower() == 'natural' or flooring_type.lower() == 'hybrid' or flooring_type.lower() == 'laminate' or flooring_type.lower() == 'vinyl':
        return redirect(url_for('main.floorings') + f'#{flooring_type.lower()}')
    
    elif flooring_type.lower() == 'tile':
        return redirect(url_for('main.tiles'))


@bp.route('/addorder', methods=['POST', 'GET'])
def addOrder():
    product_id = request.values.get('product_id')
    quantity = int(request.values.get('quantity_input'))
    print(f'Request to add order#\nProduct: {product_id}\nQuantity: {quantity}')

    order = getOrder()

    # are we adding an item?
    if product_id is not None and order is not None:

        product = db.session.scalar(db.select(Flooring).where(Flooring.id==product_id))

        orderDetail = db.session.scalar(db.select(OrderDetail).where(OrderDetail.order==order, OrderDetail.flooring==product))
        if orderDetail is not None:
            orderDetail.quantity += quantity
            try:
                updateTotalPrice()
                db.session.commit()
            except:
                flash('There was an issue updating the item to your cart',category='danger')
        
        else:
            orderDetail = OrderDetail(order=order, flooring=product, quantity=quantity)
            try:
                db.session.add(orderDetail)
                updateTotalPrice()
                db.session.commit()
            except:
                flash('There was an issue adding the item to your cart',category='danger')

    flash(f'Successfully added {quantity} [boxes] of {product.type.type} Flooring - {product.subtype} {product.colour} to Cart',category='danger')
    return redirect(url_for('main.details', flooring_id=product_id))


def getOrder() -> Order:
    # retrieve order if there is one
    if 'order_id' in session.keys():
        order = db.session.scalar(db.select(Order).where(Order.id==session['order_id']))
        # order will be None if order_id/session is stale
    else:
        # there is no order
        order = None

    # create new order if needed
    if order is None:
        order = Order(order_status=False, date=datetime.now(), total_price=0)
        try:
            db.session.add(order)
            db.session.commit()
            session['order_id'] = order.id
        except:
            print('Failed trying to create a new order!')
            order = None
    
    return order


@bp.route('/shoppingcart')
def shoppingcart():
    order = getOrder()
    orderdetails = db.session.scalars(db.select(OrderDetail).where(OrderDetail.order==order).order_by(OrderDetail.flooring_id)).all()

    return render_template('cart.html', cartActive = "active", orderdetails = orderdetails)


@bp.route('/changeorder/<string:action>/<string:product_id>')
def changeOrder(product_id, action):
    
    quantity = 1
    print(f'Request to {action} order#\nProduct: {product_id}\nQuantity: {quantity}')

    order = getOrder()

    # are we adding an item?
    if product_id is not None and order is not None:

        product = db.session.scalar(db.select(Flooring).where(Flooring.id==product_id))
        orderDetail = db.session.scalar(db.select(OrderDetail).where(OrderDetail.order==order, OrderDetail.flooring==product))

        if orderDetail is not None:
            if action == "add":
                orderDetail.quantity += quantity
                updateTotalPrice()

            elif action == "minus":
                orderDetail.quantity -= quantity
                updateTotalPrice()
                
                if orderDetail.quantity < 1:
                    return redirect(url_for('main.deleteorderitem', product_id=product_id))

            try:
                db.session.commit()
            except:
                flash('There was an issue updating the item to your cart',category='danger')

    return redirect(url_for('main.shoppingcart'))


@bp.route('/deleteorderitem/<string:product_id>')
def deleteorderitem(product_id):
    
    if 'order_id' in session:
        order = getOrder()
        product = db.session.scalar(db.select(Flooring).where(Flooring.id==product_id))
        product_detail_to_delete = db.session.scalar(db.select(OrderDetail).where(OrderDetail.order==order, OrderDetail.flooring==product))
        
        if product_detail_to_delete is not None:
            try:
                db.session.delete(product_detail_to_delete)
                updateTotalPrice()
                db.session.commit()
                
                flash(f'Successfully removed all of {product.type.type} Flooring - {product.subtype} {product.colour} to Cart',category='danger')
                return redirect(url_for('main.shoppingcart'))
            
            except:
                flash('Problem deleting item from order')

    return redirect(url_for('main.index'))


# Scrap basket
@bp.route('/deleteorder')
def deleteorder():
    if 'order_id' in session:
        del session['order_id']
        flash('All items deleted')
    return redirect(url_for('main.index'))


def updateTotalPrice():
    order = getOrder()
    orderDetails = db.session.scalars(db.select(OrderDetail).where(OrderDetail.order==order))

    if orderDetails is not None:
        total_price = 0
        for orderDetail in orderDetails:
            item = orderDetail.flooring
            total_price += orderDetail.quantity * item.price * item.discount

        order.total_price = total_price
        db.session.commit()


# Complete the order
@bp.route('/checkout', methods=['POST','GET'])
def checkout():
    form = CheckoutForm() 
    if 'order_id' in session:
        order = getOrder()
        orderdetails = db.session.scalars(db.select(OrderDetail).where(OrderDetail.order==order).order_by(OrderDetail.quantity.desc())).all()

        if form.validate_on_submit():
            order.order_status = True
            email=form.email.data
            customer = db.session.scalar(db.select(CustomerDetail).where(CustomerDetail.email==email))

            if customer is not None:
                customer.firstname=form.firstname.data
                customer.lastname=form.lastname.data
                customer.phone=form.phone.data
                customer.address=form.address.data

            else:
                customer = CustomerDetail(
                    firstname=form.firstname.data,
                    lastname=form.lastname.data,
                    email=email,
                    phone=form.phone.data,
                    address=form.address.data)
                
            order.customer = customer
            order.date = datetime.now()

            try:
                db.session.commit()
                del session['order_id']
                flash('Thank you for your order! Your order is now being processed! You will receive the email notification for any update.')
                return redirect(url_for('main.shoppingcart'))
            except:
                flash('There was an issue completing your order')
            
        return render_template('checkout.html', checkoutActive='active', form=form, total_price=order.total_price, orderdetails = orderdetails)
    