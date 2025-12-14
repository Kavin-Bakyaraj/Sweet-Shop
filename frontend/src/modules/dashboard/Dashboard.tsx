import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import DashboardLayout from '../../core/components/DashboardLayout';
import { useAuth } from '../../core/context/AuthContext';
import api from '../../core/api/client';
import { ShoppingBag, AlertTriangle, TrendingUp, Package, ArrowRight, User } from 'lucide-react';

interface Sweet {
    id: string;
    name: string;
    category: string;
    price: number;
    quantity: number;
    image_url?: string;
}

const Dashboard = () => {
    const { user, isAdmin } = useAuth();
    const [sweets, setSweets] = useState<Sweet[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await api.get('/sweets');
                setSweets(response.data);
            } catch (error) {
                console.error('Failed to fetch data:', error);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, []);

    const lowStockSweets = sweets.filter(s => s.quantity < 10);
    const featuredSweets = sweets.slice(0, 3); // Just take first 3 for now
    const totalStock = sweets.reduce((acc, s) => acc + s.quantity, 0);
    const totalValue = sweets.reduce((acc, s) => acc + (s.price * s.quantity), 0);

    if (loading) {
        return (
            <DashboardLayout>
                <div className="flex justify-center items-center h-64">
                    <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-600"></div>
                </div>
            </DashboardLayout>
        );
    }

    return (
        <DashboardLayout>
            <div className="px-4 sm:px-0 space-y-8">
                {/* Welcome Section */}
                <div className="bg-gradient-to-r from-primary-600 to-primary-800 rounded-2xl p-8 text-white shadow-lg">
                    <h1 className="text-3xl font-bold font-heading mb-2">Welcome back, {user?.username}! 👋</h1>
                    <p className="text-primary-100 text-lg">Here's what's happening in your sweet shop today.</p>
                </div>

                {/* Stats Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                        <div className="flex items-center justify-between mb-4">
                            <div className="p-3 bg-orange-50 text-orange-600 rounded-lg">
                                <Package className="h-6 w-6" />
                            </div>
                            <span className="text-sm font-medium text-gray-500">Total Products</span>
                        </div>
                        <h3 className="text-2xl font-bold text-gray-900">{sweets.length}</h3>
                    </div>

                    <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                        <div className="flex items-center justify-between mb-4">
                            <div className="p-3 bg-green-50 text-green-600 rounded-lg">
                                <ShoppingBag className="h-6 w-6" />
                            </div>
                            <span className="text-sm font-medium text-gray-500">Total Stock</span>
                        </div>
                        <h3 className="text-2xl font-bold text-gray-900">{totalStock}</h3>
                    </div>

                    {isAdmin && (
                        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                            <div className="flex items-center justify-between mb-4">
                                <div className="p-3 bg-red-50 text-red-600 rounded-lg">
                                    <AlertTriangle className="h-6 w-6" />
                                </div>
                                <span className="text-sm font-medium text-gray-500">Low Stock Alerts</span>
                            </div>
                            <h3 className="text-2xl font-bold text-gray-900">{lowStockSweets.length}</h3>
                        </div>
                    )}

                    <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                        <div className="flex items-center justify-between mb-4">
                            <div className="p-3 bg-amber-50 text-amber-600 rounded-lg">
                                <TrendingUp className="h-6 w-6" />
                            </div>
                            <span className="text-sm font-medium text-gray-500">Inventory Value</span>
                        </div>
                        <h3 className="text-2xl font-bold text-gray-900">₹{totalValue.toFixed(2)}</h3>
                    </div>
                </div>
                {/* Alerts Section (Full Width) */}
                {isAdmin && lowStockSweets.length > 0 && (
                    <div className="bg-red-50 border border-red-200 rounded-xl p-4 flex items-center justify-between">
                        <div className="flex items-center">
                            <AlertTriangle className="h-5 w-5 text-red-600 mr-3" />
                            <div>
                                <h3 className="font-bold text-red-900">Low Stock Alert</h3>
                                <p className="text-sm text-red-700">
                                    {lowStockSweets.length} items are running low on stock.
                                </p>
                            </div>
                        </div>
                        <Link
                            to="/admin"
                            className="text-sm bg-white border border-red-200 text-red-700 px-4 py-2 rounded-lg hover:bg-red-50 transition-colors font-medium shadow-sm"
                        >
                            Manage Inventory
                        </Link>
                    </div>
                )}

                {/* Quick Actions (Horizontal Row) */}
                <div>
                    <h2 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h2>
                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
                        <Link to="/catalog" className="flex flex-col items-center justify-center p-6 bg-white rounded-xl shadow-sm border border-gray-100 hover:border-primary-200 hover:shadow-md transition-all group">
                            <div className="p-3 bg-primary-50 text-primary-600 rounded-full mb-3 group-hover:scale-110 transition-transform">
                                <ShoppingBag className="h-6 w-6" />
                            </div>
                            <span className="font-medium text-gray-900">Browse Catalog</span>
                        </Link>

                        <Link to="/profile" className="flex flex-col items-center justify-center p-6 bg-white rounded-xl shadow-sm border border-gray-100 hover:border-primary-200 hover:shadow-md transition-all group">
                            <div className="p-3 bg-green-50 text-green-600 rounded-full mb-3 group-hover:scale-110 transition-transform">
                                <User className="h-6 w-6" />
                            </div>
                            <span className="font-medium text-gray-900">View Profile</span>
                        </Link>

                        {isAdmin && (
                            <>
                                <Link to="/admin" className="flex flex-col items-center justify-center p-6 bg-white rounded-xl shadow-sm border border-gray-100 hover:border-primary-200 hover:shadow-md transition-all group">
                                    <div className="p-3 bg-purple-50 text-purple-600 rounded-full mb-3 group-hover:scale-110 transition-transform">
                                        <Package className="h-6 w-6" />
                                    </div>
                                    <span className="font-medium text-gray-900">Manage Stock</span>
                                </Link>
                                <Link to="/admin" className="flex flex-col items-center justify-center p-6 bg-white rounded-xl shadow-sm border border-gray-100 hover:border-primary-200 hover:shadow-md transition-all group">
                                    <div className="p-3 bg-orange-50 text-orange-600 rounded-full mb-3 group-hover:scale-110 transition-transform">
                                        <TrendingUp className="h-6 w-6" />
                                    </div>
                                    <span className="font-medium text-gray-900">View Reports</span>
                                </Link>
                            </>
                        )}
                    </div>
                </div>

                {/* Featured Sweets (Full Width Grid) */}
                <div>
                    <div className="flex items-center justify-between mb-6">
                        <h2 className="text-xl font-bold text-gray-900 font-heading">Featured Sweets</h2>
                        <Link to="/catalog" className="text-primary-600 hover:text-primary-700 font-medium flex items-center text-sm">
                            View Full Catalog <ArrowRight className="ml-1 h-4 w-4" />
                        </Link>
                    </div>
                    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                        {featuredSweets.map(sweet => (
                            <div key={sweet.id} className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-md transition-shadow group">
                                <div className="h-48 bg-gray-100 relative overflow-hidden">
                                    {sweet.image_url ? (
                                        <img src={sweet.image_url} alt={sweet.name} className="h-full w-full object-cover group-hover:scale-105 transition-transform duration-300" />
                                    ) : (
                                        <div className="h-full w-full flex items-center justify-center text-4xl">🍬</div>
                                    )}
                                </div>
                                <div className="p-4">
                                    <h3 className="font-bold text-gray-900 mb-1">{sweet.name}</h3>
                                    <div className="flex items-center justify-between">
                                        <span className="text-primary-600 font-bold">₹{sweet.price}</span>
                                        <span className={`text-xs px-2 py-1 rounded-full font-medium ${sweet.quantity > 0 ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                                            {sweet.quantity > 0 ? 'In Stock' : 'Out of Stock'}
                                        </span>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </DashboardLayout>
    );
};

export default Dashboard;
