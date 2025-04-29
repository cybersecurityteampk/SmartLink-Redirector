# 🔗 SmartLink-Redirector | Track IPs via YouTube Redirect (Python + Cloudflare Tunnel)

A smart and simple IP Logger that redirects users to a YouTube video while logging their IP address, geolocation, browser details, and access time.

> ⚠️ For **educational**, **ethical hacking**, and **cybersecurity awareness** purposes only.

---

## 📌 What is SmartLink-Redirector?

This tool is a Python-based HTTP server that logs user information and redirects them to a YouTube video of your choice.  
It can be publicly accessible via **Cloudflare Tunnel**, making it perfect for awareness campaigns, ethical hacking demos, and red team simulations.

---

## 🌟 Features

- ✅ Logs IP address, city, country, and coordinates
- ✅ Captures browser user-agent
- ✅ Saves access date & time
- ✅ Auto-redirects user to any YouTube video
- ✅ Public access via Cloudflare Tunnel
- ✅ Lightweight and beginner-friendly


## ⚙️ Requirements

Make sure you have the following installed:

- Python
- `pip` (Python package manager)
- Cloudflared (for public tunnel)

- wget https://github.com/cloudflare/cloudflared/releases/download/2023.4.0/cloudflared-linux-amd64.deb
- sudo dpkg -i cloudflared-linux-amd64.deb
- cloudflared tunnel --url http://localhost:4444


## 🔧 Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/cybersecurityteampk/SmartLink-Redirector.git
cd SmartLink-Redirector
