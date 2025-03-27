
// Types for our data
export type Product = {
  id: number;
  name: string;
  currentPrice: number;
  previousPrice: number;
  suggestedPrice: number;
  category: string;
  image: string;
  inStock: number;
  competitors: CompetitorPrice[];
  priceHistory: PricePoint[];
};

export type CompetitorPrice = {
  name: string;
  price: number;
  inStock: boolean;
};

export type PricePoint = {
  date: string;
  price: number;
};

// Mock data
export const products: Product[] = [
  {
    id: 1,
    name: "Premium Wireless Headphones",
    currentPrice: 199.99,
    previousPrice: 219.99,
    suggestedPrice: 189.99,
    category: "Electronics",
    image: "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8cHJvZHVjdHxlbnwwfHwwfHx8MA%3D%3D",
    inStock: 45,
    competitors: [
      { name: "Competitor A", price: 209.99, inStock: true },
      { name: "Competitor B", price: 199.99, inStock: true },
      { name: "Competitor C", price: 179.99, inStock: false }
    ],
    priceHistory: [
      { date: "2023-06-01", price: 229.99 },
      { date: "2023-07-01", price: 219.99 },
      { date: "2023-08-01", price: 219.99 },
      { date: "2023-09-01", price: 209.99 },
      { date: "2023-10-01", price: 199.99 }
    ]
  },
  {
    id: 2,
    name: "Ultra HD Smart TV 55\"",
    currentPrice: 699.99,
    previousPrice: 749.99,
    suggestedPrice: 679.99,
    category: "Electronics",
    image: "https://images.unsplash.com/photo-1593784991095-a205069470b6?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8dHZ8ZW58MHx8MHx8fDA%3D",
    inStock: 12,
    competitors: [
      { name: "Competitor A", price: 749.99, inStock: true },
      { name: "Competitor B", price: 719.99, inStock: true },
      { name: "Competitor C", price: 689.99, inStock: true }
    ],
    priceHistory: [
      { date: "2023-06-01", price: 799.99 },
      { date: "2023-07-01", price: 789.99 },
      { date: "2023-08-01", price: 769.99 },
      { date: "2023-09-01", price: 749.99 },
      { date: "2023-10-01", price: 699.99 }
    ]
  },
  {
    id: 3,
    name: "Professional DSLR Camera",
    currentPrice: 1299.99,
    previousPrice: 1299.99,
    suggestedPrice: 1349.99,
    category: "Photography",
    image: "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8Y2FtZXJhfGVufDB8fDB8fHww",
    inStock: 8,
    competitors: [
      { name: "Competitor A", price: 1349.99, inStock: true },
      { name: "Competitor B", price: 1299.99, inStock: true },
      { name: "Competitor C", price: 1399.99, inStock: false }
    ],
    priceHistory: [
      { date: "2023-06-01", price: 1299.99 },
      { date: "2023-07-01", price: 1299.99 },
      { date: "2023-08-01", price: 1299.99 },
      { date: "2023-09-01", price: 1299.99 },
      { date: "2023-10-01", price: 1299.99 }
    ]
  },
  {
    id: 4,
    name: "Ergonomic Office Chair",
    currentPrice: 249.99,
    previousPrice: 229.99,
    suggestedPrice: 259.99,
    category: "Furniture",
    image: "https://images.unsplash.com/photo-1580480055273-228ff5388ef8?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8Y2hhaXJ8ZW58MHx8MHx8fDA%3D",
    inStock: 23,
    competitors: [
      { name: "Competitor A", price: 279.99, inStock: true },
      { name: "Competitor B", price: 249.99, inStock: true },
      { name: "Competitor C", price: 259.99, inStock: true }
    ],
    priceHistory: [
      { date: "2023-06-01", price: 219.99 },
      { date: "2023-07-01", price: 219.99 },
      { date: "2023-08-01", price: 229.99 },
      { date: "2023-09-01", price: 229.99 },
      { date: "2023-10-01", price: 249.99 }
    ]
  },
  {
    id: 5,
    name: "Designer Wristwatch",
    currentPrice: 399.99,
    previousPrice: 399.99,
    suggestedPrice: 429.99,
    category: "Fashion",
    image: "https://images.unsplash.com/photo-1524805444758-089113d48a6d?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8d2F0Y2h8ZW58MHx8MHx8fDA%3D",
    inStock: 15,
    competitors: [
      { name: "Competitor A", price: 449.99, inStock: true },
      { name: "Competitor B", price: 429.99, inStock: false },
      { name: "Competitor C", price: 399.99, inStock: true }
    ],
    priceHistory: [
      { date: "2023-06-01", price: 399.99 },
      { date: "2023-07-01", price: 399.99 },
      { date: "2023-08-01", price: 399.99 },
      { date: "2023-09-01", price: 399.99 },
      { date: "2023-10-01", price: 399.99 }
    ]
  },
  {
    id: 6,
    name: "Premium Coffee Maker",
    currentPrice: 129.99,
    previousPrice: 149.99,
    suggestedPrice: 129.99,
    category: "Kitchen",
    image: "https://images.unsplash.com/photo-1570087407382-74d8e6559a7a?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTB8fGNvZmZlZSUyMG1ha2VyfGVufDB8fDB8fHww",
    inStock: 32,
    competitors: [
      { name: "Competitor A", price: 139.99, inStock: true },
      { name: "Competitor B", price: 129.99, inStock: true },
      { name: "Competitor C", price: 149.99, inStock: true }
    ],
    priceHistory: [
      { date: "2023-06-01", price: 159.99 },
      { date: "2023-07-01", price: 159.99 },
      { date: "2023-08-01", price: 149.99 },
      { date: "2023-09-01", price: 149.99 },
      { date: "2023-10-01", price: 129.99 }
    ]
  }
];

// Categories for filtering
export const categories = [
  "All",
  "Electronics",
  "Photography",
  "Furniture",
  "Fashion",
  "Kitchen"
];

// Price adjustment reasons
export const priceAdjustmentReasons = [
  { id: "competitive", label: "Match Competitor Pricing" },
  { id: "festive", label: "Festive Season Discount" },
  { id: "clearance", label: "Stock Clearance" },
  { id: "demand", label: "High Demand Adjustment" },
  { id: "premium", label: "Premium Positioning" }
];
