import qrcode
from fastapi import FastAPI
from fastapi.responses import FileResponse
import uuid
from PIL import Image

app = FastAPI()

# Defina sua chave PIX
CHAVE_PIX = "sua_chave_pix_aqui"

def gerar_qrcode_pix(valor: float, chave_pix: str):
    # Criando o código Pix com base nas informações de pagamento
    pix_data = {
        "chave": chave_pix,
        "valor": valor,
        "nome": "Seu Nome ou Razão Social",
        "cidade": "Sua Cidade",
        "codigo_banco": "001",  # Código do Banco Central para o Pix
    }

    payload = f"00020101021126530014br.gov.bcb.pix01{pix_data['chave']}520400005303986540000{valor:.2f}5802BR5909{pix_data['nome']}6009{pix_data['cidade']}62070503{pix_data['codigo_banco']}63"

    qr = qrcode.make(payload)
    arquivo_qr = f"qr_code_{uuid.uuid4()}.png"
    qr.save(arquivo_qr)

    return arquivo_qr

@app.get("/gerar_qrcode_pix")
def gerar_qrcode(valor: float):
    arquivo_qr = gerar_qrcode_pix(valor, CHAVE_PIX)
    return FileResponse(arquivo_qr, media_type="image/png", filename="qrcode_pix.png")
