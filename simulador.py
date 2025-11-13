import requests
import time
import random

API_URL_VEICULOS = "http://127.0.0.1:5000/api/veiculos"
API_URL_RASTREADOR = "http://127.0.0.1:5000/api/rastreador"

posicoes_carros = {}

LAT_INICIAL_BASE = -22.2152
LON_INICIAL_BASE = -49.9442
INTERVALO_SEGUNDOS = 10

def atualizar_lista_de_carros():
    try:
        response = requests.get(API_URL_VEICULOS)
        if response.status_code != 200:
            print(f"Erro ao buscar veículos: {response.status_code}")
            return

        veiculos = response.json()
        
        for veiculo in veiculos:
            id_rastreador = veiculo.get('id_rastreador')
            
            if id_rastreador and id_rastreador not in posicoes_carros:
                pos_inicial = {
                    "lat": LAT_INICIAL_BASE + random.uniform(-0.01, 0.01), 
                    "lon": LON_INICIAL_BASE + random.uniform(-0.01, 0.01)
                }
                posicoes_carros[id_rastreador] = pos_inicial
                print(f"Novo carro [ID Rastreador: {id_rastreador}] (Modelo: {veiculo.get('modelo')}) adicionado ao simulador.")
                
    except requests.exceptions.ConnectionError:
        print("Erro: Não foi possível conectar ao servidor (app.py) para buscar veículos.")
        return

print(f"--- Simulador de GPS para TODOS os carros ---")
print("Buscando veículos cadastrados...")
print("Pressione Ctrl+C para parar.")

while True:
    try:
        atualizar_lista_de_carros()

        if not posicoes_carros:
            print(f"Nenhum carro com rastreador encontrado. Verificando novamente em {INTERVALO_SEGUNDOS}s...")
            time.sleep(INTERVALO_SEGUNDOS)
            continue

        print(f"\n--- Atualizando {len(posicoes_carros)} carro(s) ---")
        
        for id_rastreador, pos in list(posicoes_carros.items()):
            
            nova_lat = pos['lat'] + random.uniform(-0.0005, 0.0005)
            nova_lon = pos['lon'] + random.uniform(-0.0005, 0.0005)

            posicoes_carros[id_rastreador]['lat'] = nova_lat
            posicoes_carros[id_rastreador]['lon'] = nova_lon
            
            payload = {
                "id_rastreador": id_rastreador,
                "lat": nova_lat,
                "lon": nova_lon
            }
            
            response = requests.post(API_URL_RASTREADOR, json=payload)
            
            if response.status_code == 201:
                print(f"  [ID: {id_rastreador:03d}] Posição enviada: Lat={nova_lat:.6f}, Lon={nova_lon:.6f}")
            else:
                print(f"  [ID: {id_rastreador:03d}] Erro: {response.status_code} - {response.text}")
        
        print(f"--- Próxima atualização em {INTERVALO_SEGUNDOS} segundos ---")
        time.sleep(INTERVALO_SEGUNDOS)

    except requests.exceptions.ConnectionError:
        print(f"Erro: Conexão com API (POST) falhou. Tentando novamente em {INTERVALO_SEGUNDOS}s...")
        time.sleep(INTERVALO_SEGUNDOS)
    except KeyboardInterrupt:
        print("\nSimulador interrompido.")
        break