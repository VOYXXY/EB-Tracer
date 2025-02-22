import os
import time
import requests
import ipaddress
import socket
import phonenumbers
from phonenumbers import geocoder, carrier, timezone

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
/        |/       \ 
$$$$$$$$/ $$$$$$$  |
$$ |__    $$ |__$$ |
$$    |   $$    $$< 
$$$$$/    $$$$$$$  |
$$ |_____ $$ |__$$ |
$$       |$$    $$/ 
$$$$$$$$/ $$$$$$$/
"""

# Custom Header für "Made by VOJXX | Version : 1.1V"
HEADER = f"""
{CYAN}Made by{END} {ORANGE}VOJXX{END} {RED}|{END} {CYAN}Version :{END}{ORANGE} 1.1V{END} {RED}|{END}
"""

def clear_screen():
    """ Leert den Bildschirm """
    os.system('cls' if os.name == 'nt' else 'clear')

def print_ascii_art():
    """ Zeigt die ASCII-Art in Rot an """
    print(f"{RED}{ART}{END}")
    print(f"{HEADER}\n")

def is_home_network(ip):
    """ Überprüft, ob die IP zu einem Heimnetzwerk gehört """
    try:
        ip_obj = ipaddress.ip_address(ip)
        return ip_obj.is_private
    except ValueError:
        return False  # Ungültige IP

def scan_ssh_port(ip, port=22, timeout=2):
    """ Prüft, ob der SSH-Port (22) offen ist """
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            return True
    except (socket.timeout, ConnectionRefusedError):
        return False
    except Exception:
        return "Unbekannt"

def get_host_name(ip):
    """ Holt den Hostnamen einer IP-Adresse """
    try:
        host_name = socket.gethostbyaddr(ip)[0]
        return host_name
    except (socket.herror, socket.gaierror):
        return "N/A"  # Wenn keine DNS-Auflösung möglich ist

def get_ip_info(ip):
    """ Holt Infos zu einer IP """
    url = f"http://ip-api.com/json/{ip}?fields=66846719"
    response = requests.get(url, timeout=5)
    
    if response.status_code == 200:
        data = response.json()
        if data.get("status") == "success":
            lat = data.get("lat", "N/A")
            lon = data.get("lon", "N/A")
            
            # Hostname hinzufügen
            host_name = get_host_name(ip)
            
            return {
                "IP": data.get("query", "N/A"),
                "Home Network": "Ja" if is_home_network(ip) else "Nein",
                "Continent": data.get("continent", "N/A"),
                "Continent Code": data.get("continentCode", "N/A"),
                "Country": data.get("country", "N/A"),
                "Country Code": data.get("countryCode", "N/A"),
                "Region": data.get("regionName", "N/A"),
                "City": data.get("city", "N/A"),
                "District": data.get("district", "N/A"),
                "Zip": data.get("zip", "N/A"),
                "Latitude": lat,
                "Longitude": lon,
                "Timezone": data.get("timezone", "N/A"),
                "Currency": data.get("currency", "N/A"),
                "ISP": data.get("isp", "N/A"),
                "Organization": data.get("org", "N/A"),
                "AS": data.get("as", "N/A"),
                "Reverse DNS": data.get("reverse", "N/A"),
                "Mobile": "Ja" if data.get("mobile", False) else "Nein",
                "Proxy": "Ja" if data.get("proxy", False) else "Nein",
                "Hosting": "Ja" if data.get("hosting", False) else "Nein",
                "SSH": "True" if scan_ssh_port(ip) else "False",
                "Hostname": host_name  # Der Hostname wird jetzt auch angezeigt
            }
        else:
            return {"Fehler": "Ungültige IP-Adresse oder keine Daten verfügbar."}
    else:
        return {"Fehler": f"HTTP-Statuscode {response.status_code}"}

def get_phone_info(phone_number):
    """ Holt Informationen zu einer Telefonnummer """
    try:
        parsed_number = phonenumbers.parse(phone_number)

        # Land
        country = geocoder.country_name_for_number(parsed_number, "de")

        # Anbieter
        phone_carrier = carrier.name_for_number(parsed_number, "de")

        # Gültigkeit und Nummerntyp
        is_valid = phonenumbers.is_valid_number(parsed_number)
        number_type = phonenumbers.number_type(parsed_number)

        # Zeitzone
        time_zone = timezone.time_zones_for_number(parsed_number)

        # Formatierte Nummer
        formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)

        return {
            "Number": formatted_number,
            "Country": country,
            "Timezone": ", ".join(time_zone) if time_zone else "N/A",
            "Region": geocoder.description_for_number(parsed_number, "de"),
            "Number Type": phonenumbers.number_type(parsed_number),
            "ISP": phone_carrier if phone_carrier else "N/A",
            "Validation": "Valid" if is_valid else "Invalid"
        }
    except phonenumbers.phonenumberutil.NumberParseException:
        return {"Error": "Ungültige Telefonnummer"}

def show_menu():
    """ Zeigt das Hauptmenü an """
    clear_screen()
    print_ascii_art()
    print(f"{ORANGE}[!] Wähle eine Option:{END}")
    print()
    print(f"{RED}[{END}{ORANGE}1{END}{RED}]{END} {CYAN}Trace IP{END}")                    
    print(f"{RED}[{END}{ORANGE}2{END}{RED}]{END} {CYAN}Trace my IP{END}")    
    print(f"{RED}[{END}{ORANGE}3{END}{RED}]{END} {CYAN}Attack Host {END}")
    print(f"{RED}[{END}{ORANGE}4{END}{RED}]{END} {CYAN}Phone Number Info{END}")
    print()
    
    choice = input(f"{RED}[{END} EB-Tracer {RED}]{END} >> ").strip()
    
    if choice == "1":
        trace_ip()
    elif choice == "2":
        trace_my_ip()
    elif choice == "4":
        trace_phone()
    else:
        print(f"{RED}[!] Ungültige Auswahl!{END}")
        time.sleep(2)
        show_menu()

def trace_phone():
    """ Benutzer gibt eine Telefonnummer ein, die überprüft wird """
    clear_screen()
    print_ascii_art()
    phone_number = input(f"{GREEN}[+]{END}{CYAN} Gib eine Telefonnummer ein (mit Ländervorwahl): {END}").strip()
    
    if phone_number:
        info = get_phone_info(phone_number)
        for key, value in info.items():
            if key == "ISP":
                print(f"[ {ORANGE}ISP{END} {WHITE}: {CYAN}{value if value else 'N/A'}{END} ]\n")
            else:
                print(f"[ {ORANGE}{key}{END} {WHITE}: {CYAN}{value}{END} ]")
    else:
        print(f"{RED}[!] Keine gültige Telefonnummer eingegeben!{END}")
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
    print(f"{GREEN}[+] Gib eine IP-Adresse ein: {WHITE}{ip}\n")

    info = get_ip_info(ip)

    for key, value in info.items():
        if key != "Google Maps":  # Google Maps-Link nicht mehr anzeigen
            print(f"[ {ORANGE}{key}{END} {WHITE}: {CYAN}{value}{END} ]")
    
    # SSH-Status vor Google Maps-Link anzeigen
    print(f"[ {ORANGE}SSH{END} {WHITE}: {CYAN}{info.get('SSH', 'N/A')}{END} ]\n")
    
    print("\n")
    input(f"{GREEN}[>] {CYAN}Drücke Enter, um zurückzukehren...{END}")
    clear_screen()
    show_menu()

if __name__ == "__main__":
    show_menu()
