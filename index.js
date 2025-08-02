import express from 'express';
import puppeteer from 'puppeteer';

const app = express();
const PORT = process.env.PORT || 3000;

app.get('/price', async (req, res) => {
  const barcode = req.query.barcode;
  if (!barcode) return res.status(400).json({ error: 'Barcode is required.' });

  const url = `https://cosmetica.com.tr/search?s=${barcode}`;
  let browser;

  try {
    browser = await puppeteer.launch({
      headless: 'new',
      args: ['--no-sandbox', '--disable-setuid-sandbox'],
    });

    const page = await browser.newPage();
    await page.goto(url, { waitUntil: 'domcontentloaded' });

    const result = await page.evaluate(() => {
      const product = document.querySelector('div.h-full');
      if (!product) return null;

      const discounted = product.querySelector('.price .price-new')?.innerText?.trim();
      const original = product.querySelector('.text-base')?.innerText?.trim();
      const name = product.querySelector('.mb-1')?.innerText?.trim();

      return {
        discountedPrice: discounted || null,
        originalPrice: original || null,
        name: name || null,
      };
    });

    if (!result) return res.status(404).json({ error: 'Product not found' });
    res.json(result);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Server error' });
  } finally {
    if (browser) await browser.close();
  }
});

app.listen(PORT, () => {
  console.log(`API ready at http://localhost:${PORT}`);
});
