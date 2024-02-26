from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pytesseract
import cv2
import numpy as np
from pdf2image import convert_from_bytes
import os
import re

app = Flask(__name__, static_url_path='/static')
CORS(app)

def verificar_frase_chave(texto):
    frases_chave = [
        "Cobertura Superior",
        "cobertura premium",
        "1x Zurich Full Insurance EEA",
        "Esta apólice de seguro cobre o valor total",
        "cobre o valor total",
        "Full Protection Insurance",
        "Volledige beschermingsverzekering",
        "Volledige beschermi",
        "Volledige"
    ]

    for frase in frases_chave:
        if frase.lower() in texto.lower():
            return True

    return False

def sharpen_image(image):
    kernel = np.array([[-1, -1, -1],
                       [-1, 9, -1],
                       [-1, -1, -1]])
    return cv2.filter2D(image, -1, kernel)

def verificar_qualidade_imagem(imagem):
    # Define um limiar para determinar se a qualidade da imagem é baixa
    limiar_qualidade = 300

    laplacian_var = cv2.Laplacian(imagem, cv2.CV_64F).var()
    if laplacian_var < limiar_qualidade:
        return True
    return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    results = []

    files = request.files.getlist('files[]')

    for file in files:
        file_name = os.path.basename(file.filename) 
        pdf_bytes = file.read()

        # Converta o arquivo PDF em imagens PNG
        images = convert_from_bytes(pdf_bytes)

        quality_low = False  # Variável para verificar a qualidade baixa da imagem

        codigo_reserva = None

        for i, img in enumerate(images):
            img_np = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            
            # Converta a imagem para escala de cinza
            gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)

            # Ajuste gamma para aumentar o contraste
            gamma = 1.0
            adjusted = np.power(gray / float(np.max(gray)), gamma) * 255
            adjusted = np.uint8(adjusted)

            # Realize o OCR na imagem pré-processada
            texto = pytesseract.image_to_string(adjusted, lang='por')

            contem_frase_chave = verificar_frase_chave(texto)

            padrao = r"Reserva: (\w+-\d+)"
            # print("codigo_reserva", codigo_reserva)
            resultado = re.search(padrao, texto)
            if resultado:
                codigo_reserva = resultado.group(1)
            elif codigo_reserva is None:  # Verifica se codigo_reserva ainda não foi atribuído
                codigo_reserva = "Não possui código da reserva"

            
            # Verifica a qualidade da imagem
            if not quality_low:
                quality_low = verificar_qualidade_imagem(gray)

            results.append({
                'fileName': file_name,
                'text': texto,
                'containsKeyPhrase': contem_frase_chave,
                'codigoReserva': codigo_reserva,
                'isQualityLow': quality_low
            })

            if contem_frase_chave:
                break

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
