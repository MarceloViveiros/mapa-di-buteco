import json
import time
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="roteiro_buteco_jf_eudev")

print("Lendo a base de dados com as informações profundas do prato...")

# 1. MUDANÇA CRÍTICA AQUI: Lendo o arquivo certo!
with open("bares_completos_v2.json", "r", encoding="utf-8") as arquivo:
    bares = json.load(arquivo)

for bar in bares:
    endereco_original = bar.get("endereco", "")
    
    # Previne erros caso o bar venha sem endereço
    if endereco_original and endereco_original != "Não informado":
        endereco_limpo = endereco_original.replace(" | ", ", ")
        print(f"📍 Buscando: {bar['nome']}...")
        
        try:
            localizacao = geolocator.geocode(endereco_limpo)
            if localizacao:
                bar["latitude"] = localizacao.latitude
                bar["longitude"] = localizacao.longitude
                print(f"   ✅ OK")
            else:
                bar["latitude"] = None
                bar["longitude"] = None
                print("   ❌ Não achou automático")
        except Exception as e:
             print("   ⚠️ Erro de rede")
        
        time.sleep(1.5) # Respeitando o satélite
    else:
        bar["latitude"] = None
        bar["longitude"] = None

# 2. SALVANDO O ARQUIVO DEFINITIVO
print("\nSalvando o arquivo bares_finais.json...")
with open("bares_finais.json", "w", encoding="utf-8") as arquivo_novo:
    json.dump(bares, arquivo_novo, ensure_ascii=False, indent=4)

print("Pipeline concluído!")