#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests
import time
import os
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
from sys import stderr

# ================ HANYA MERAH & PUTIH ================
R = '\033[91m'      # Merah
W = '\033[97m'      # Putih
B = '\033[1;91m'    # Merah Bold
N = '\033[0m'       # Reset

# ================ ASCII ART DARI ANDA ================
ASCII_ART = f"""
{R}⠀⠀⠀⠀⣀⣀⣀⣀⣀⣀⣀⣀⣀⡀⢀⡀⢀⣀⣀⣀⣀⣀⣀⣀⣀⣀⠀⠀⠀⠀
{R}⠀⠀⠀⠀⣿⠉⣉⣉⣉⣉⣉⣉⣉⣁⣈⣁⣈⣉⣉⣉⣉⣉⣉⣉⠉⣿⠀⠀⠀⠀
{R}⠀⠀⠀⠀⣿⠀{W}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{R}⠀⣿⠀⠀⠀⠀
{R}⠀⠀⠀⠀⣿⠀{W}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{R}⠀⣿⠀⠀⠀⠀
{R}⠀⠀⠀⠀⣿⠀{W}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{R}⠀⣿⠀⠀⠀⠀
{R}⠀⠀⠀⠀⣿⠀{W}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{R}⠀⣿⠀⠀⠀⠀
{R}⠀⠀⠀⠀⣿⣀⣉⣉⣉⣉⣉⣉⣉⣉⣉⣉⣉⣉⣉⣉⣉⣉⣉⣉⣀⣿⠀⠀⠀⠀
{R}⠀⠀⠀⠀⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠀⠀⠀⠀
{R}⠀⠀⠀⠀⣶⡖⠀⠶⠖⠀⠶⠆⠐⠶⠆⠰⠶⠂⠰⠶⠀⠲⠶⠀⢲⣶⠀⠀⠀⠀
{R}⠀⠀⠀⢰⣿⠃⠐⠒⠂⠐⠒⠀⠒⠒⠂⠐⠒⠒⠀⠒⠂⠐⠒⠂⠘⣿⡆⠀⠀⠀
{R}⠀⠀⠀⣾⡿⠀⠛⠛⠀⠚⠛⠀⠚⠛⠃⠘⠛⠓⠀⠛⠓⠀⠛⠛⠀⢿⣷⠀⠀⠀
{R}⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⡏{W}⢸⣿⣿⣿⣿⣿⣿⡇{R}⢸⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀
{R}⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⠀{W}⠙⠛⠛⠛⠛⠛⠛⠋{R}⠀⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀
{R}⠀⠀⣉⣉⣉⣉⣉⣉⣉⣉⣉⣉⣉⣉⣉⣉⣉⣉⣉⣉⣉⣉⣉⣉⣉⣉⣉⣉⠀⠀
{R}⠀⠈⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠁⠀
{N}"""

# ================ BANNER TOOLS ================
BANNER = f"""
{R}╔═══════════════════════════════════════════════════════════════╗
{R}║{W}                                                               {R}║
{R}║{W}    ██████╗██████╗  ██████╗ ██╗    ██╗███╗   ███╗██████╗  {R}║
{R}║{W}   ██╔════╝██╔══██╗██╔══██╗██║    ██║████╗ ████║██╔══██╗ {R}║
{R}║{W}   ██║     ██████╔╝██║  ██║██║ █╗ ██║██╔████╔██║██████╔╝ {R}║
{R}║{W}   ██║     ██╔══██╗██║  ██║██║███╗██║██║╚██╔╝██║██╔══██╗ {R}║
{R}║{W}   ╚██████╗██║  ██║██████╔╝╚███╔███╔╝██║ ╚═╝ ██║██║  ██║ {R}║
{R}║{W}    ╚═════╝╚═╝  ╚═╝╚═════╝  ╚══╝╚══╝ ╚═╝     ╚═╝╚═╝  ╚═╝ {R}║
{R}║{W}                                                               {R}║
{R}║{W}        C R O W M A S T E R   P H O N E                      {R}║
{R}║{W}     ═══ Cek Phone Number Tracker ═══                        {R}║
{R}║{W}                                                               {R}║
{R}╠═══════════════════════════════════════════════════════════════╣
{R}║{W}  Author  : HUNXBYTS                                         {R}║
{R}║{W}  Tool    : CrowMaster Phone - Phone Tracker                 {R}║
{R}║{W}  Warna   : {R}MERAH {W}& {R}PUTIH                                 {R}║
{R}╚═══════════════════════════════════════════════════════════════╝
{N}"""

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def run_banner():
    clear()
    print(ASCII_ART)
    print(BANNER)
    print(f"{R}╰── {W}═══════════════════════════════════════════════════════ {R}───╮{N}")
    print(f"{R}⧽{W}    Selamat datang di CrowMaster Phone Tracker!          {R}⧽{N}")
    print(f"{R}╰┈➤ {W} Tools ini dibuat untuk keperluan edukasi!           {R}┈➤{N}")
    print(f"{R}╰── {W}═══════════════════════════════════════════════════════ {R}───╯{N}")

