import os
import time
import requests

# Farben definieren
BLUE = '\033[94m'
GREEN = '\033[32m'
RED = '\033[91m'
WHITE = '\033[97m'
CYAN = '\033[36m'
ORANGE = '\033[93m'
END = '\033[0m'

# ASCII-Art
ART = """ 
________  _______
/        |/       \\ 
$$$$$$$$/ $$$$$$$  |
$$ |__    $$ |__$$ |
$$    |   $$    $$<
$$$$$/    $$$$$$$  |
$$ |_____ $$ |__$$ |
$$       |$$    $$/ 
$$$$$$$$/ $$$$$$$/
"""

def clear_screen():
    """ Leert den Bildschirm """
    os.system('cls' if os.name == 'nt' else 'clear')

def print_ascii_art():
    """ Zeigt die ASCII-Art in Rot an """
    print(f"{RED}{ART}{END}")

def get_ip_info(ip):
    """ Holt Infos zu einer IP """
    url = f"http://ip-api.com/json/{ip}?fields=66846719"
    response = requests.get(url, timeout=5)
    
    if response.status_code == 200:
        data = response.json()
        if data.get("status") == "success":
            lat = data.get("lat", "N/A")
            lon = data.get("lon", "N/A")
            google_maps_link = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}" if lat != "N/A" and lon != "N/A" else "N/A"
            
            return {
                "IP": data.get("query", "N/A"),
                "STATUS": data.get("status", "N/A"),
                "KONTINENT": data.get("continent", "N/A"),
                "KONTINENTCODE": data.get("continentCode", "N/A"),
                "LAND": data.get("country", "N/A"),
                "LÄNDERCODE": data.get("countryCode", "N/A"),
                "REGIONCODE": data.get("region", "N/A"),
                "REGION": data.get("regionName", "N/A"),
                "STADT": data.get("city", "N/A"),
                "DISTRIKT": data.get("district", "N/A"),
                "POSTLEITZAHL": data.get("zip", "N/A"),
                "BREITENGRAD": lat,
                "LÄNGENGRAD": lon,
                "ZEITZONE": data.get("timezone", "N/A"),
                "UTC OFFSET": data.get("offset", "N/A"),
                "WÄHRUNG": data.get("currency", "N/A"),
                "ISP": data.get("isp", "N/A"),
                "ORGANISATION": data.get("org", "N/A"),
                "AS": data.get("as", "N/A"),
                "AS NAME": data.get("asname", "N/A"),
                "REVERSE DNS": data.get("reverse", "N/A"),
                "MOBILE": "Ja" if data.get("mobile", False) else "Nein",
                "PROXY": "Ja" if data.get("proxy", False) else "Nein",
                "HOSTING": "Ja" if data.get("hosting", False) else "Nein",
                "GOOGLE MAPS": google_maps_link
            }
        else:
            return {"Fehler": "Ungültige IP-Adresse oder keine Daten verfügbar."}
    else:
        return {"Fehler": f"HTTP-Statuscode {response.status_code}"}

def show_menu():
    """ Zeigt das Hauptmenü an """
    clear_screen()
    print_ascii_art()
    print()
    print(f"{ORANGE}[!] Wähle eine Option:{END}")
    print()
    print(f"{GREEN}[1]{END} {CYAN}Trace eine IP")                    
    print(f"{GREEN}[2]{END} {CYAN}Trace meine eigene IP")                    
    print()
    
    choice = input(f"{GREEN}[>]{END}{CYAN} Auswahl: {END}").strip()
    
    if choice == "1":
        trace_ip()
    elif choice == "2":
        trace_my_ip()
    else:
        print(f"{RED}[!] Ungültige Auswahl!{END}")
        time.sleep(2)
        show_menu()

def trace_ip():
    """ Benutzer gibt eine IP ein, die getraced wird """
    clear_screen()
    print_ascii_art()
    ip = input(f"{GREEN}[+]{END}{CYAN} Gib eine IP-Adresse ein: {END}").strip()
    
    if ip:
        display_ip_info(ip)
    else:
        print(f"{RED}[!] Keine gültige IP eingegeben!{END}")
        time.sleep(2)
        show_menu()

def trace_my_ip():
    """ Holt automatisch die eigene IP und zeigt die Infos an """
    clear_screen()
    print_ascii_art()
    print(f"{GREEN}[+] {CYAN}Hole eigene IP...{END}")
    
    try:
        response = requests.get("https://api64.ipify.org?format=json", timeout=5)
        my_ip = response.json().get("ip", "N/A")
        if my_ip != "N/A":
            display_ip_info(my_ip)
        else:
            print(f"{RED}[!] Konnte eigene IP nicht ermitteln!{END}")
            time.sleep(2)
            show_menu()
    except Exception as e:
        print(f"{RED}[!] Fehler: {e}{END}")
        time.sleep(2)
        show_menu()

def display_ip_info(ip):
    """ Holt und zeigt die IP-Informationen an """
    clear_screen()
    print_ascii_art()
    print(f"{GREEN}IP-Informationen für: {WHITE}{ip}\n")

    info = get_ip_info(ip)

    for key, value in info.items():
        print(f"{ORANGE}{key}: {WHITE}{value}{END}")

    print("\n")
    input(f"{GREEN}[>] {CYAN}Drücke Enter, um zurückzukehren...{END}")
    show_menu()

if __name__ == "__main__":
    show_menu()
