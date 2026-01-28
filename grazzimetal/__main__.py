import os
import requests
import pandas as pd
from playwright.sync_api import sync_playwright, TimeoutError

def baixar_imagem_solopes(codigo: str, nome_arquivo: str) -> bool:
    url_base = "https://buscanarede.com.br/grazzimetal"

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            print("Abrindo site...")
            page.goto(url_base, timeout=15000, wait_until="domcontentloaded")

            page.wait_for_selector("#search", timeout=10000)
            page.fill("#search", codigo)
            page.keyboard.press("Enter")

            page.wait_for_selector("div.product-item", timeout=10000)

            img = page.query_selector("div.product-item a img.img-fluid")

            if not img:
                raise Exception("Imagem do produto não encontrada")

            img_url = img.get_attribute("src")

            if not img_url:
                raise Exception("SRC da imagem vazio")

            print(f"Imagem encontrada: {img_url}")

            os.makedirs("grazzimetal/images", exist_ok=True)

            response = requests.get(img_url, timeout=15)
            response.raise_for_status()

            with open(f"grazzimetal/images/{nome_arquivo}.jpg", "wb") as f:
                f.write(response.content)

            browser.close()
            print("✔ Imagem salva com sucesso")
            return True

    except TimeoutError:
        print("---> Timeout durante a automação")
        return False

    except Exception as e:
        print(f"---> Erro: {e}")
        return False




local_planilha = rf'grazzimetal\plan.xlsx'
planilha = pd.read_excel(local_planilha)
codigos = planilha['codigo']
qtd_codigos = len(codigos)

erros = []
indice_ok = 0
indice_erros = 0
for cod in codigos:
    print('-' * 120)
    nome = f'GRAZZIMETAL-{cod}'
    if baixar_imagem_solopes(codigo=cod, nome_arquivo=nome):
        indice_ok+=1
        print(f'Baixado com sucesso: {indice_ok}/{qtd_codigos}')
        continue
    else:
        indice_erros+=1
        erros.append(cod)


print("\nFinalizado")
print(f"Erros ({len(erros)}): {erros}")



