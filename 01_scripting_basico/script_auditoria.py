import requests
import json
from requests.auth import HTTPBasicAuth

# Deshabilitar advertencias de certificados SSL autofirmados
requests.packages.urllib3.disable_warnings()

# 1. Parámetros de la API RESTCONF
url = "https://sandbox-iosxe-latest-1.cisco.com/restconf/data/ietf-interfaces:interfaces"
headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}
auth = HTTPBasicAuth("developer", "C1sco12345!")
interfaces_activas = []

try:
    # 2. Petición GET HTTP
    response = requests.get(
        url,
        headers=headers,
        auth=auth,
        verify=False  # Ignorar verificación SSL en entorno de lab
    )
    if response.status_code == 200:
        data = response.json()
        interfaces = data["ietf-interfaces:interfaces"]["interface"]
        
        print(f"{'Nombre':<20} {'Tipo':<30} {'Habilitada':<10}")
        print("-" * 60)
        
        for iface in interfaces:
            nombre = iface.get("name", "N/A")
            activa = iface.get("enabled", False)

            if activa:
                datos_ipv4 = iface.get("ietf-ip:ipv4", {})
                lista_ip = datos_ipv4.get("address", [])

                if lista_ip:
                    ip_info = lista_ip[0]
                    interfaces_activas.append({
                        "nombre": nombre,
                        "ip": ip_info.get("ip"),
                        "mascara": ip_info.get("netmask"),
                        "activa": activa
                    })

        with open("inventario_interfaces.json", "w", encoding="utf-8") as archivo:
            json.dump(interfaces_activas, archivo, indent=4)

        print("Archivo creado correctamente.")
    else:
        print(f"Error HTTP {response.status_code}: {response.text}")

except requests.exceptions.RequestException as e:
    print(f"Error de conexión: {e}")
    with open("inventario_interfaces.json", "w", encoding="utf-8") as archivo:
                json.dump(interfaces_activas, archivo, indent=4)
                print("Archivo creado correctamente.")