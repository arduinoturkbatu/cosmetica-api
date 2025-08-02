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

    product = soup.select_one("div.product-item")
    if not product:
        return {"error": "Ürün bulunamadı."}

    name = product.select_one("h3.product-name").get_text(strip=True)
    price = product.select_one(".product-price").get_text(strip=True)

    return {
        "barcode": barcode,
        "name": name,
        "price": price
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
