import React, { useState } from 'react';
import {
    Box,
    Paper,
    TextField,
    Button,
    Typography,
    CircularProgress,
    Alert,
    Grid,
    Card,
    CardContent
} from '@mui/material';
import { productService } from '../services/productService';

const PriceCalculator = () => {
    const [url, setUrl] = useState('');
    const [stock, setStock] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [productData, setProductData] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        setProductData(null);

        try {
            const data = await productService.scrapeProduct(url);
            setProductData(data);
        } catch (err) {
            setError(err.message || 'Failed to fetch product data');
        } finally {
            setLoading(false);
        }
    };

    return (
        <Box sx={{ maxWidth: 800, mx: 'auto', p: 3 }}>
            <Paper sx={{ p: 3, mb: 3 }}>
                <Typography variant="h5" gutterBottom>
                    Price Calculator
                </Typography>
                <form onSubmit={handleSubmit}>
                    <Grid container spacing={2}>
                        <Grid item xs={12}>
                            <TextField
                                fullWidth
                                label="Product URL (Amazon/Flipkart)"
                                value={url}
                                onChange={(e) => setUrl(e.target.value)}
                                placeholder="https://www.amazon.in/..."
                                required
                            />
                        </Grid>
                        <Grid item xs={12}>
                            <TextField
                                fullWidth
                                label="Current Stock"
                                type="number"
                                value={stock}
                                onChange={(e) => setStock(e.target.value)}
                                required
                            />
                        </Grid>
                        <Grid item xs={12}>
                            <Button
                                variant="contained"
                                type="submit"
                                fullWidth
                                disabled={loading}
                            >
                                {loading ? <CircularProgress size={24} /> : 'Calculate Price'}
                            </Button>
                        </Grid>
                    </Grid>
                </form>
            </Paper>

            {error && (
                <Alert severity="error" sx={{ mb: 2 }}>
                    {error}
                </Alert>
            )}

            {productData && (
                <Card>
                    <CardContent>
                        <Grid container spacing={2}>
                            <Grid item xs={12} md={4}>
                                <img
                                    src={productData.url}
                                    alt={productData.name}
                                    style={{ width: '100%', height: 'auto' }}
                                />
                            </Grid>
                            <Grid item xs={12} md={8}>
                                <Typography variant="h6" gutterBottom>
                                    {productData.name}
                                </Typography>
                                <Typography variant="subtitle1" color="text.secondary" gutterBottom>
                                    Brand: {productData.brand}
                                </Typography>
                                <Typography variant="body1" paragraph>
                                    {productData.description}
                                </Typography>
                                <Box sx={{ mt: 2 }}>
                                    <Typography variant="h6" color="primary">
                                        Current Price: ₹{productData.current_price.toLocaleString()}
                                    </Typography>
                                    {productData.base_price > productData.current_price && (
                                        <Typography variant="body2" color="text.secondary" sx={{ textDecoration: 'line-through' }}>
                                            MRP: ₹{productData.base_price.toLocaleString()}
                                        </Typography>
                                    )}
                                    <Typography variant="h6" color="secondary" sx={{ mt: 2 }}>
                                        AI Suggested Price: ₹{(productData.current_price * 0.9).toLocaleString()}
                                    </Typography>
                                    <Typography variant="body2" color="text.secondary">
                                        Based on current market trends and stock levels
                                    </Typography>
                                </Box>
                            </Grid>
                        </Grid>
                    </CardContent>
                </Card>
            )}
        </Box>
    );
};

export default PriceCalculator; 