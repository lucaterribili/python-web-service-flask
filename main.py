from flask import Flask, request, jsonify
import requests

app = Flask(__name__)


@app.route('/shadow', methods=['POST'])
def hello():
    # Assicurati che il corpo della richiesta sia JSON
    if request.is_json:
        # Ottieni i dati JSON inviati con la richiesta
        data = request.get_json()

        # Utilizza i dati ricevuti, per esempio, stampa il nome
        name = data.get('name', 'Guest')  # Predefinito a 'Guest' se 'name' non è presente

        # Restituisci una risposta JSON
        return jsonify({'message': f'Hello, {name}!'}), 200
    else:
        return jsonify({"error": "La richiesta deve essere JSON"}), 400


if __name__ == '__main__':
    app.run(debug=True)
