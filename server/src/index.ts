import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import productRoutes from './routes/productRoutes';
import priceRoutes from './routes/priceRoutes';
import pool from './config/database';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());

// Routes
app.use('/api/products', productRoutes);
app.use('/api/prices', priceRoutes);

// Test database connection
pool.getConnection()
  .then(connection => {
    console.log('Connected to MySQL database');
    connection.release();
  })
  .catch(error => {
    console.error('MySQL connection error:', error);
  });

// Start server
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
}); 