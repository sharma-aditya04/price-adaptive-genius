import React, { useState, useEffect } from 'react';
import { productService } from '../services/productService';
import ProductCard from './ProductCard';
import { Box, Grid, Typography, CircularProgress, Alert } from '@mui/material';
import FilterPanel from './FilterPanel';

const ProductList = () => {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [filters, setFilters] = useState({
        category: '',
        subcategory: '',
        brand: '',
        minPrice: '',
        maxPrice: ''
    });

    useEffect(() => {
        fetchProducts();
    }, [filters]);

    const fetchProducts = async () => {
        try {
            setLoading(true);
            setError(null);
            const response = await productService.getProducts(filters);
            setProducts(response.products);
        } catch (err) {
            setError('Failed to fetch products. Please try again later.');
            console.error('Error fetching products:', err);
        } finally {
            setLoading(false);
        }
    };

    const handleFilterChange = (newFilters) => {
        setFilters(prev => ({
            ...prev,
            ...newFilters
        }));
    };

    if (loading) {
        return (
            <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
                <CircularProgress />
            </Box>
        );
    }

    if (error) {
        return (
            <Box m={3}>
                <Alert severity="error">{error}</Alert>
            </Box>
        );
    }

    return (
        <Box sx={{ display: 'flex', gap: 3, p: 3 }}>
            <FilterPanel filters={filters} onFilterChange={handleFilterChange} />
            <Box sx={{ flexGrow: 1 }}>
                <Typography variant="h5" gutterBottom>
                    Products ({products.length})
                </Typography>
                <Grid container spacing={3}>
                    {products.map((product) => (
                        <Grid item xs={12} sm={6} md={4} lg={3} key={product.id}>
                            <ProductCard product={product} />
                        </Grid>
                    ))}
                </Grid>
            </Box>
        </Box>
    );
};

export default ProductList; 