def phone_tracker():
    """Fungsi utama untuk melacak nomor telepon"""
    run_banner()
    
    print(f"\n{R}╔═══════════════════════════════════════════════════════════════╗{N}")
    print(f"{R}║{W}            📱 PHONE NUMBER TRACKER 📱                      {R}║{N}")
    print(f"{R}╚═══════════════════════════════════════════════════════════════╝{N}")
    
    while True:
        print(f"\n{R}╰── {W}Masukkan nomor telepon target {R}⧽{W} [Contoh: +6281xxxxxxxxx]")
        user_phone = input(f"{R}╰┈➤ {W}Nomor : {R}").strip()
        
        if not user_phone:
            print(f"\n{R}╔═══════════════════════════════════════════════════════════════╗{N}")
            print(f"{R}║{W}  ⚠️  {R}Nomor tidak boleh kosong! Silahkan coba lagi.       {R}║{N}")
            print(f"{R}╚═══════════════════════════════════════════════════════════════╝{N}")
            continue
        break
    
    print(f"\n{R}╔═══════════════════════════════════════════════════════════════╗{N}")
    print(f"{R}║{W}            🔍 HASIL PELACAKAN NOMOR 🔍                      {R}║{N}")
    print(f"{R}╚═══════════════════════════════════════════════════════════════╝{N}")
    
    try:
        default_region = "ID"
        parsed_number = phonenumbers.parse(user_phone, default_region)
        
        # Kumpulkan informasi
        info = {
            "Nomor Asli": parsed_number.national_number,
            "Kode Negara": f"+{parsed_number.country_code}",
            "Lokasi": geocoder.description_for_number(parsed_number, "id"),
            "Kode Region": phonenumbers.region_code_for_number(parsed_number),
            "Operator": carrier.name_for_number(parsed_number, "en") or "Tidak diketahui",
            "Valid": "Ya" if phonenumbers.is_valid_number(parsed_number) else "Tidak",
            "Possible": "Ya" if phonenumbers.is_possible_number(parsed_number) else "Tidak",
            "Format International": phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
            "Format E.164": phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164),
            "Format Mobile": phonenumbers.format_number_for_mobile_dialing(parsed_number, default_region, with_formatting=True),
            "Timezone": ', '.join(timezone.time_zones_for_number(parsed_number)) or "Tidak diketahui",
        }
        
        # Tipe nomor
        number_type = phonenumbers.number_type(parsed_number)
        if number_type == phonenumbers.PhoneNumberType.MOBILE:
            info["Tipe"] = "📱 Mobile / Seluler"
        elif number_type == phonenumbers.PhoneNumberType.FIXED_LINE:
            info["Tipe"] = "☎️ Fixed Line / Telepon Rumah"
        elif number_type == phonenumbers.PhoneNumberType.VOIP:
            info["Tipe"] = "🌐 VoIP"
        else:
            info["Tipe"] = "📞 Lainnya"
        
        # Tampilkan hasil dengan format merah putih
        print(f"\n{R}╰── {W}═══════════ INFORMASI NOMOR ═══════════ {R}───╮{N}")
        
        for key, value in info.items():
            print(f"{R}╰┈➤ {W}{key:<20} {R}: {W}{value}{N}")
        
        print(f"{R}╰── {W}═══════════════════════════════════════ {R}───╯{N}")
        
    except phonenumbers.NumberParseException:
        print(f"\n{R}╔═══════════════════════════════════════════════════════════════╗{N}")
        print(f"{R}║{W}  ❌ {R}Error: Nomor tidak valid! {W}Silahkan coba lagi.      {R}║{N}")
        print(f"{R}║{W}  📝 {R}Pastikan format nomor benar (contoh: +6281xxxxxxxxx){R}║{N}")
        print(f"{R}╚═══════════════════════════════════════════════════════════════╝{N}")
    
    except Exception as e:
        print(f"\n{R}╔═══════════════════════════════════════════════════════════════╗{N}")
        print(f"{R}║{W}  ❌ {R}Terjadi kesalahan: {W}{str(e)}                        {R}║{N}")
        print(f"{R}╚═══════════════════════════════════════════════════════════════╝{N}")

