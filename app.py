import os
from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright

app = Flask(__name__)

def get_price_from_cosmetica(barcode):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Cosmetica'da arama yap
        search_url = f"https://www.cosmetica.com.tr/search?s={barcode}"
        page.goto(search_url)
        page.wait_for_timeout(3000)  # Sayfa yüklenmesi için kısa bekleme

        try:
            # Ürün bilgilerini çek
            title = page.locator("h2.card-title").first.inner_text()
            price = page.locator(".currentPrice").first.inner_text()

            return {
                "barcode": barcode,
                "title": title,
                "price": price
            }

        except Exception as e:
            return {
                "barcode": barcode,
                "error": "Ürün bulunamadı veya sayfa yapısı değişmiş olabilir.",
                "details": str(e)
            }

        finally:
            browser.close()

@app.route("/price", methods=["GET"])
def price():
    barcode = request.args.get("barcode")
    if not barcode:
        return jsonify({"error": "Lütfen ?barcode= parametresi giriniz"}), 400
    
    result = get_price_from_cosmetica(barcode)
    return jsonify(result)

# Render 10000 portunu kullanır
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render'ın verdiği portu oku, yoksa 10000'e düş
    app.run(host="0.0.0.0", port=port)
