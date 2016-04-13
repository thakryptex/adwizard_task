from flask import Flask, jsonify
import db_handler as db
import string
import random


app = Flask(__name__)

db.check_existence()

symbols = string.ascii_letters + string.digits
size = 4
max = len(symbols) ** size  # 4 символа из 62 возможных с возможностью повторения символов внутри выборки


def generate_key():
    return ''.join([random.SystemRandom().choice(symbols) for _ in range(size)])


@app.route('/api/keys', methods=['GET'])
def keys_left():
    """
    :return: количество неиспользованных ключей
    """
    used = db.number_of_keys()
    left = max - used
    return jsonify({'keys left': left})


@app.route('/api/keys', methods=['POST'])
def key_new():
    """
    :return: генерирует новый ключ для клиента
    """
    if db.number_of_keys() == max:
        return jsonify({'message': "Key's limit is expired. Key can't be generated."})
    key = ''
    key_accepted = False
    while not key_accepted:
        key = generate_key()
        if not db.has_key(key):
            key_accepted = True
    db.add_key(key)
    return jsonify({'key': key})


@app.route('/api/keys/<string:key>', methods=['GET'])
def key_info(key):
    """
    :param key: ключ, по которому запрашивается информация в запросе
    :return: ключ и его статус
    """
    status = db.get_status(key)
    return jsonify({'key': key, 'status': status})


@app.route('/api/keys/<string:key>', methods=['PUT'])
def key_remove(key):
    """
    :param key: ключ, по которому запрашивается информация в запросе
    :return: ключ и сообщение об операции изменения статуса ключа
    """
    if not db.has_key(key):
        return jsonify({'key': key, 'message': "This key can't be marked as used, because it wasn't generated."})
    elif db.is_used(key):
        return jsonify({'key': key, 'message': "This key can't be marked as used, because it is already used."})
    else:
        db.mark_used(key)
        return jsonify({'key': key, 'message': 'This key is now marked as used.'})


if __name__ == '__main__':
    app.run(port=8000, debug=True)
