import React from 'react';
import { Edit2, Trash2, PlusCircle } from 'lucide-react';

interface Sweet {
    id: string;
    name: string;
    category: string;
    price: number;
    quantity: number;
    image_url?: string;
}

interface SweetTableProps {
    sweets: Sweet[];
    onEdit: (sweet: Sweet) => void;
    onDelete: (id: string) => void;
    onRestock: (sweet: Sweet) => void;
}

const SweetTable: React.FC<SweetTableProps> = ({ sweets, onEdit, onDelete, onRestock }) => {
    return (
        <div className="bg-surface shadow-sm border border-primary-100 rounded-xl overflow-hidden">
            <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-primary-50">
                        <tr>
                            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-primary-800 uppercase tracking-wider">
                                Image
                            </th>
                            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-primary-800 uppercase tracking-wider">
                                Name
                            </th>
                            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-primary-800 uppercase tracking-wider">
                                Category
                            </th>
                            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-primary-800 uppercase tracking-wider">
                                Price
                            </th>
                            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-primary-800 uppercase tracking-wider">
                                Stock
                            </th>
                            <th scope="col" className="px-6 py-3 text-right text-xs font-medium text-primary-800 uppercase tracking-wider">
                                Actions
                            </th>
                        </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                        {sweets.map((sweet) => (
                            <tr key={sweet.id} className="hover:bg-gray-50 transition-colors">
                                <td className="px-6 py-4 whitespace-nowrap">
                                    <div className="h-10 w-10 rounded-full bg-gray-100 flex items-center justify-center overflow-hidden">
                                        {sweet.image_url ? (
                                            <img src={sweet.image_url} alt={sweet.name} className="h-full w-full object-cover" />
                                        ) : (
                                            <span className="text-lg" role="img" aria-label="sweet">🍬</span>
                                        )}
                                    </div>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap">
                                    <div className="text-sm font-medium text-gray-900">{sweet.name}</div>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap">
                                    <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-secondary-100 text-secondary-800">
                                        {sweet.category}
                                    </span>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                    ₹{sweet.price.toFixed(2)}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap">
                                    <span className={`text-sm font-medium ${sweet.quantity > 10 ? 'text-green-600' : 'text-red-600'}`}>
                                        {sweet.quantity}
                                    </span>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                    <button
                                        onClick={() => onRestock(sweet)}
                                        className="text-green-600 hover:text-green-900 mr-4 transition-colors"
                                        title="Restock"
                                    >
                                        <PlusCircle className="h-4 w-4" />
                                    </button>
                                    <button
                                        onClick={() => onEdit(sweet)}
                                        className="text-primary-600 hover:text-primary-900 mr-4 transition-colors"
                                        title="Edit"
                                    >
                                        <Edit2 className="h-4 w-4" />
                                    </button>
                                    <button
                                        onClick={() => onDelete(sweet.id)}
                                        className="text-red-600 hover:text-red-900 transition-colors"
                                        title="Delete"
                                    >
                                        <Trash2 className="h-4 w-4" />
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
            {sweets.length === 0 && (
                <div className="text-center py-8 text-gray-500">
                    No sweets found. Add some to get started!
                </div>
            )}
        </div>
    );
};

export default SweetTable;
