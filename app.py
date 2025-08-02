import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_price_from_cosmetica(barcode):
    url = f"https://www.cosmetica.com.tr/search?s={barcode}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return {"error": "Siteye erişilemedi."}

    soup = BeautifulSoup(response.text, "html.parser")

    # Ürün kartını bul (class'a değil yapıya göre git)
    product = soup.find("div", class_="h-full")
    if not product:
        return {"error": "Ürün bulunamadı."}

    # Ürün adı
    name_tag = product.find("div", class_="mb-1")
    name = name_tag.get_text(strip=True) if name_tag else "Ürün adı bulunamadı"

    # Eski fiyat (üstü çizili olan)
    price_tag = product.find("div", class_="pb-1")
    price = price_tag.get_text(strip=True) if price_tag else "Yok"

    # İndirimli fiyat
    discount_tag = product.find("div", class_="text-base")
    discount = discount_tag.get_text(strip=True) if discount_tag else "Yok"

    return {
        "barcode": barcode,
        "name": name,
        "price": price,
        "discount": discount
    }

@app.route("/price")
def price():
    barcode = request.args.get("barcode")
    if not barcode:
        return jsonify({"error": "barcode parametresi eksik"}), 400

    result = get_price_from_cosmetica(barcode)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
