import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { LogOut, User, LayoutDashboard, ShoppingBag, Shield } from 'lucide-react';

interface DashboardLayoutProps {
    children: React.ReactNode;
}

const DashboardLayout: React.FC<DashboardLayoutProps> = ({ children }) => {
    const { user, logout, isAdmin } = useAuth();
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    return (
        <div className="min-h-screen bg-background">
            {/* Navbar */}
            <nav className="bg-surface border-b border-primary-100 shadow-sm">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex justify-between h-16">
                        <div className="flex">
                            <div className="flex-shrink-0 flex items-center">
                                <h1 className="text-2xl font-bold text-primary-600 font-heading">Sweet Shop</h1>
                            </div>
                            <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                                <Link to="/dashboard" className="border-transparent text-gray-500 hover:border-primary-300 hover:text-primary-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors">
                                    <LayoutDashboard className="w-4 h-4 mr-2" />
                                    Dashboard
                                </Link>
                                <Link to="/catalog" className="border-transparent text-gray-500 hover:border-primary-300 hover:text-primary-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors">
                                    <ShoppingBag className="w-4 h-4 mr-2" />
                                    Catalog
                                </Link>
                                {isAdmin && (
                                    <Link to="/admin" className="border-transparent text-gray-500 hover:border-primary-300 hover:text-primary-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors">
                                        <Shield className="w-4 h-4 mr-2" />
                                        Admin
                                    </Link>
                                )}
                            </div>
                        </div>
                        <div className="flex items-center">
                            <div className="flex-shrink-0">
                                <div className="flex items-center space-x-4">
                                    <div className="flex items-center text-sm text-gray-600">
                                        <User className="w-4 h-4 mr-2" />
                                        <span className="font-medium">{user?.username}</span>
                                    </div>
                                    <button
                                        onClick={handleLogout}
                                        className="relative inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 shadow-sm hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 transition-colors"
                                    >
                                        <LogOut className="w-4 h-4 mr-2" />
                                        Logout
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </nav>

            {/* Main Content */}
            <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
                {children}
            </main>
        </div>
    );
};

export default DashboardLayout;
