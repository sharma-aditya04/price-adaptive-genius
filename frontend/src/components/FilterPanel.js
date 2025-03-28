import React, { useState, useEffect } from 'react';
import {
    Box,
    Paper,
    Typography,
    FormControl,
    InputLabel,
    Select,
    MenuItem,
    TextField,
    Button,
    Divider
} from '@mui/material';
import { productService } from '../services/productService';

const FilterPanel = ({ filters, onFilterChange }) => {
    const [categories, setCategories] = useState({});
    const [brands, setBrands] = useState([]);
    const [localFilters, setLocalFilters] = useState(filters);

    useEffect(() => {
        fetchFilterOptions();
    }, []);

    useEffect(() => {
        setLocalFilters(filters);
    }, [filters]);

    const fetchFilterOptions = async () => {
        try {
            const [categoriesData, brandsData] = await Promise.all([
                productService.getCategories(),
                productService.getBrands()
            ]);
            setCategories(categoriesData);
            setBrands(brandsData);
        } catch (error) {
            console.error('Error fetching filter options:', error);
        }
    };

    const handleChange = (field) => (event) => {
        const newFilters = {
            ...localFilters,
            [field]: event.target.value
        };
        setLocalFilters(newFilters);
    };

    const handleApplyFilters = () => {
        onFilterChange(localFilters);
    };

    const handleReset = () => {
        const resetFilters = {
            category: '',
            subcategory: '',
            brand: '',
            minPrice: '',
            maxPrice: ''
        };
        setLocalFilters(resetFilters);
        onFilterChange(resetFilters);
    };

    return (
        <Paper sx={{ p: 2, width: 250 }}>
            <Typography variant="h6" gutterBottom>
                Filters
            </Typography>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                <FormControl fullWidth>
                    <InputLabel>Category</InputLabel>
                    <Select
                        value={localFilters.category}
                        label="Category"
                        onChange={handleChange('category')}
                    >
                        <MenuItem value="">All Categories</MenuItem>
                        {Object.keys(categories).map((category) => (
                            <MenuItem key={category} value={category}>
                                {category}
                            </MenuItem>
                        ))}
                    </Select>
                </FormControl>

                {localFilters.category && (
                    <FormControl fullWidth>
                        <InputLabel>Subcategory</InputLabel>
                        <Select
                            value={localFilters.subcategory}
                            label="Subcategory"
                            onChange={handleChange('subcategory')}
                        >
                            <MenuItem value="">All Subcategories</MenuItem>
                            {categories[localFilters.category]?.map((subcategory) => (
                                <MenuItem key={subcategory} value={subcategory}>
                                    {subcategory}
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>
                )}

                <FormControl fullWidth>
                    <InputLabel>Brand</InputLabel>
                    <Select
                        value={localFilters.brand}
                        label="Brand"
                        onChange={handleChange('brand')}
                    >
                        <MenuItem value="">All Brands</MenuItem>
                        {brands.map((brand) => (
                            <MenuItem key={brand} value={brand}>
                                {brand}
                            </MenuItem>
                        ))}
                    </Select>
                </FormControl>

                <Divider />

                <TextField
                    label="Min Price"
                    type="number"
                    value={localFilters.minPrice}
                    onChange={handleChange('minPrice')}
                    fullWidth
                />

                <TextField
                    label="Max Price"
                    type="number"
                    value={localFilters.maxPrice}
                    onChange={handleChange('maxPrice')}
                    fullWidth
                />

                <Box sx={{ display: 'flex', gap: 1 }}>
                    <Button
                        variant="contained"
                        onClick={handleApplyFilters}
                        fullWidth
                    >
                        Apply Filters
                    </Button>
                    <Button
                        variant="outlined"
                        onClick={handleReset}
                        fullWidth
                    >
                        Reset
                    </Button>
                </Box>
            </Box>
        </Paper>
    );
};

export default FilterPanel; 