from flask import Flask, request, jsonify
import connectdb as connect
import responseformat as res
import error as err

app = Flask(__name__)


@app.route("/display", methods=["get", "post"])
def fetch():
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
            query = ("select * from {}".format(table_name))
            cur.execute(query)
            msg = "Data fetched succesfully"
            return res.generateResponse(cur, msg)
        except Exception as e:
            print(e)
            return err.ReturnFetchError()
        finally:
            conn.close()


@app.route("/insert", methods=["get", "post"])
def insertData():
    database = "pizza"
    table_name = "user"
    conn = connect.ConnectMySql(database)
    print(f"Connection status : {conn}")

    if conn is False:
        return err.ReturnConnectionError()
    else:
        try:
            cur = conn.cursor()
            print(f"Cursor object : {cur}")
            values = [105,'lakshmi','9182736455',5]
            query = ("insert into {} values ({})".format(table_name, values))
            cur.execute(query)
            msg = "data inserted successfully"
            return jsonify(
            {"fulfillmentMessages": [{"text": {"text": ["inserted successfully"]}}]}
            )
        except Exception as e:
            print(e)
            return err.ReturnFetchError()
        finally:
            conn.commit()
            conn.close()


if __name__ == "__main__":
    app.run(debug=True, port=3000)

