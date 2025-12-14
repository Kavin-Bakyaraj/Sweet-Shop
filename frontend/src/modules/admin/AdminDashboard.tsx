import React, { useState, useEffect } from 'react';
import DashboardLayout from '../../core/components/DashboardLayout';
import SweetTable from './components/SweetTable';
import SweetForm from './components/SweetForm';
import RestockForm from './components/RestockForm';
import api from '../../core/api/client';
import { Plus } from 'lucide-react';

interface Sweet {
    id: string;
    name: string;
    category: string;
    price: number;
    quantity: number;
    image_url?: string;
}

const AdminDashboard = () => {
    const [sweets, setSweets] = useState<Sweet[]>([]);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [isRestockModalOpen, setIsRestockModalOpen] = useState(false);
    const [editingSweet, setEditingSweet] = useState<Sweet | null>(null);
    const [restockSweet, setRestockSweet] = useState<Sweet | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');

    useEffect(() => {
        fetchSweets();
    }, []);

    const fetchSweets = async () => {
        try {
            const response = await api.get('/sweets');
            setSweets(response.data);
        } catch (err) {
            console.error('Failed to fetch sweets:', err);
            setError('Failed to load sweets');
        }
    };

    const handleAddClick = () => {
        setEditingSweet(null);
        setIsModalOpen(true);
    };

    const handleEditClick = (sweet: Sweet) => {
        setEditingSweet(sweet);
        setIsModalOpen(true);
    };

    const handleDeleteClick = async (id: string) => {
        if (window.confirm('Are you sure you want to delete this sweet?')) {
            try {
                await api.delete(`/admin/sweets/${id}`);
                fetchSweets();
            } catch (err) {
                console.error('Failed to delete sweet:', err);
                alert('Failed to delete sweet');
            }
        }
    };

    const handleFormSubmit = async (data: Omit<Sweet, 'id'>) => {
        setIsLoading(true);
        try {
            if (editingSweet) {
                await api.put(`/admin/sweets/${editingSweet.id}`, data);
            } else {
                await api.post('/admin/sweets', data);
            }
            setIsModalOpen(false);
            fetchSweets();
        } catch (err) {
            console.error('Failed to save sweet:', err);
            alert('Failed to save sweet');
        } finally {
            setIsLoading(false);
        }
    };

    const handleRestockClick = (sweet: Sweet) => {
        setRestockSweet(sweet);
        setIsRestockModalOpen(true);
    };

    const handleRestockSubmit = async (quantity: number) => {
        if (!restockSweet) return;
        setIsLoading(true);
        try {
            await api.post(`/inventory/sweets/${restockSweet.id}/restock`, { quantity });
            setIsRestockModalOpen(false);
            fetchSweets();
        } catch (err) {
            console.error('Failed to restock sweet:', err);
            alert('Failed to restock sweet');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <DashboardLayout>
            <div className="px-4 sm:px-0">
                <div className="flex justify-between items-center mb-8">
                    <div>
                        <h1 className="text-3xl font-bold text-gray-900 font-heading">Admin Dashboard</h1>
                        <p className="mt-2 text-gray-600">Manage your sweet inventory.</p>
                    </div>
                    <button
                        onClick={handleAddClick}
                        className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 transition-colors"
                    >
                        <Plus className="h-5 w-5 mr-2" />
                        Add Sweet
                    </button>
                </div>

                {error && (
                    <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-lg mb-6">
                        {error}
                    </div>
                )}

                <SweetTable
                    sweets={sweets}
                    onEdit={handleEditClick}
                    onDelete={handleDeleteClick}
                    onRestock={handleRestockClick}
                />

                {isModalOpen && (
                    <SweetForm
                        initialData={editingSweet}
                        onSubmit={handleFormSubmit}
                        onCancel={() => setIsModalOpen(false)}
                        isLoading={isLoading}
                    />
                )}

                {isRestockModalOpen && restockSweet && (
                    <RestockForm
                        sweetName={restockSweet.name}
                        onSubmit={handleRestockSubmit}
                        onCancel={() => setIsRestockModalOpen(false)}
                        isLoading={isLoading}
                    />
                )}
            </div>
        </DashboardLayout>
    );
};

export default AdminDashboard;
