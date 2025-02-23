import os
import time
import requests
import ipaddress
import socket
import phonenumbers
from phonenumbers import geocoder, carrier, timezone

BLUE = '\033[94m'
GREEN = '\033[32m'
RED = '\033[91m'
WHITE = '\033[97m'
CYAN = '\033[36m'
ORANGE = '\033[93m'
END = '\033[0m'

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

HEADER = f"""
{CYAN}Made by{END} {ORANGE}VOJXX{END} {RED}|{END} {CYAN}Version :{END}{ORANGE} 1.1V{END} {RED}|{END}
"""

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_ascii_art():
    print(f"{RED}{ART}{END}")
    print(f"{HEADER}\n")

def is_home_network(ip):
    try:
        ip_obj = ipaddress.ip_address(ip)
        return ip_obj.is_private
    except ValueError:
        return False  

def scan_ssh_port(ip, port=22, timeout=2):
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            return True
    except (socket.timeout, ConnectionRefusedError):
        return False
    except Exception:
        return "Unbekannt"

def get_host_name(ip):

    try:
        host_name = socket.gethostbyaddr(ip)[0]
        return host_name
    except (socket.herror, socket.gaierror):
        return "N/A" 

def get_ip_info(ip):
    url = f"http://ip-api.com/json/{ip}?fields=66846719"
    response = requests.get(url, timeout=5)
    
    if response.status_code == 200:
        data = response.json()
        if data.get("status") == "success":
            lat = data.get("lat", "N/A")
            lon = data.get("lon", "N/A")
            
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
                "Hostname": host_name 
            }
        else:
            return {"Fehler": "Ungültige IP-Adresse oder keine Daten verfügbar."}
    else:
        return {"Fehler": f"HTTP-Statuscode {response.status_code}"}

def get_phone_info(phone_number):
    try:
        parsed_number = phonenumbers.parse(phone_number)
        country = geocoder.country_name_for_number(parsed_number, "en")
        phone_carrier = carrier.name_for_number(parsed_number, "en")

        is_valid = phonenumbers.is_valid_number(parsed_number)
        number_type = phonenumbers.number_type(parsed_number)

        time_zone = timezone.time_zones_for_number(parsed_number)

        formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)

        number_type_str = ""
        if number_type == 1:
            number_type_str = "Festnetznummer"
        elif number_type == 2:
            number_type_str = "Mobilnummer"
        elif number_type == 3:
            number_type_str = "VoIP-Nummer"
        elif number_type == 4:
            number_type_str = "Kurzwahl"
        elif number_type == 5:
            number_type_str = "Premium-Dienstnummer"
        else:
            number_type_str = "Unbekannter Typ"

        return {
            "Number": formatted_number,
            "Country": country,
            "Timezone": ", ".join(time_zone) if time_zone else "N/A",
            "Region": geocoder.description_for_number(parsed_number, "de"),
            "Number Type": number_type_str,
            "ISP": phone_carrier if phone_carrier else "N/A",
            "Validation": "Valid" if is_valid else "Invalid"
        }
    except phonenumbers.phonenumberutil.NumberParseException:
        return {"Error": "Ungültige Telefonnummer"}
        
def show_menu():
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
    phone_number = input(f"{GREEN}[+]{END}{CYAN} Enter full number : {END}").strip()
    
    if phone_number:
        info = get_phone_info(phone_number)
        
        print(f"\n{GREEN}[+] Information for : {CYAN}{phone_number}{END}\n")
        for key, value in info.items():
            print(f"[ {ORANGE}{key}{END} {WHITE}: {CYAN}{value}{END} ]")
    else:
        print(f"{RED}[!] Keine gültige Telefonnummer eingegeben!{END}")
        time.sleep(2)
        show_menu()
    
    print()
    print()
    input(f"{GREEN}[>] {CYAN}Drücke Enter, um zurückzukehren...{END}")
    clear_screen()
    show_menu()

def trace_ip():
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
        if key != "Google Maps":  
            print(f"[ {ORANGE}{key}{END} {WHITE}: {CYAN}{value}{END} ]")
    
    print(f"[ {ORANGE}SSH{END} {WHITE}: {CYAN}{info.get('SSH', 'N/A')}{END} ]\n")
    
    print("\n")
    input(f"{GREEN}[>] {CYAN}Drücke Enter, um zurückzukehren...{END}")
    clear_screen()
    show_menu()

if __name__ == "__main__":
    show_menu()
