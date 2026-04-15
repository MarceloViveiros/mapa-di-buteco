import cloudscraper
from bs4 import BeautifulSoup
import json
import time

print("Iniciando o Deep Scraper para o 'Eu Dev!'...")
print("Paciência: O robô vai entrar em 40 páginas. Isso levará alguns minutos.\n")

scraper = cloudscraper.create_scraper()
todos_os_bares = []

# 1. LOOP DA VITRINE: Passa pelas 4 páginas principais
for numero_pagina in range(1, 5):
    print(f"--- Varrendo Página {numero_pagina} da Vitrine ---")
    
    if numero_pagina == 1:
         url = "https://comidadibuteco.com.br/butecos/juiz-de-fora/"
    else:
         url = f"https://comidadibuteco.com.br/butecos/juiz-de-fora/page/{numero_pagina}/" 

    resposta = scraper.get(url)

    if resposta.status_code == 200:
        soup = BeautifulSoup(resposta.text, 'html.parser')
        cards_dos_bares = soup.find_all('div', class_="col-12 col-md-4 col-lg-3 mb-4")
        
        for card in cards_dos_bares:
            try:
                # ---------------------------------------------------------
                # PARTE A: DADOS DA VITRINE
                # ---------------------------------------------------------
                nome_h2 = card.find('h2')
                nome = nome_h2.text.strip() if nome_h2 else "Sem Nome"
                
                div_imagem = card.find('div', class_='image')
                tag_img = div_imagem.find('img') if div_imagem else None
                imagem_url = tag_img['src'] if tag_img else "Sem Imagem"
                
                div_botoes = card.find('div', class_='d-flex justify-content-between')
                tag_detalhes = div_botoes.find('a', string='Detalhes') if div_botoes else None
                link_detalhes = tag_detalhes['href'] if tag_detalhes else None

                # Variáveis vazias preparadas para receber os dados profundos
                nome_prato = "Não informado"
                descricao_prato = "Não informada"
                telefone = "Não informado"
                horario = "Não informado"
                endereco = "Não informado"

                # ---------------------------------------------------------
                # PARTE B: DEEP SCRAPING (ENTRANDO NA PÁGINA DO BAR)
                # ---------------------------------------------------------
                if link_detalhes:
                    print(f"  Entrando no bar: {nome}...")
                    time.sleep(2) # Pausa de 2 segundos para o segurança não desconfiar
                    
                    resp_interno = scraper.get(link_detalhes)
                    
                    if resp_interno.status_code == 200:
                        soup_interno = BeautifulSoup(resp_interno.text, 'html.parser')
                        div_texto = soup_interno.find('div', class_='section-text')
                        
                        if div_texto:
                            paragrafos = div_texto.find_all('p')
                            
                            # 1. O Prato (Geralmente o primeiro parágrafo)
                            if len(paragrafos) > 0:
                                tag_b_prato = paragrafos[0].find('b')
                                if tag_b_prato:
                                    nome_prato = tag_b_prato.text.strip()
                                    # Pega o texto inteiro e tira o nome do prato, sobrando a descrição
                                    descricao_prato = paragrafos[0].text.replace(nome_prato, '').strip()
                            
                            # 2. Varrendo os outros parágrafos com nossa lógica Ninja
                            for p in paragrafos:
                                texto_p = p.text
                                
                                if 'Telefone:' in texto_p:
                                    telefone = texto_p.replace('Telefone:', '').strip()
                                    
                                elif 'Horario:' in texto_p:
                                    horario = texto_p.replace('Horario:', '').strip()
                                    
                                elif 'Endereço:' in texto_p:
                                    endereco = texto_p.replace('Endereço:', '').strip()

                # ---------------------------------------------------------
                # PARTE C: SALVANDO O BAR NO NOSSO BANCO
                # ---------------------------------------------------------
                todos_os_bares.append({
                    "nome": nome,
                    "imagem": imagem_url,
                    "link_detalhes": link_detalhes,
                    "endereco": endereco,
                    "prato": nome_prato,
                    "descricao_prato": descricao_prato,
                    "telefone": telefone,
                    "horario": horario
                })
                
            except Exception as e:
                print(f"Erro ao processar o card do bar {nome}: {e}")

    else:
        print(f"Falha na página {numero_pagina}. Código: {resposta.status_code}")
    
    time.sleep(3) # Pausa maior ao mudar de página da vitrine

# ---------------------------------------------------------
# FASE FINAL: EXPORTANDO O JSON
# ---------------------------------------------------------
print("\nSalvando arquivo bares_completos_v2.json...")
with open("bares_completos_v2.json", "w", encoding="utf-8") as arquivo_json:
    json.dump(todos_os_bares, arquivo_json, ensure_ascii=False, indent=4)

print(f"✅ Sucesso Absoluto! {len(todos_os_bares)} bares extraídos com dados profundos.")