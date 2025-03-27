
import React, { useState } from 'react';
import { Menu, X, Bell, Search } from 'lucide-react';

const Navbar: React.FC = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <nav className="bg-white/80 backdrop-blur-md border-b border-gray-200 fixed w-full z-10 transition-all duration-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <div className="flex-shrink-0 flex items-center">
              <span className="text-xl font-semibold bg-clip-text text-transparent bg-gradient-to-r from-gray-800 to-gray-600">
                PriceOptimize
              </span>
            </div>
          </div>

          {/* Desktop menu */}
          <div className="hidden md:flex items-center space-x-4">
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Search className="h-4 w-4 text-gray-400" />
              </div>
              <input
                type="text"
                className="block w-full pl-10 pr-3 py-2 border border-gray-200 rounded-md leading-5 bg-white/50 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-0 focus:ring-gray-300 focus:border-gray-300 transition duration-150 ease-in-out text-sm"
                placeholder="Search products..."
              />
            </div>
            <button className="p-2 rounded-full text-gray-600 hover:text-gray-800 hover:bg-gray-100 transition duration-150 ease-in-out">
              <Bell className="h-5 w-5" />
            </button>
            <button className="p-2 rounded-full bg-gray-100 text-gray-700 hover:bg-gray-200 transition duration-150 ease-in-out">
              <span className="flex items-center font-medium">Admin</span>
            </button>
          </div>

          {/* Mobile menu button */}
          <div className="flex md:hidden items-center">
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="inline-flex items-center justify-center p-2 rounded-md text-gray-600 hover:text-gray-800 hover:bg-gray-100 transition duration-150 ease-in-out"
            >
              {isMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile menu */}
      <div className={`md:hidden ${isMenuOpen ? 'block' : 'hidden'}`}>
        <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 bg-white/80 backdrop-blur-md animate-fade-in">
          <div className="px-4 py-2">
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Search className="h-4 w-4 text-gray-400" />
              </div>
              <input
                type="text"
                className="block w-full pl-10 pr-3 py-2 border border-gray-200 rounded-md leading-5 bg-white/50 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-0 focus:ring-gray-300 focus:border-gray-300 transition duration-150 ease-in-out text-sm"
                placeholder="Search products..."
              />
            </div>
          </div>
          <button className="w-full text-left block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-100 transition duration-150 ease-in-out">
            Notifications
          </button>
          <button className="w-full text-left block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-100 transition duration-150 ease-in-out">
            Profile
          </button>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
