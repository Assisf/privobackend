from flask import Flask, request, jsonify
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import subprocess

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/imprimir", methods=["POST"])
def imprimir():
    data = request.get_json()
    numero_pedido = data.get("numero_pedido")
    itens = data.get("itens", [])

    # Gera o PDF
    nome_arquivo = f"pedido_{numero_pedido}.pdf"
    c = canvas.Canvas(nome_arquivo, pagesize=A4)
    width, height = A4

    y = height - 50
    c.drawString(50, y, f"Pedido Nº: {numero_pedido}")
    y -= 30
    
    total = 0
    for item in itens:
        linha = f"{item['quantidade']}x {item['nome']} - R$ {item['preco']:.2f}"
        c.drawString(50, y, linha)
        total += item["quantidade"] * item["preco"]
        y -= 20

    y -= 10
    c.drawString(50, y, f"Total: R$ {total:.2f}")

    # Adiciona rodapé com o nome da empresa
    rodape_y = 30
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(width / 2, rodape_y, "Infinity Software")

    c.save()

    # Windows: chama o notepad para imprimir (vai abrir caixa de diálogo e permitir escolher Microsoft Print to PDF)
    # Isso só funciona porque o notepad /p manda direto para a impressora padrão (ou pede escolha)
    try:
        subprocess.run(["notepad", "/p", nome_arquivo], check=True)
    except Exception as e:
        return jsonify({"erro": f"Erro ao tentar imprimir: {e}"}), 500

    return jsonify({"mensagem": f"Pedido {numero_pedido} gerado e enviado para a impressão!"})

if __name__ == "__main__":
    app.run(debug=True)
