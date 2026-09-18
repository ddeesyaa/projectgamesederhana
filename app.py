from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

# Bank Soal Terpusat di Python (Backend)
LEVELS_DATA = [
    {
        "title": "Physical Layer",
        "edu": "Kategori: Media & Perangkat Keras Jaringan.",
        "bank": [
            {"q": "Kabel yang menggunakan serat kaca dan cahaya?", "options": ["UTP", "Fiber Optic", "Coaxial"], "correct": 1},
            {"q": "Konektor standar untuk kabel LAN RJ-45 memiliki berapa pin?", "options": ["4 Pin", "6 Pin", "8 Pin"], "correct": 2},
            {"q": "Alat untuk mengetes kabel LAN?", "options": ["LAN Tester", "Crimping Tool", "Fiber Cleaver"], "correct": 0},
            {"q": "Kabel UTP yang digunakan antar PC langsung?", "options": ["Straight", "Crossover", "Rollover"], "correct": 1},
            {"q": "Lapisan terbawah model OSI?", "options": ["Data Link", "Physical", "Network"], "correct": 1},
            {"q": "Topologi yang menyerupai bintang?", "options": ["Bus", "Star", "Ring"], "correct": 1},
            {"q": "Perangkat yang sekadar meneruskan sinyal listrik tanpa filter?", "options": ["Hub", "Switch", "Router"], "correct": 0},
            {"q": "Urutan warna kabel ke-1 pada T568B?", "options": ["Hijau", "Putih Orange", "Putih Hijau"], "correct": 1}
        ]
    },
    {
        "title": "Data Link Layer",
        "edu": "Kategori: Pengalamatan Fisik & Switching.",
        "bank": [
            {"q": "Alamat fisik unik perangkat keras?", "options": ["IP Address", "MAC Address", "UUID"], "correct": 1},
            {"q": "Switch bekerja di layer mana?", "options": ["Layer 1", "Layer 2", "Layer 3"], "correct": 1},
            {"q": "Protokol untuk mencegah loop di switch?", "options": ["STP", "VLAN", "RIP"], "correct": 0},
            {"q": "Teknologi membagi jaringan secara logis?", "options": ["VPN", "VLAN", "VNC"], "correct": 1},
            {"q": "Protokol memetakan IP ke MAC?", "options": ["DNS", "ARP", "DHCP"], "correct": 1},
            {"q": "Satuan data pada layer Data Link?", "options": ["Bit", "Frame", "Packet"], "correct": 1},
            {"q": "Mode switch yang mengirim data ke satu tujuan?", "options": ["Broadcast", "Multicast", "Unicast"], "correct": 2},
            {"q": "VLAN default biasanya memiliki ID berapa?", "options": ["0", "1", "100"], "correct": 1}
        ]
    },
    {
        "title": "Network Layer",
        "edu": "Kategori: Routing & Logika IP.",
        "bank": [
            {"q": "Protokol yang bertugas merutekan paket?", "options": ["IP", "TCP", "HTTP"], "correct": 0},
            {"q": "IP 192.168.1.1 termasuk kelas?", "options": ["Kelas A", "Kelas B", "Kelas C"], "correct": 2},
            {"q": "Berapa bit panjang IPv4?", "options": ["32 bit", "64 bit", "128 bit"], "correct": 0},
            {"q": "IP loopback lokal standar?", "options": ["127.0.0.1", "10.0.0.1", "192.168.0.1"], "correct": 0},
            {"q": "Perangkat Layer 3 model OSI?", "options": ["Hub", "Switch", "Router"], "correct": 2},
            {"q": "Satuan data pada layer Network?", "options": ["Frame", "Packet", "Segment"], "correct": 1},
            {"q": "Perintah cek koneksi ke IP tujuan?", "options": ["Ipconfig", "Ping", "Traceroute"], "correct": 1},
            {"q": "CIDR /24 memiliki subnet mask?", "options": ["...255.0", "...255.128", "...255.240"], "correct": 0}
        ]
    },
    {
        "title": "Transport & Services",
        "edu": "Kategori: Pengiriman Data & Port.",
        "bank": [
            {"q": "Protokol yang menggunakan 3-way handshake?", "options": ["UDP", "TCP", "ICMP"], "correct": 1},
            {"q": "Port standar untuk layanan Web (HTTP)?", "options": ["21", "80", "443"], "correct": 1},
            {"q": "Layanan mengubah nama domain ke IP?", "options": ["DHCP", "DNS", "FTP"], "correct": 1},
            {"q": "Protokol pengiriman email?", "options": ["SMTP", "POP3", "SNMP"], "correct": 0},
            {"q": "Port untuk layanan remote aman SSH?", "options": ["21", "22", "23"], "correct": 1},
            {"q": "Layanan pemberi IP otomatis?", "options": ["DNS", "DHCP", "NAT"], "correct": 1},
            {"q": "Protokol transfer file?", "options": ["HTTP", "SSH", "FTP"], "correct": 2},
            {"q": "Port untuk HTTPS?", "options": ["80", "443", "8080"], "correct": 1}
        ]
    },
    {
        "title": "Cyber Security",
        "edu": "Kategori: Keamanan & Pertahanan Sistem.",
        "bank": [
            {"q": "Sistem penyaring trafik berbahaya?", "options": ["Firewall", "Repeater", "Modem"], "correct": 0},
            {"q": "Metode tebak password secara paksa?", "options": ["DDoS", "Brute Force", "Spoofing"], "correct": 1},
            {"q": "Enkripsi paling aman untuk Wifi saat ini?", "options": ["WEP", "WPA2", "WPA3"], "correct": 2},
            {"q": "Serangan membanjiri trafik server?", "options": ["Malware", "DDoS", "Phishing"], "correct": 1},
            {"q": "Teknik menyamar menjadi IP orang lain?", "options": ["Sniffing", "Spoofing", "Spamming"], "correct": 1},
            {"q": "Sistem pendeteksi intrusi jaringan?", "options": ["IDS", "VPN", "Proxy"], "correct": 0},
            {"q": "Virus yang mengunci data untuk tebusan?", "options": ["Adware", "Ransomware", "Spyware"], "correct": 1},
            {"q": "Website palsu untuk curi akun disebut?", "options": ["Phishing", "Deface", "Exploit"], "correct": 0}
        ]
    }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/get_level/<int:level_id>')
def get_level(level_id):
    if level_id >= len(LEVELS_DATA):
        return jsonify({"status": "finished"})
    
    level = LEVELS_DATA[level_id]
    # Ambil 5 soal unik secara acak untuk level tersebut
    selected_questions = random.sample(level['bank'], 5)
    
    # Hapus kunci 'correct' sebelum dikirim ke client agar tidak bisa di-inspect
    client_questions = []
    for q in selected_questions:
        client_questions.append({
            "q": q["q"],
            "options": q["options"]
        })
    
    return jsonify({
        "status": "success",
        "title": level["title"],
        "edu": level["edu"],
        "questions": client_questions
    })

@app.route('/api/verify', methods=['POST'])
def verify_answer():
    data = request.json
    level_id = data.get('level_id')
    question_text = data.get('question')
    choice = data.get('choice')
    
    # Cari jawaban yang benar di backend
    level = LEVELS_DATA[level_id]
    correct_answer = next((q for q in level['bank'] if q['q'] == question_text), None)
    
    if correct_answer and correct_answer['correct'] == choice:
        return jsonify({"status": "correct"})
    else:
        # Jika salah, kirimkan soal pengganti (Anti-stuck)
        # Ambil soal yang belum dipakai (di sini kita ambil random saja dari bank yang berbeda)
        new_q = random.choice([q for q in level['bank'] if q['q'] != question_text])
        return jsonify({
            "status": "incorrect",
            "new_question": {
                "q": new_q["q"],
                "options": new_q["options"]
            }
        })

if __name__ == '__main__':
    app.run(debug=True)