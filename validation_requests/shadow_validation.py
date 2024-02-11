def validate_shadow(request):
    # Verifica la presenza dei parametri obbligatori
    required_params = ['url']

    errors = {}

    # Verifica se la richiesta è JSON
    if not request.is_json:
        errors["error"] = "Richiesta non in formato JSON"
        return errors

    # Ottieni i dati JSON inviati con la richiesta
    data = request.get_json()
    for param in required_params:
        if param not in data:
            errors[param] = "Mancante"

    return errors
