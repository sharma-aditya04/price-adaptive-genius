
import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { LogIn } from 'lucide-react';

const Navbar = () => {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-white/90 backdrop-blur-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex-shrink-0 flex items-center">
            <Link to="/" className="text-xl font-bold text-gray-900 flex items-center">
              <span className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-2 py-1 rounded mr-2">PAG</span>
              Price Adaptive Genius
            </Link>
          </div>
          
          <div className="flex items-center space-x-4">
            <Link to="/login">
              <Button variant="outline" size="sm" className="flex items-center gap-1">
                <LogIn className="h-4 w-4" />
                <span>Login</span>
              </Button>
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
