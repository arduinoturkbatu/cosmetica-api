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

    product = soup.select_one("html body div#__next div div div div.wrapper div.mt-6.grid.lg:gap-8.grid-cols-1.lg:grid-cols-[280px,1fr] div div.grid.h-min.grid-cols-2.gap-4.lg:grid-cols-4 div.relative.flex.h-full.w-full.grow.flex-col.overflow-hidden")
    if not product:
        return {"error": "Ürün bulunamadı."}

    name = product.select_one("html body div#__next div div div div.wrapper div.mt-6.grid.lg:gap-8.grid-cols-1.lg:grid-cols-[280px,1fr] div div.grid.h-min.grid-cols-2.gap-4.lg:grid-cols-4 div.relative.flex.h-full.w-full.grow.flex-col.overflow-hidden a.flex.h-full.w-full.grow.flex-col.overflow-hidden.rounded.rounded-b-none.border.border-b-0.border-neutral-300/70 div.flex.grow.flex-col.p-2.5.!pb-0.md:p-4 div.mb-1.mt-0.5.text-left.text-sm.font-semibold.text-button-01").get_text(strip=True)
    price = product.select_one("html body div#__next div div div div.wrapper div.mt-6.grid.lg:gap-8.grid-cols-1.lg:grid-cols-[280px,1fr] div div.grid.h-min.grid-cols-2.gap-4.lg:grid-cols-4 div.relative.flex.h-full.w-full.grow.flex-col.overflow-hidden a.flex.h-full.w-full.grow.flex-col.overflow-hidden.rounded.rounded-b-none.border.border-b-0.border-neutral-300/70 div.flex.grow.flex-col.p-2.5.!pb-0.md:p-4 div.mt-auto.flex.items-center.gap-2 div.flex.flex-col div.pb-1.text-xs.font-medium.!leading-none.text-button-01/50.line-through.md:text-sm").get_text(strip=True)
    discount = product.select_one("html body div#__next div div div div.wrapper div.mt-6.grid.lg:gap-8.grid-cols-1.lg:grid-cols-[280px,1fr] div div.grid.h-min.grid-cols-2.gap-4.lg:grid-cols-4 div.relative.flex.h-full.w-full.grow.flex-col.overflow-hidden a.flex.h-full.w-full.grow.flex-col.overflow-hidden.rounded.rounded-b-none.border.border-b-0.border-neutral-300/70 div.flex.grow.flex-col.p-2.5.!pb-0.md:p-4 div.mt-auto.flex.items-center.gap-2 div.flex.flex-col div.text-base.font-semibold.!leading-none.text-button-01.md:text-lg").get_text(strip=True)

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
