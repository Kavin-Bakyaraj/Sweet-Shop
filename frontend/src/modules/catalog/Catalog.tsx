import { useState, useEffect } from 'react';
import DashboardLayout from '../../core/components/DashboardLayout';
import SweetCard from './components/SweetCard';
import SearchBar from './components/SearchBar';
import api from '../../core/api/client';
import { useAuth } from '../../core/context/AuthContext';

interface Sweet {
    id: string;
    name: string;
    category: string;
    price: number;
    quantity: number;
    image_url?: string;
}

const Catalog = () => {
    const [sweets, setSweets] = useState<Sweet[]>([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState('');
    const [selectedCategory, setSelectedCategory] = useState('');
    const [categories, setCategories] = useState<string[]>([]);
    const { isAdmin } = useAuth();

    useEffect(() => {
        fetchSweets();
    }, []);

    const fetchSweets = async () => {
        try {
            setLoading(true);
            const response = await api.get('/sweets');
            setSweets(response.data);

            // Extract unique categories
            const uniqueCategories = Array.from(new Set(response.data.map((s: Sweet) => s.category))) as string[];
            setCategories(uniqueCategories);
        } catch (error) {
            console.error('Failed to fetch sweets:', error);
        } finally {
            setLoading(false);
        }
    };

    const handlePurchase = async (id: string) => {
        try {
            await api.post('/orders', {
                items: [
                    { sweet_id: id, quantity: 1 }
                ]
            });
            // Refresh list to show updated stock
            fetchSweets();
            alert('Order placed successfully! Check your profile for details.');
        } catch (error) {
            console.error('Purchase failed:', error);
            alert('Failed to place order. Please try again.');
        }
    };

    const filteredSweets = sweets.filter((sweet) => {
        const matchesSearch = sweet.name.toLowerCase().includes(searchTerm.toLowerCase());
        const matchesCategory = selectedCategory ? sweet.category === selectedCategory : true;
        return matchesSearch && matchesCategory;
    });

    return (
        <DashboardLayout>
            <div className="px-4 sm:px-0">
                <div className="mb-8">
                    <h1 className="text-3xl font-bold text-gray-900 font-heading">Our Sweets</h1>
                    <p className="mt-2 text-gray-600">Browse our delicious collection of handcrafted sweets.</p>
                </div>

                <SearchBar
                    searchTerm={searchTerm}
                    onSearchChange={setSearchTerm}
                    selectedCategory={selectedCategory}
                    onCategoryChange={setSelectedCategory}
                    categories={categories}
                />

                {loading ? (
                    <div className="flex justify-center py-12">
                        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-600"></div>
                    </div>
                ) : (
                    <>
                        {filteredSweets.length === 0 ? (
                            <div className="text-center py-12 bg-surface rounded-xl border border-dashed border-gray-300">
                                <p className="text-gray-500 text-lg">No sweets found matching your criteria.</p>
                                <button
                                    onClick={() => { setSearchTerm(''); setSelectedCategory(''); }}
                                    className="mt-4 text-primary-600 hover:text-primary-700 font-medium"
                                >
                                    Clear filters
                                </button>
                            </div>
                        ) : (
                            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                                {filteredSweets.map((sweet) => (
                                    <SweetCard
                                        key={sweet.id}
                                        sweet={sweet}
                                        onPurchase={handlePurchase}
                                        isAdmin={isAdmin}
                                    />
                                ))}
                            </div>
                        )}
                    </>
                )}
            </div>
        </DashboardLayout>
    );
};

export default Catalog;
