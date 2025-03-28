import React from 'react';
import {
    Card,
    CardContent,
    CardMedia,
    Typography,
    Box,
    Chip,
    IconButton,
    Tooltip
} from '@mui/material';
import {
    Favorite as FavoriteIcon,
    FavoriteBorder as FavoriteBorderIcon,
    ShoppingCart as ShoppingCartIcon
} from '@mui/icons-material';

const ProductCard = ({ product }) => {
    const [isFavorite, setIsFavorite] = React.useState(false);

    const handleFavoriteClick = () => {
        setIsFavorite(!isFavorite);
    };

    const formatPrice = (price) => {
        return new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR',
            maximumFractionDigits: 0
        }).format(price);
    };

    const calculateDiscount = () => {
        const discount = ((product.base_price - product.current_price) / product.base_price) * 100;
        return Math.round(discount);
    };

    return (
        <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
            <CardMedia
                component="img"
                height="200"
                image={product.url}
                alt={product.name}
                sx={{ objectFit: 'contain', p: 1, bgcolor: 'background.paper' }}
            />
            <CardContent sx={{ flexGrow: 1 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 1 }}>
                    <Typography variant="subtitle2" color="text.secondary">
                        {product.brand}
                    </Typography>
                    <Tooltip title={isFavorite ? "Remove from favorites" : "Add to favorites"}>
                        <IconButton size="small" onClick={handleFavoriteClick}>
                            {isFavorite ? <FavoriteIcon color="error" /> : <FavoriteBorderIcon />}
                        </IconButton>
                    </Tooltip>
                </Box>

                <Typography variant="h6" component="div" gutterBottom>
                    {product.name}
                </Typography>

                <Typography variant="body2" color="text.secondary" gutterBottom>
                    {product.description}
                </Typography>

                <Box sx={{ mt: 2 }}>
                    <Typography variant="h6" color="primary">
                        {formatPrice(product.current_price)}
                    </Typography>
                    {product.current_price < product.base_price && (
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 0.5 }}>
                            <Typography variant="body2" color="text.secondary" sx={{ textDecoration: 'line-through' }}>
                                {formatPrice(product.base_price)}
                            </Typography>
                            <Chip
                                label={`${calculateDiscount()}% OFF`}
                                color="success"
                                size="small"
                            />
                        </Box>
                    )}
                </Box>

                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mt: 2 }}>
                    <Chip
                        label={product.category}
                        size="small"
                        variant="outlined"
                    />
                    <Tooltip title="Add to cart">
                        <IconButton color="primary">
                            <ShoppingCartIcon />
                        </IconButton>
                    </Tooltip>
                </Box>
            </CardContent>
        </Card>
    );
};

export default ProductCard; 