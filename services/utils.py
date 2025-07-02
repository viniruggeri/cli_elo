from datetime import datetime

# validação de data no formato yyyy-mm-dd
def validar_data(formato: str, data_str: str) -> bool:
    try:
        datetime.strptime(data_str, formato)
        return True
    except ValueError:
        return False