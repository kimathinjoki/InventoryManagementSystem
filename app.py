from flask import Flask,request,render_template,redirect,url_for
import pygal
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from config.config import Development

app = Flask(__name__)
app.config.from_object(Development)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:kimfelix09@127.0.0.1:5432/postgres'
# app.config['SECRET_KEY'] = 'hihcfgndiajhfapp'
# app.config['SQL_TRACK-MODIFICATIONS'] =False
db = SQLAlchemy(app)

from models.inventory import New_inventory
from models.new_sales import New_sale
from models.stock import Add_stock



# class New_inventory(db.Model):
#     __tablename__ = 'new_inventories'
#     id = db.Column(db.Integer, primary_key= True)
#     name = db.Column(db.String(40), nullable = False)
#     type = db.Column(db.String(10), nullable= False)
#     buying_price = db.Column(db.Float, nullable= False)
#     selling_price = db.Column(db.Float, nullable= False)
#
# class New_buying_price(db.Model):
#     tablename = 'new_buying_price'
#     id = db.Column(db.Integer, primary_key= True)
#     old_price= db.Column(db.Float, nullable= False)
#     new_price = db.Column(db.Float,nullable=False)
#
# class New_selling_price(db.Model):
#     tablename = 'new_selling_price'
#     id = db.Column(db.Integer, primary_key= True)
#     old_price= db.Column(db.Float, nullable= False)
#     new_price = db.Column(db.Float,nullable=False)

@app.before_first_request
def create_tables():
    db.create_all()


connection = psycopg2.connect(user = "postgres",
                              password = "kimfelix09",
                              host = "127.0.0.1",
                              port = "5432",
                              database = "postgres")

cursor = connection.cursor()
# Print PostgreSQL Connection properties
# print ( connection.get_dsn_parameters(),"\n")



@app.route('/')
def index():
    cursor.execute("""SELECT type, COUNT (type)
   FROM inventories
   GROUP BY type;""")
    record = cursor.fetchall()


    print(record[0][0])


    pie_chart = pygal.Pie()
    pie_chart.title = 'Vegetables vs Fruits'
    pie_chart.add(record[0][0],record [0][1])
    pie_chart.add(record[1][0],record [1][1])

    # pie_chart.add('IE', [5.7, 10.2, 2.6, 1])
    # pie_chart.add('Firefox', [.6, 16.8, 7.4, 2.2, 1.2, 1, 1, 1.1, 4.3, 1])
    # pie_chart.add('Chrome', [.3, .9, 17.1, 15.3, .6, .5, 1.6])
    # pie_chart.add('Safari', [4.4, .1])
    # pie_chart.add('Opera', [.1, 1.6, .1, .5])
    pie_chart.render()

    pie = pie_chart.render_data_uri()

    # this is a line graph of the same representation


    cursor.execute(
        """SELECT EXTRACT(MONTH FROM s.created_on) AS sales_month, SUM(i.selling_price * s.quantity) AS subtotal
   FROM sales AS s
   JOIN inventories AS i ON s.inventory_id = i.id
   GROUP BY sales_month
   ORDER BY sales_month; """
    )
    sales = cursor.fetchall()
    x = []
    y = []
    for each in sales:
        x.append(each[0])
        y.append(each[1])



    line_chart = pygal.Line()
    line_chart.title = 'Vegetables vs Fruits'

    line_chart.x_labels = x
    line_chart.add('sales',y)
    # line_chart.x_labels = map(str, range(2002, 2013))
    # line_chart.add('Firefox', [None, None, 0, 16.6, 25, 31, 36.4, 45.5, 46.3, 42.8, 37.1])
    # line_chart.add('Chrome', [None, None, None, None, None, None, 0, 3.9, 10.8, 23.8, 35.3])
    # line_chart.add('IE', [85.8, 84.6, 84.7, 74.5, 66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
    # line_chart.add('Others', [14.2, 15.4, 15.3, 8.9, 9, 10.4, 8.9, 5.8, 6.7, 6.8, 7.5])
    # line_chart.render()

    line = line_chart.render_data_uri()

    return render_template('index.html', pie=pie, line=line)


@app.route('/inventory',methods = ['GET','POST'])
def inventory():

    inventories = New_inventory.fetch_records()
    # print(inventories)
    cursor.execute("""SELECT inventory_id, sum(quantity) as "stock"
       FROM ((SELECT st.inventory_id, sum(stock) as "quantity"
       FROM public.add_stock as st
       GROUP BY inventory_id) union all
           (SELECT sa.inventory_id, - sum(quantity) as "quantity"
       FROM public.new_sale as sa
       GROUP BY inventory_id) 
           ) stsa
       GROUP BY inventory_id
       ORDER BY inventory_id;""")

    available_stock = cursor.fetchall()


    if request.method == 'POST':
        name = request.form['name']
        type = request.form['type']
        bp = request.form['bp']
        sp = request.form['sp']

        print(name)
        print(type)
        print(bp)
        print(sp)

        new_inventory = New_inventory(name=name, type=type,buying_price = bp, selling_price=sp)
        new_inventory.add_inventory()

        return redirect(url_for('inventory'))

    return render_template('inventory.html',inventories = inventories,available_stock=available_stock)

# deleting an item
@app.route('/inventory/delete/<int:id>', methods=["GET","POST"])
def deleteInventory(id):

    delete_inventory = New_inventory.fetch_by_id(id)
    print('Record deleted successfully')
    if delete_inventory:
        db.session.delete(delete_inventory)
        db.session.commit()

        return redirect(url_for('inventory'))
    else:
        print('Record not found')
        return redirect(url_for('inventory'))


@app.route('/new_sale/<int:id>',methods=["GET","POST"])
def new_sale(id):

    if request.method == 'POST':

        # quantity = request.form['quantity']

#         push to db

        quantity = request.form['quantity']
        new_sale = New_sale(inventory_id=id, quantity=quantity)
        db.session.add(new_sale)
        db.session.commit()

    return  redirect(url_for('inventory'))


@app.route('/add_stock/<int:id>', methods=["GET","POST"])
def add_stock(id):

    if request.method == 'POST':
        quantity = request.form['quantity']
        add_stock = Add_stock(inventory_id=id, stock=quantity)
        db.session.add(add_stock)
        db.session.commit()



    return  redirect(url_for("inventory"))


@app.route('/view_sales/<int:id>', methods= ['POST','GET'])

def view_sales(id):
    sales = New_sale.query.filter_by(inventory_id=id).all()

    return render_template('views.html', sales=sales)











# @app.route('/about')
# def about():
#
#     return render_template('about.html')
@app.route('/add/<int:x>/<int:y>')
def add(x,y):
    total = x+y

    return render_template('add.html', total=total)

# @app.route('/contact')
# def contact():
#     return render_template('contact.html')





if __name__ == '__main__':
    app.run()

