from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright
import os

app = Flask(__name__)

def fetch_product_info(barcode):
    url = f"https://www.cosmetica.com.tr/search?s={barcode}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_timeout(4000)  # 4 saniye bekle, site JS renderı için

        # Burada CSS selector ile ürün bilgilerini çek
        product_element = page.query_selector("a.flex.h-full.w-full.grow.flex-col.overflow-hidden.rounded.rounded-b-none.border.border-b-0.border-neutral-300\\/70")
        if not product_element:
            browser.close()
            return None

        product_url = "https://www.cosmetica.com.tr" + product_element.get_attribute("href")
        product_name = product_element.query_selector("div.mb-1.text-left.text-sm.font-semibold.text-button-01").inner_text().strip()

        price_section = product_element.evaluate_handle('el => el.nextElementSibling')
        original_price_div = price_section.query_selector("div.pb-1.text-xs.font-medium.text-button-01\\/50.line-through.md\\:text-sm")
        discounted_price_div = price_section.query_selector("div.text-base.font-semibold.text-button-01.md\\:text-lg")

        original_price = original_price_div.inner_text().strip() if original_price_div else None
        discounted_price = discounted_price_div.inner_text().strip() if discounted_price_div else None

        browser.close()

        if not discounted_price:
            discounted_price = original_price
            original_price = None

        return {
            "product_name": product_name,
            "product_url": product_url,
            "original_price": original_price,
            "discounted_price": discounted_price
        }

@app.route("/get-price", methods=["GET"])
def get_price():
    barcode = request.args.get("barcode")
    if not barcode:
        return jsonify({"error": "Barkod parametresi eksik"}), 400

    data = fetch_product_info(barcode)
    if not data:
        return jsonify({"error": "Ürün bulunamadı veya bir hata oluştu."}), 404

    return jsonify(data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