def menu():
    """Menu utama tools"""
    run_banner()
    
    print(f"\n{R}╔═══════════════════════════════════════════════════════════════╗{N}")
    print(f"{R}║{W}                    📋 MENU UTAMA 📋                         {R}║{N}")
    print(f"{R}╠═══════════════════════════════════════════════════════════════╣{N}")
    print(f"{R}║{W}  {R}1. {W}Phone Number Tracker     {R}│{W}   📱 Cek Nomor HP      {R}║{N}")
    print(f"{R}║{W}  {R}2. {W}IP Address Tracker       {R}│{W}   🌐 Lacak IP         {R}║{N}")
    print(f"{R}║{W}  {R}3. {W}Username Tracker         {R}│{W}   👤 Cari Username    {R}║{N}")
    print(f"{R}║{W}  {R}4. {W}Show My IP              {R}│{W}   🖥️  Lihat IP Saya    {R}║{N}")
    print(f"{R}║{W}  {R}0. {W}Exit                    {R}│{W}   🚪 Keluar            {R}║{N}")
    print(f"{R}╚═══════════════════════════════════════════════════════════════╝{N}")

def ip_tracker():
    """Fungsi IP Tracker"""
    run_banner()
    
    print(f"\n{R}╔═══════════════════════════════════════════════════════════════╗{N}")
    print(f"{R}║{W}              🌐 IP ADDRESS TRACKER 🌐                      {R}║{N}")
    print(f"{R}╚═══════════════════════════════════════════════════════════════╝{N}")
    
    ip = input(f"\n{R}╰┈➤ {W}Masukkan IP Target : {R}").strip()
    
    if not ip:
        print(f"\n{R}╔═══════════════════════════════════════════════════════════════╗{N}")
        print(f"{R}║{W}  ⚠️  {R}IP tidak boleh kosong!                               {R}║{N}")
        print(f"{R}╚═══════════════════════════════════════════════════════════════╝{N}")
        return
    
    try:
        req_api = requests.get(f"http://ipwho.is/{ip}", timeout=10)
        ip_data = json.loads(req_api.text)
        
        print(f"\n{R}╰── {W}═══════════ INFORMASI IP ═══════════ {R}───╮{N}")
        
        info_ip = {
            "IP Target": ip,
            "Tipe IP": ip_data.get("type", "Tidak diketahui"),
            "Negara": ip_data.get("country", "Tidak diketahui"),
            "Kode Negara": ip_data.get("country_code", "Tidak diketahui"),
            "Kota": ip_data.get("city", "Tidak diketahui"),
            "Region": ip_data.get("region", "Tidak diketahui"),
            "Latitude": ip_data.get("latitude", "Tidak diketahui"),
            "Longitude": ip_data.get("longitude", "Tidak diketahui"),
            "ISP": ip_data.get("connection", {}).get("isp", "Tidak diketahui"),
            "Organisasi": ip_data.get("connection", {}).get("org", "Tidak diketahui"),
        }
        
        for key, value in info_ip.items():
            print(f"{R}╰┈➤ {W}{key:<15} {R}: {W}{value}{N}")
        
        if ip_data.get("latitude") and ip_data.get("longitude"):
            lat = ip_data["latitude"]
            lon = ip_data["longitude"]
            print(f"{R}╰┈➤ {W}Maps Link       {R}: {W}https://www.google.com/maps/@{lat},{lon},12z{N}")
        
        print(f"{R}╰── {W}═══════════════════════════════════════ {R}───╯{N}")
        
    except requests.exceptions.RequestException:
        print(f"\n{R}╔═══════════════════════════════════════════════════════════════╗{N}")
        print(f"{R}║{W}  ❌ {R}Gagal terhubung ke API! Cek koneksi internet.       {R}║{N}")
        print(f"{R}╚═══════════════════════════════════════════════════════════════╝{N}")
    except Exception as e:
        print(f"\n{R}╔═══════════════════════════════════════════════════════════════╗{N}")
        print(f"{R}║{W}  ❌ {R}Error: {W}{str(e)}                                    {R}║{N}")
        print(f"{R}╚═══════════════════════════════════════════════════════════════╝{N}")

