from flask import Flask, render_template
import string
import random

app = Flask(__name__)

def senha_aleatoria(tamanho=10, caracteres = string.ascii_lowercase + string.ascii_uppercase + string.digits):
    return ''.join(random.choice(caracteres) for _ in range(tamanho))

@app.route('/')
def senha(tamanho = 10, caracteres = string.ascii_lowercase + string.ascii_uppercase + string.digits):
        senha = senha_aleatoria(tamanho, caracteres)
        return render_template('senha.html', senha=senha)

if __name__ == '__main__':
    app.run(debug=True)

