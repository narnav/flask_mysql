from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

# MySQL configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '123',
    'database': 'db1',
}

# Helper function to create a MySQL connection
def get_mysql_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    return "Welcome to the Flask-MySQL example!"


@app.route('/cars', methods=['GET'])
def get_cars():
    try:
        connection = get_mysql_connection()
        cursor = connection.cursor()

        # Fetch all cars from the 'cars' table
        cursor.execute('SELECT * FROM cars')
        cars = cursor.fetchall()

        # Convert the result to a list of dictionaries for JSON serialization
        cars_list = []
        for car in cars:
            car_dict = {
                'id': car[0],
                'model': car[1],
                'color': car[2]
            }
            cars_list.append(car_dict)

        cursor.close()
        connection.close()

        return jsonify(cars_list)
    except Exception as e:
        return jsonify({'error': str(e)})
@app.route('/cars', methods=['POST'])
def add_car():
    try:
        connection = get_mysql_connection()
        cursor = connection.cursor()

        # Get the model and color from the request body
        model = request.json['model']
        color = request.json['color']

        # Insert a new car into the 'cars' table
        cursor.execute('INSERT INTO cars (model, color) VALUES (%s, %s)', (model, color))
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