def show_my_ip():
    """Menampilkan IP sendiri"""
    run_banner()
    
    try:
        response = requests.get('https://api.ipify.org/', timeout=10)
        my_ip = response.text
        
        print(f"\n{R}╔═══════════════════════════════════════════════════════════════╗{N}")
        print(f"{R}║{W}              🖥️  YOUR IP ADDRESS 🖥️                        {R}║{N}")
        print(f"{R}╚═══════════════════════════════════════════════════════════════╝{N}")
        print(f"\n{R}╰┈➤ {W}IP Address Anda : {R}{my_ip}{N}")
        
    except Exception as e:
        print(f"\n{R}╔═══════════════════════════════════════════════════════════════╗{N}")
        print(f"{R}║{W}  ❌ {R}Error: {W}{str(e)}                                    {R}║{N}")
        print(f"{R}╚═══════════════════════════════════════════════════════════════╝{N}")

def username_tracker():
    """Fungsi Username Tracker"""
    run_banner()
    
    print(f"\n{R}╔═══════════════════════════════════════════════════════════════╗{N}")
    print(f"{R}║{W}              👤 USERNAME TRACKER 👤                         {R}║{N}")
    print(f"{R}╚═══════════════════════════════════════════════════════════════╝{N}")
    
    username = input(f"\n{R}╰┈➤ {W}Masukkan Username : {R}").strip()
    
    if not username:
        print(f"\n{R}╔═══════════════════════════════════════════════════════════════╗{N}")
        print(f"{R}║{W}  ⚠️  {R}Username tidak boleh kosong!                        {R}║{N}")
        print(f"{R}╚═══════════════════════════════════════════════════════════════╝{N}")
        return
    
    social_media = [
        {"url": "https://www.facebook.com/{}", "name": "Facebook"},
        {"url": "https://www.twitter.com/{}", "name": "Twitter"},
        {"url": "https://www.instagram.com/{}", "name": "Instagram"},
        {"url": "https://www.linkedin.com/in/{}", "name": "LinkedIn"},
        {"url": "https://www.github.com/{}", "name": "GitHub"},
        {"url": "https://www.tiktok.com/@{}", "name": "TikTok"},
        {"url": "https://www.youtube.com/{}", "name": "YouTube"},
        {"url": "https://www.snapchat.com/add/{}", "name": "Snapchat"},
        {"url": "https://www.pinterest.com/{}", "name": "Pinterest"},
        {"url": "https://www.tumblr.com/{}", "name": "Tumblr"},
        {"url": "https://soundcloud.com/{}", "name": "SoundCloud"},
        {"url": "https://www.twitch.tv/{}", "name": "Twitch"},
        {"url": "https://www.telegram.me/{}", "name": "Telegram"},
        {"url": "https://www.medium.com/@{}", "name": "Medium"},
        {"url": "https://www.quora.com/profile/{}", "name": "Quora"},
    ]
    
    print(f"\n{R}╰── {W}═══════ PENCARIAN USERNAME ═══════ {R}───╮{N}")
    print(f"{R}║{W}  🔍 Mencari username di berbagai platform...{R}║{N}")
    print(f"{R}╰── {W}═══════════════════════════════════════ {R}───╯{N}")
    
    found = False
    for site in social_media:
        url = site['url'].format(username)
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"{R}╰┈➤ {W}{site['name']:<12} {R}: {W}✅ Ditemukan -> {R}{url}{N}")
                found = True
            else:
                print(f"{R}╰┈➤ {W}{site['name']:<12} {R}: {W}❌ Tidak ditemukan{N}")
        except:
            print(f"{R}╰┈➤ {W}{site['name']:<12} {R}: {W}⚠️  Error koneksi{N}")
    
    if not found:
        print(f"\n{R}╔═══════════════════════════════════════════════════════════════╗{N}")
        print(f"{R}║{W}  ❌ {R}Username '{W}{username}{R}' tidak ditemukan di platform manapun.{R}║{N}")
        print(f"{R}╚═══════════════════════════════════════════════════════════════╝{N}")

