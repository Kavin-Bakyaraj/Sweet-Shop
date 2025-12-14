import React from 'react';
import { ShoppingCart } from 'lucide-react';

interface Sweet {
    id: string;
    name: string;
    category: string;
    price: number;
    quantity: number;
    image_url?: string;
}

interface SweetCardProps {
    sweet: Sweet;
    onPurchase?: (id: string) => void;
    isAdmin?: boolean;
}

const SweetCard: React.FC<SweetCardProps> = ({ sweet, onPurchase, isAdmin = false }) => {
    return (
        <div className="bg-surface rounded-xl shadow-sm border border-primary-100 overflow-hidden hover:shadow-md transition-shadow duration-300 flex flex-col h-full">
            <div className="h-48 bg-primary-50 flex items-center justify-center relative overflow-hidden group">
                {sweet.image_url ? (
                    <img src={sweet.image_url} alt={sweet.name} className="h-full w-full object-cover transition-transform duration-300 group-hover:scale-105" />
                ) : (
                    <span className="text-4xl" role="img" aria-label="sweet">🍬</span>
                )}
                {/* Overlay for hover effect */}
                <div className="absolute inset-0 bg-black/5 opacity-0 group-hover:opacity-100 transition-opacity" />
            </div>

            <div className="p-5 flex-1 flex flex-col">
                <div className="flex justify-between items-start mb-2">
                    <div>
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-secondary-100 text-secondary-800 mb-2">
                            {sweet.category}
                        </span>
                        <h3 className="text-lg font-bold text-gray-900 font-heading line-clamp-1" title={sweet.name}>
                            {sweet.name}
                        </h3>
                    </div>
                    <p className="text-lg font-bold text-primary-600">
                        ₹{sweet.price.toFixed(2)}
                    </p>
                </div>

                <div className="mt-auto pt-4 flex items-center justify-between border-t border-gray-100">
                    <div className="text-sm text-gray-500">
                        <span className={`font-medium ${sweet.quantity > 0 ? 'text-green-600' : 'text-red-600'}`}>
                            {sweet.quantity > 0 ? `${sweet.quantity} in stock` : 'Out of stock'}
                        </span>
                    </div>

                    {!isAdmin && sweet.quantity > 0 && (
                        <button
                            onClick={() => onPurchase?.(sweet.id)}
                            className="inline-flex items-center px-3 py-1.5 border border-transparent rounded-full shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 transition-colors"
                            title="Buy 1"
                        >
                            <ShoppingCart className="h-4 w-4 mr-1.5" />
                            Buy
                        </button>
                    )}
                </div>
            </div>
        </div>
    );
};

export default SweetCard;
