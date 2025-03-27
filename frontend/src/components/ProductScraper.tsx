import React, { useState } from 'react';
import { Box, TextField, Button, Typography, Paper, CircularProgress, Alert, Snackbar } from '@mui/material';
import { styled } from '@mui/material/styles';
import { scrapeProduct, ProductInfo } from '../services/scraperService';
import '../styles/global.css';

const StyledPaper = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(4),
  margin: theme.spacing(3),
  background: 'var(--glass-gradient)',
  backdropFilter: 'blur(10px)',
  borderRadius: '20px',
  boxShadow: '0 8px 32px rgba(0, 0, 0, 0.1)',
  transition: 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
  border: '1px solid rgba(255, 255, 255, 0.2)',
  '&:hover': {
    transform: 'translateY(-8px) scale(1.02)',
    boxShadow: '0 20px 40px rgba(0, 0, 0, 0.15)',
  },
}));

const StyledTextField = styled(TextField)(({ theme }) => ({
  '& .MuiOutlinedInput-root': {
    background: 'rgba(255, 255, 255, 0.9)',
    backdropFilter: 'blur(5px)',
    borderRadius: '12px',
    transition: 'all 0.3s ease',
    '&:hover fieldset': {
      borderColor: '#4f46e5',
    },
    '&.Mui-focused fieldset': {
      borderColor: '#4f46e5',
      boxShadow: '0 0 0 4px rgba(79, 70, 229, 0.1)',
    },
  },
}));

const StyledButton = styled(Button)(({ theme }) => ({
  background: 'var(--primary-gradient)',
  color: 'white',
  padding: '14px 28px',
  borderRadius: '12px',
  fontWeight: 600,
  transition: 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
  letterSpacing: '0.5px',
  textTransform: 'uppercase',
  fontSize: '0.9rem',
  '&:hover': {
    transform: 'translateY(-3px)',
    boxShadow: '0 8px 20px rgba(79, 70, 229, 0.4)',
  },
  '&::after': {
    content: '""',
    position: 'absolute',
    top: 0,
    left: 0,
    width: '100%',
    height: '100%',
    background: 'linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.3), transparent)',
    transform: 'translateX(-100%)',
    transition: 'transform 0.8s ease',
  },
  '&:hover::after': {
    transform: 'translateX(100%)',
  },
}));

const ProductScraper: React.FC = () => {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  const [productData, setProductData] = useState<ProductInfo | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(false);
    setProductData(null);

    try {
      const result = await scrapeProduct(url);
      setProductData(result);
      setSuccess(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to scrape product');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ 
      display: 'flex', 
      flexDirection: 'column', 
      alignItems: 'center',
      animation: 'fadeIn 0.6s ease-out',
      minHeight: '100vh',
      background: 'var(--background-gradient)',
      padding: '2rem',
    }}>
      <StyledPaper elevation={3}>
        <Typography 
          variant="h4" 
          gutterBottom 
          sx={{ 
            background: 'var(--primary-gradient)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            fontWeight: 'bold',
            mb: 4,
            textAlign: 'center',
            animation: 'fadeIn 0.8s ease-out',
          }}
        >
          Product Scraper
        </Typography>
        
        <form onSubmit={handleSubmit} style={{ width: '100%' }}>
          <StyledTextField
            fullWidth
            label="Enter Product URL"
            variant="outlined"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://www.amazon.in/..."
            margin="normal"
            required
            sx={{ mb: 3 }}
          />
          
          <Box sx={{ 
            display: 'flex', 
            justifyContent: 'center',
            animation: 'scaleIn 0.6s ease-out',
          }}>
            <StyledButton
              type="submit"
              variant="contained"
              disabled={loading}
              sx={{ 
                minWidth: '200px',
                position: 'relative',
                overflow: 'hidden',
              }}
            >
              {loading ? (
                <CircularProgress 
                  size={24} 
                  sx={{ 
                    color: 'white',
                    animation: 'spin 1s linear infinite'
                  }} 
                />
              ) : (
                'Scrape Product'
              )}
            </StyledButton>
          </Box>
        </form>

        {productData && (
          <Box sx={{ 
            mt: 4,
            animation: 'fadeIn 0.6s ease-out',
            background: 'rgba(255, 255, 255, 0.8)',
            borderRadius: '12px',
            padding: '20px',
            backdropFilter: 'blur(5px)',
          }}>
            <Typography variant="h6" gutterBottom sx={{ color: '#4f46e5' }}>
              Product Details
            </Typography>
            <Typography variant="body1" gutterBottom>
              <strong>Name:</strong> {productData["Product Name"]}
            </Typography>
            <Typography variant="body1" gutterBottom>
              <strong>Price:</strong> {productData["Price"]}
            </Typography>
            <Typography variant="body1" gutterBottom>
              <strong>Stock:</strong> {productData["Stock"]}
            </Typography>
            {productData["Description"] && (
              <Typography variant="body1" gutterBottom>
                <strong>Description:</strong> {productData["Description"]}
              </Typography>
            )}
            {productData["Rating"] && (
              <Typography variant="body1" gutterBottom>
                <strong>Rating:</strong> {productData["Rating"]}
              </Typography>
            )}
            {productData["Reviews Count"] && (
              <Typography variant="body1" gutterBottom>
                <strong>Reviews:</strong> {productData["Reviews Count"]}
              </Typography>
            )}
          </Box>
        )}
      </StyledPaper>

      <Snackbar 
        open={!!error} 
        autoHideDuration={6000} 
        onClose={() => setError(null)}
        anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
      >
        <Alert 
          onClose={() => setError(null)} 
          severity="error" 
          sx={{ 
            width: '100%',
            background: 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)',
            color: 'white',
            '& .MuiAlert-icon': {
              color: 'white'
            },
            animation: 'slideIn 0.4s ease-out',
            backdropFilter: 'blur(5px)',
            border: '1px solid rgba(255, 255, 255, 0.2)',
          }}
        >
          {error}
        </Alert>
      </Snackbar>

      <Snackbar 
        open={success} 
        autoHideDuration={6000} 
        onClose={() => setSuccess(false)}
        anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
      >
        <Alert 
          onClose={() => setSuccess(false)} 
          severity="success" 
          sx={{ 
            width: '100%',
            background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
            color: 'white',
            '& .MuiAlert-icon': {
              color: 'white'
            },
            animation: 'slideIn 0.4s ease-out',
            backdropFilter: 'blur(5px)',
            border: '1px solid rgba(255, 255, 255, 0.2)',
          }}
        >
          Product scraped successfully!
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default ProductScraper; 