def main():
    """Fungsi utama"""
    while True:
        menu()
        
        try:
            pilihan = input(f"\n{R}╰┈➤ {W}Pilih menu (0-4) : {R}")
            
            if pilihan == '0':
                print(f"\n{R}╔═══════════════════════════════════════════════════════════════╗{N}")
                print(f"{R}║{W}  👋 Terima kasih telah menggunakan CrowMaster Phone!       {R}║{N}")
                print(f"{R}║{W}  {R}© {W}Created by HUNXBYTS - {R}Merah Putih Forever!      {R}║{N}")
                print(f"{R}╚═══════════════════════════════════════════════════════════════╝{N}")
                break
                
            elif pilihan == '1':
                phone_tracker()
                input(f"\n{R}╰┈➤ {W}Tekan Enter untuk kembali ke menu...")
                
            elif pilihan == '2':
                ip_tracker()
                input(f"\n{R}╰┈➤ {W}Tekan Enter untuk kembali ke menu...")
                
            elif pilihan == '3':
                username_tracker()
                input(f"\n{R}╰┈➤ {W}Tekan Enter untuk kembali ke menu...")
                
            elif pilihan == '4':
                show_my_ip()
                input(f"\n{R}╰┈➤ {W}Tekan Enter untuk kembali ke menu...")
                
            else:
                print(f"\n{R}╔═══════════════════════════════════════════════════════════════╗{N}")
                print(f"{R}║{W}  ⚠️  {R}Pilihan tidak valid! Silahkan pilih 0-4.             {R}║{N}")
                print(f"{R}╚═══════════════════════════════════════════════════════════════╝{N}")
                time.sleep(1)
                
        except KeyboardInterrupt:
            print(f"\n\n{R}╔═══════════════════════════════════════════════════════════════╗{N}")
            print(f"{R}║{W}  ⚠️  {R}Keluar dari program...                               {R}║{N}")
            print(f"{R}╚═══════════════════════════════════════════════════════════════╝{N}")
            break
        except Exception as e:
            print(f"\n{R}╔═══════════════════════════════════════════════════════════════╗{N}")
            print(f"{R}║{W}  ❌ {R}Error tak terduga: {W}{str(e)}                         {R}║{N}")
            print(f"{R}╚═══════════════════════════════════════════════════════════════╝{N}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{R}╔═══════════════════════════════════════════════════════════════╗{N}")
        print(f"{R}║{W}  👋 Sampai jumpa! {R}Merah Putih!                          {R}║{N}")
        print(f"{R}╚═══════════════════════════════════════════════════════════════╝{N}")�{N}")
```