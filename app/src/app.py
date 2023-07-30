from flask import Flask, render_template, request
from distributer import distribute_funds
from values import api_key, api_secret

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            coin = request.form.get('coin')
            addresses = request.form.get('addresses').split(',')
            min_amount = float(request.form.get('min_amount'))
            max_amount = float(request.form.get('max_amount'))
            network = 'Arbitrum'  # Default network

            # Call distribute_funds function
            try:
                distribute_funds(api_key, api_secret, coin, addresses, min_amount, max_amount, network)
                return "Funds distributed successfully", 200
            except ValueError as e:
                return str(e), 400 # Return the error message and a 400 status code
        except Exception as e:
            return str(e), 500

    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
