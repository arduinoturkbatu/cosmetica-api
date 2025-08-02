from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

app = Flask(__name__)

def get_price_from_cosmetica(barcode: str):
    search_url = f"https://www.cosmetica.com.tr/search?s={barcode}"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(search_url)

        # Sayfanın tamamen yüklenmesi için bekle
        try:
            # Ürün linkini içeren ana div yüklensin diye bekliyoruz (max 7 saniye)
            page.wait_for_selector("div.relative.flex.h-full.w-full.grow.flex-col.overflow-hidden", timeout=7000)
        except PlaywrightTimeoutError:
            browser.close()
            return None

        # Ürün sayfası linkini al
        product_link_element = page.query_selector("div.relative.flex.h-full.w-full.grow.flex-col.overflow-hidden > a")
        if not product_link_element:
            browser.close()
            return None
        product_url = "https://www.cosmetica.com.tr" + product_link_element.get_attribute("href")

        # Ürün sayfasına git
        page.goto(product_url)
        try:
            # Fiyat bilgilerini içeren elementler yüklenene kadar bekle (max 7 saniye)
            page.wait_for_selector("div.text-base.font-semibold", timeout=7000)
        except PlaywrightTimeoutError:
            browser.close()
            return None

        # Fiyatları çek
        discounted_price_element = page.query_selector("div.text-base.font-semibold")
        original_price_element = page.query_selector("div.text-xs.font-medium.line-through")

        discounted_price = discounted_price_element.inner_text().strip() if discounted_price_element else None
        original_price = original_price_element.inner_text().strip() if original_price_element else discounted_price

        browser.close()
        return {
            "product_url": product_url,
            "discounted_price": discounted_price,
            "original_price": original_price
        }


@app.route('/price')
def price():
    barcode = request.args.get('barcode')
    if not barcode:
        return jsonify({"error": "barcode parametresi yok"}), 400
    
    result = get_price_from_cosmetica(barcode)
    if not result:
        return jsonify({"error": "Ürün bulunamadı veya siteye erişilemiyor"}), 404
    
    return jsonify(result)


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
