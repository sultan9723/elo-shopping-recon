# ELO.shopping Cybersecurity Recon (Ethical)

## 🧠 Objective
This is an ethical recon project for learning purposes. The target elo.shopping was analyzed using passive and active information gathering tools.

## 🛠 Tools Used
- Nmap
- Nikto
- Gobuster
- Curl

## 🔍 Key Findings
- /admin/ and /admin4.nsf paths found
- /password.inc exists with open CORS
- /.xml and /.json return 200 OK — potential API endpoints
- Missing HTTP headers like X-Content-Type-Options
- Hosted via Shopify & Cloudflare — stack information leaked via headers

## 📁 Folder Structure
- scan/ – Stores recon output files

## ⚠️ Ethical Note
This project was done for *educational and non-destructive purposes only*. No exploitation, fuzzing, or password attacks were performed.

## 📅 Date
July 2025
