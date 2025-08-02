const express = require("express");
const puppeteer = require("puppeteer");

const app = express();

async function getPriceFromCosmetica(barcode) {
  const browser = await puppeteer.launch({
    args: ["--no-sandbox", "--disable-setuid-sandbox"]
  });
  const page = await browser.newPage();
  const url = `https://www.cosmetica.com.tr/search?s=${barcode}`;
  await page.goto(url, { waitUntil: "networkidle2" });

  const result = await page.evaluate(() => {
    const product = document.querySelector(".h-full");
    if (!product) return { error: "Ürün bulunamadı." };

    const name = product.querySelector(".mb-1")?.innerText;
    const price = product.querySelector(".pb-1")?.innerText;
    const discount = product.querySelector(".text-base")?.innerText;

    return {
      name,
      price,
      discount
    };
  });

  await browser.close();
  return result;
}

app.get("/price", async (req, res) => {
  const barcode = req.query.barcode;
  if (!barcode) return res.status(400).json({ error: "barcode parametresi eksik" });

  try {
    const result = await getPriceFromCosmetica(barcode);
    res.json({ barcode, ...result });
  } catch (error) {
    res.status(500).json({ error: "Sunucu hatası", details: error.message });
  }
});

const PORT = process.env.PORT || 10000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
