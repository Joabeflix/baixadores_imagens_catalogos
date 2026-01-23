from playwright.sync_api import sync_playwright, TimeoutError
import pandas as pd
import os

configuracoes = {
    "INTERRUPTOR EMBREAGEM": [
        "interruptor-de-embreagem-27"
        ],

    "INTERRUPTOR LUZ FREIO": [
        "interruptor-de-luz-de-freio-120",
        "interruptor-de-luz-de-freio",
        "interruptor-de-luz-de-freio-123"
        ],

    "INTERRUPTOR FREIO": [
        "interruptor-de-luz-de-freio-120",
        "interruptor-de-luz-de-freio",
        "interruptor-de-luz-de-freio-123"
        ],

    "INTERRUPTOR LUZ RE": [
        "interruptor-de-luz-de-re-114"
        ],

    "INTERRUPTOR LUZ RET1 02": [
        "interruptor-de-luz-de-re-114"
        ],
    "INTERRUPTOR OLEO MOTOR": [
        "interruptor-de-pressao-de-oleo-117",
        "sensor-mecanico-de-pressao-22",
        "interruptor-de-pressao-de-oleo-113",
        "sensor-eletronico-de-pressao-67"
        ],

    "INTERRUPTOR OLEO MOTOR 0.30 BAR": [
        "interruptor-de-pressao-de-oleo-117",
        "sensor-mecanico-de-pressao-22",
        "interruptor-de-pressao-de-oleo-113",
        "sensor-eletronico-de-pressao-67"
        ],

    "INTERRUPTOR PEDAL EMBREAGEM": [
        "interruptor-de-embreagem-27"
        ],

    "INTERRUPTOR PNEUMATICO FREIO ESTACIONAMENTO": [
        "interruptor-pneumatico-34"
    ],

    "INTERRUPTOR PRESSAO DIRECAO HIDRAULICA": [
        "interruptor-de-pressao-da-direcao-hidraulica-7",
        "interruptor-de-pressao-da-direcao-hidraulica"
    ],

    "INTERRUPTOR PRESSAO HIDRAULICO": [
        "interruptor-de-pressao-da-direcao-hidraulica-7",
        "interruptor-de-pressao-da-direcao-hidraulica"  
    ],

    "INTERRUPTOR PRESSAO OLEO": [
        "interruptor-de-pressao-de-oleo-117",
        "sensor-mecanico-de-pressao-22",
        "interruptor-de-pressao-de-oleo-113",
        "sensor-eletronico-de-pressao-67"
        ],

    "INTERRUPTOR REDUCAO": [
        "interruptor-de-transferencia-51"
    ],

    "SENSOR PRESSAO AR": [
        "sensor-eletronico-de-pressao-65",
        "sensor-eletronico-de-pressao-73"
    ],

    "SENSOR PRESSAO ARLA": [
        "sensor-eletronico-de-pressao-65",
        "sensor-eletronico-de-pressao-73"
    ],

    "INTERRUPTOR PRESSAO OLEO": [
        "interruptor-de-pressao-de-oleo-117",
        "sensor-mecanico-de-pressao-22",
        "interruptor-de-pressao-de-oleo-113",
        "sensor-eletronico-de-pressao-67"
        ],
    
    "SENSOR PRESSAO OLEO MOTOR": [
        "sensor-mecanico-de-pressao-22",
        "interruptor-de-pressao-de-oleo-117",
        "interruptor-de-pressao-de-oleo-113",
        "sensor-eletronico-de-pressao-67"
    ],

    "SENSOR TEMPERATURA PRESSAO OLEO": [
        "sensor-eletronico-de-pressao-73",
        "sensor-eletronico-de-pressao-67"
        ],
}



def baixar_imagem_3rho(categoria: str, codigo: str) -> bool:
    link_base = 'https://www.3rho.com.br/pt-br/produtos-detalhes/'
    link = f'{link_base}{categoria}/{codigo}'
    print(f'---> Link: {link}')

    try:
        with sync_playwright() as p:
            navegador = p.chromium.launch(headless=True)
            pagina = navegador.new_page()

            pagina.goto(link, timeout=15000, wait_until="domcontentloaded")
            pagina.wait_for_selector("text=Baixar imagem", timeout=10000)

            with pagina.expect_download(timeout=10000) as download_info:
                pagina.click("text=Baixar imagem")

            download = download_info.value

            os.makedirs(r"3rho\images", exist_ok=True)
            download.save_as(rf"3rho\images\3RHO-{codigo}.jpg")

            navegador.close()
            print("---> ✔ Download OK")
            return True

    except TimeoutError:
        print("---> Timeout")
        return False

    except Exception as e:
        print(f"---> Erro: {e}")
        return False




def main():
    local_planilha = r'3rho\plan.xlsx'
    planilha = pd.read_excel(local_planilha)

    erros = []

    qtd_fazer = len(planilha['codigo'])
    finalizado_com_sucesso = 0

    for _, linha in planilha.iterrows():

        codigo = str(linha['codigo']).strip()
        nome = str(linha['nome']).strip().upper()


        print('-' * 120)
        print(f'\n---> Produto: {nome} | Código: {codigo}')

        categorias = configuracoes.get(nome)

        if not categorias:
            print("---> Produto não mapeado no dicionário")
            erros.append(codigo)
            continue

        sucesso = False

        for categoria in categorias:
            sucesso = baixar_imagem_3rho(categoria, codigo)
            if sucesso:
                finalizado_com_sucesso+=1
                print(f'Feito com sucesso: {finalizado_com_sucesso}/{qtd_fazer}\n')
                break

        if not sucesso:
            print("---> Nenhuma tentativa funcionou")
            erros.append(codigo)
            

    print("\nFinalizado")
    print(f"Erros ({len(erros)}): {erros}")



main()
