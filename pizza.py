from flask import Flask, request
import connectdb as connect
import responseformat as res
import error1 as err

app = Flask(__name__)


@app.route("/display", methods=["get", "post"])
def display():
    database = "pizza"
    conn = connect.ConnectMySql(database)
    table_name = "user"
    print(f"Connection status : {conn}")

    if conn is False:
        return err.ReturnConnectionError()
    else:
        try:
            cur = conn.cursor()
            print(f"Cursor object : {cur}")
            cur.execute("select * from {}".format(table_name))
            msg = "Data fetched succesfully"
            return res.generateResponse(cur, msg)
        except Exception as e:
            print(e)
            return err.ReturnFetchError()
        finally:
            conn.close()


@app.route("/insert", methods=["get", "post"])
def insert():
    database = "pizza"
    table_name = "order_details"
    conn = connect.ConnectMySql(database)
    print(f"Connection status : {conn}")

    if conn is False:
        return err.ReturnConnectionError()
    else:
        try:
            cur = conn.cursor()
            print(f"Cursor object : {cur}")
            cur.execute("select max(order_id) from {}".format(table_name))
            data = cur.fetchone()
            order_id = int(data[0]) + 1
            cur.execute("select max(user_id) from user")
            data = cur.fetchone()
            user_id = int(data[0]) + 1
            data = request.get_json(silent=True, force=True)
            query_result = data.get('queryResult')
            pizza_type = (query_result.get('parameters').get('pizza_type'))
            pizza_variety = (query_result.get('parameters').get('pizza_variety'))
            pizza_size = (query_result.get('parameters').get('pizza_size'))
            quantity = (query_result.get('parameters').get('quantity'))
            toppings = (query_result.get('parameters').get('toppings'))
            crust_type = (query_result.get('parameters').get('crust_type'))
            values = (order_id, pizza_type, pizza_variety, pizza_size, quantity, toppings, crust_type)
            cur.execute(f"insert into {table_name} values {values}")
            name = (query_result.get('parameters').get('name'))
            address = (query_result.get('parameters').get('address'))
            phone = (query_result.get('parameters').get('phone-number'))
            values = (user_id, name, phone, address, order_id)
            table_name = "user"
            cur.execute(f"insert into {table_name} values {values}")
            return {
                "fulfillmentText": 'order placed successfully\n'
                                   'your order details as follows:\n'
                                   'user-name:' + name + '\n'
                                                         'address:' + address + '\n'
                                                                                'mobile:' + phone + '\n'
                                                                                                    'order_id:' + str(
                    order_id) + '\n'
                                'pizza-type:' + pizza_type + '\n'
                                                             'pizza_variety:' + pizza_variety + '\n'
                                                                                                'pizza-size:' + pizza_size + '\n'
                                                                                                                             'quantity:' + quantity + '\n'
                                                                                                                                                      'toppings:' + toppings + '\n'
                                                                                                                                                                               'crust-type:' + crust_type + '\n'
            }
        except Exception as e:
            print(e)
        finally:
            conn.commit()
            conn.close()


@app.route("/order_status", methods=["get", "post"])
def order_status():
    database = "pizza"
    conn = connect.ConnectMySql(database)
    print(f"Connection status : {conn}")

    if conn is False:
        return err.ReturnConnectionError()
    else:
        try:
            cur = conn.cursor()
            print(f"Cursor object : {cur}")
            data = request.get_json(silent=True, force=True)
            query_result = data.get('queryResult')
            order_id = (query_result.get('parameters').get('number'))
            # print(order_id)
            cur.execute("SELECT user.order_id, name, status FROM user "
                        "INNER JOIN order_status ON user.order_id =order_status.order_id "
                        f"and user.order_id={order_id};")
            data = cur.fetchone()
            id, name, status = data
            # return [id, name, status]
            return {
                "fulfillmentText": 'order placed successfully\n'
                                   'your order details as follows:\n'
                                   'order_id:' + id + '\n'
                                   'name:' + name + '\n'
                                   'status:' + status + '\n'
            }
        except Exception as e:
            print(e)
            return err.ReturnFetchError()
        finally:
            conn.close()


if __name__ == "__main__":
    app.run(debug=True, port=5000)
