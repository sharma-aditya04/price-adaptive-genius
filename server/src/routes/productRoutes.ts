import express from 'express';
import pool from '../config/database';

const router = express.Router();

// Get all products
router.get('/', async (req, res) => {
  try {
    const [products] = await pool.query('SELECT * FROM products');
    res.json(products);
  } catch (error) {
    res.status(500).json({ message: 'Error fetching products', error });
  }
});

// Get single product
router.get('/:id', async (req, res) => {
  try {
    const [products] = await pool.query('SELECT * FROM products WHERE id = ?', [req.params.id]);
    if (!Array.isArray(products) || products.length === 0) {
      return res.status(404).json({ message: 'Product not found' });
    }
    res.json(products[0]);
  } catch (error) {
    res.status(500).json({ message: 'Error fetching product', error });
  }
});

// Create new product
router.post('/', async (req, res) => {
  try {
    const { name, description, basePrice, currentPrice, category, brand, url, minPrice, maxPrice, targetMargin } = req.body;
    
    const [result] = await pool.query(
      'INSERT INTO products (name, description, base_price, current_price, category, brand, url, min_price, max_price, target_margin) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
      [name, description, basePrice, currentPrice, category, brand, url, minPrice, maxPrice, targetMargin]
    );

    const [newProduct] = await pool.query('SELECT * FROM products WHERE id = ?', [(result as any).insertId]);
    res.status(201).json(newProduct[0]);
  } catch (error) {
    res.status(400).json({ message: 'Error creating product', error });
  }
});

// Update product
router.put('/:id', async (req, res) => {
  try {
    const { name, description, basePrice, currentPrice, category, brand, url, minPrice, maxPrice, targetMargin } = req.body;
    
    await pool.query(
      'UPDATE products SET name = ?, description = ?, base_price = ?, current_price = ?, category = ?, brand = ?, url = ?, min_price = ?, max_price = ?, target_margin = ? WHERE id = ?',
      [name, description, basePrice, currentPrice, category, brand, url, minPrice, maxPrice, targetMargin, req.params.id]
    );

    const [updatedProduct] = await pool.query('SELECT * FROM products WHERE id = ?', [req.params.id]);
    if (!Array.isArray(updatedProduct) || updatedProduct.length === 0) {
      return res.status(404).json({ message: 'Product not found' });
    }
    res.json(updatedProduct[0]);
  } catch (error) {
    res.status(400).json({ message: 'Error updating product', error });
  }
});

// Delete product
router.delete('/:id', async (req, res) => {
  try {
    const [result] = await pool.query('DELETE FROM products WHERE id = ?', [req.params.id]);
    if ((result as any).affectedRows === 0) {
      return res.status(404).json({ message: 'Product not found' });
    }
    res.json({ message: 'Product deleted successfully' });
  } catch (error) {
    res.status(500).json({ message: 'Error deleting product', error });
  }
});

// Update product price
router.patch('/:id/price', async (req, res) => {
  try {
    const { price } = req.body;
    
    // Get current price
    const [products] = await pool.query('SELECT current_price FROM products WHERE id = ?', [req.params.id]);
    if (!Array.isArray(products) || products.length === 0) {
      return res.status(404).json({ message: 'Product not found' });
    }

    const currentPrice = (products[0] as any).current_price;

    // Add to price history
    await pool.query(
      'INSERT INTO price_history (product_id, price) VALUES (?, ?)',
      [req.params.id, currentPrice]
    );

    // Update current price
    await pool.query(
      'UPDATE products SET current_price = ? WHERE id = ?',
      [price, req.params.id]
    );

    const [updatedProduct] = await pool.query('SELECT * FROM products WHERE id = ?', [req.params.id]);
    res.json(updatedProduct[0]);
  } catch (error) {
    res.status(400).json({ message: 'Error updating price', error });
  }
});

export default router; 