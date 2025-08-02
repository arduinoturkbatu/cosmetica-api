from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright

app = Flask(__name__)

def scrape_cosmetica(barcode: str):
    url = f"https://www.cosmetica.com.tr/search?s={barcode}"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        # Sayfanın tamamen yüklenmesini bekleyelim
        page.wait_for_load_state("networkidle")
        
        # Ürün kartını seçelim
        product = page.query_selector("a.flex.h-full.w-full.grow.flex-col.overflow-hidden.rounded.border")
        if not product:
            browser.close()
            return None
        
        product_url = "https://www.cosmetica.com.tr" + product.get_attribute("href")
        product_name = product.query_selector("div.mb-1.text-left.text-sm.font-semibold").inner_text().strip()
        
        # Fiyat bilgilerini alalım
        price_container = product.query_selector("div.mt-auto.flex.items-center.gap-2")
        if not price_container:
            browser.close()
            return None
        
        original_price = price_container.query_selector("div.text-xs.font-medium.line-through")
        discounted_price = price_container.query_selector("div.text-base.font-semibold")
        
        original_price_text = original_price.inner_text().strip() if original_price else None
        discounted_price_text = discounted_price.inner_text().strip() if discounted_price else None
        
        browser.close()
        
        return {
            "product_url": product_url,
            "product_name": product_name,
            "original_price": original_price_text or discounted_price_text,
            "discounted_price": discounted_price_text or original_price_text
        }

@app.route("/product", methods=["GET"])
def get_product():
    barcode = request.args.get("barcode")
    if not barcode:
        return jsonify({"error": "barcode param missing"}), 400
    
    result = scrape_cosmetica(barcode)
    if not result:
        return jsonify({"error": "Product not found or page structure changed"}), 404
    
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
