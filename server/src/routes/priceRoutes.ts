import express from 'express';
import axios from 'axios';
import pool from '../config/database';

const router = express.Router();

// Predict price using AI model
router.post('/predict', async (req, res) => {
  try {
    const { productId } = req.body;
    
    // Get product data
    const [products] = await pool.query('SELECT * FROM products WHERE id = ?', [productId]);
    if (!Array.isArray(products) || products.length === 0) {
      return res.status(404).json({ message: 'Product not found' });
    }

    const product = products[0];

    // Get competitor prices
    const [competitorPrices] = await pool.query(
      'SELECT source, price FROM competitor_prices WHERE product_id = ?',
      [productId]
    );

    // Call AI model endpoint
    const response = await axios.post(process.env.AI_MODEL_ENDPOINT || 'http://localhost:8000/predict', {
      product: {
        name: product.name,
        description: product.description,
        category: product.category,
        brand: product.brand,
        currentPrice: product.current_price,
        competitorPrices: competitorPrices
      }
    });

    const predictedPrice = response.data.predictedPrice;

    // Apply pricing rules
    const finalPrice = applyPricingRules(predictedPrice, {
      minPrice: product.min_price,
      maxPrice: product.max_price,
      targetMargin: product.target_margin
    });

    res.json({
      predictedPrice,
      finalPrice,
      pricingRules: {
        minPrice: product.min_price,
        maxPrice: product.max_price,
        targetMargin: product.target_margin
      }
    });
  } catch (error) {
    res.status(500).json({ message: 'Error predicting price', error });
  }
});

// Update competitor prices
router.post('/competitor-prices', async (req, res) => {
  try {
    const { productId, competitorPrices } = req.body;
    
    // Check if product exists
    const [products] = await pool.query('SELECT id FROM products WHERE id = ?', [productId]);
    if (!Array.isArray(products) || products.length === 0) {
      return res.status(404).json({ message: 'Product not found' });
    }

    // Delete existing competitor prices
    await pool.query('DELETE FROM competitor_prices WHERE product_id = ?', [productId]);

    // Insert new competitor prices
    for (const price of competitorPrices) {
      await pool.query(
        'INSERT INTO competitor_prices (product_id, source, price) VALUES (?, ?, ?)',
        [productId, price.source, price.price]
      );
    }

    // Get updated product with competitor prices
    const [updatedProduct] = await pool.query(
      `SELECT p.*, 
        GROUP_CONCAT(
          JSON_OBJECT(
            'source', cp.source,
            'price', cp.price,
            'lastChecked', cp.last_checked
          )
        ) as competitor_prices
      FROM products p
      LEFT JOIN competitor_prices cp ON p.id = cp.product_id
      WHERE p.id = ?
      GROUP BY p.id`,
      [productId]
    );

    res.json(updatedProduct[0]);
  } catch (error) {
    res.status(400).json({ message: 'Error updating competitor prices', error });
  }
});

// Helper function to apply pricing rules
function applyPricingRules(predictedPrice: number, rules: any): number {
  let finalPrice = predictedPrice;

  // Ensure price is within min and max bounds
  finalPrice = Math.max(rules.minPrice, Math.min(rules.maxPrice, finalPrice));

  // Apply target margin
  const targetPrice = finalPrice * (1 + rules.targetMargin);
  finalPrice = Math.min(rules.maxPrice, targetPrice);

  return finalPrice;
}

export default router; 