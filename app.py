from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import time

app = Flask(__name__)

@app.route('/price', methods=['GET'])
def get_price():
    barcode = request.args.get('barcode')
    if not barcode:
        return jsonify({'error': 'barcode parameter is required'}), 400

    url = f'https://www.cosmetica.com.tr/search?s={barcode}'

    try:
        # Basit HTTP isteği
        response = requests.get(url)
        if response.status_code != 200:
            return jsonify({'error': 'Failed to fetch data from Cosmetica'}), 500
        
        # Burada bekleme yapabiliriz (örneğin 3 sn)
        time.sleep(3)

        soup = BeautifulSoup(response.text, 'html.parser')

        # Ürün bloğunu bul
        product = soup.find('a', class_='flex h-full w-full grow flex-col overflow-hidden rounded rounded-b-none border border-b-0 border-neutral-300/70')

        if not product:
            return jsonify({'error': 'Product not found'}), 404

        # Ürün ismi
        product_name_div = product.find('div', class_='mb-1 mt-0.5 text-left text-sm font-semibold text-button-01')
        product_name = product_name_div.text.strip() if product_name_div else ''

        # Fiyat bilgileri
        price_div = product.find('div', class_='text-base font-semibold !leading-none text-button-01 md:text-lg')
        discounted_price = price_div.text.strip() if price_div else ''

        original_price_div = product.find('div', class_='pb-1 text-xs font-medium !leading-none text-button-01/50 line-through md:text-sm')
        original_price = original_price_div.text.strip() if original_price_div else discounted_price

        return jsonify({
            'product_name': product_name,
            'original_price': original_price,
            'discounted_price': discounted_price,
            'product_url': 'https://www.cosmetica.com.tr' + product['href']
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
