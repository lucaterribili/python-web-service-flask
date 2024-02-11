from flask import Flask, request, jsonify
from pymysql import OperationalError
from database import BasicORM
import requests
from validation_requests.shadow_validation import validate_shadow

flask_service = Flask(__name__)


@app.route('/shadow', methods=['POST'])
def shadow():
    snakeORM = BasicORM()
    validation = validate_shadow(request)
    # validation
    if len(validation) != 0:
        return jsonify(validation, 400)
    result = ""
    charset = "UTF-8"
    params = request.get_json()
    # Get proxies
    query = """
    SELECT * FROM proxies ORDER BY RAND() LIMIT 3;
    """
    try:
        # EXECUTE query
        results = snakeORM.execute_query(query)

        # Stampa i risultati
        for row in results:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/58.0.3029.110 Safari/537.3'
            }
            proxies = {
                "http": f"http://{row['username']}:{row['password']}@{row['ip']}:{row['port']}",
                "https": f"http://{row['username']}:{row['password']}@{row['ip']}:{row['port']}",
            }
            response = requests.get(params['url'], proxies=proxies, headers=headers)
            status_code = response.status_code
            if status_code == 200:
                result = response.text
                charset = response.headers.get('Content-Type', '').split('; charset=')[-1]
                break
        # Chiudi la connessione al database
        snakeORM.close()

    except Exception as e:
        # Controlla se si tratta di OperationalError
        if isinstance(e, OperationalError):
            message = "Errore connessione al database: {}".format(e.args[0])
        else:
            # Gestisci altri tipi di errore
            message = "Errore interno: {}".format(e)
        return jsonify({'message': message, 'status': 'error'}), 500

    return jsonify({'message': 'Richiesta valida', 'response': result}), 200, {'Content-Type': 'application/json; '
                                                                                               'charset=' + charset}


if __name__ == '__main__':
    flask_service.run(host='0.0.0.0', port=8888)
