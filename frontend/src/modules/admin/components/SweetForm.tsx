import React, { useState, useEffect } from 'react';
import { X, Upload } from 'lucide-react';
import api from '../../../core/api/client';

interface Sweet {
    id?: string;
    name: string;
    category: string;
    price: number;
    quantity: number;
    image_url?: string;
}

interface SweetFormProps {
    initialData?: Sweet | null;
    onSubmit: (data: Omit<Sweet, 'id'>) => Promise<void>;
    onCancel: () => void;
    isLoading: boolean;
}

const SweetForm: React.FC<SweetFormProps> = ({ initialData, onSubmit, onCancel, isLoading }) => {
    const [formData, setFormData] = useState({
        name: '',
        category: '',
        price: '',
        quantity: '',
        image_url: ''
    });

    useEffect(() => {
        if (initialData) {
            setFormData({
                name: initialData.name,
                category: initialData.category,
                price: initialData.price.toString(),
                quantity: initialData.quantity.toString(),
                image_url: initialData.image_url || ''
            });
        }
    }, [initialData]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        await onSubmit({
            name: formData.name,
            category: formData.category,
            className="w-full inline-flex justify-center rounded-lg border border-transparent shadow-sm px-4 py-2.5 bg-primary-600 text-base font-medium text-white hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 sm:col-start-2 sm:text-sm disabled:opacity-70 transition-colors"
            >
            { isLoading? 'Saving...': 'Save Sweet' }
                                </button >
    <button
        type="button"
        onClick={onCancel}
        className="mt-3 w-full inline-flex justify-center rounded-lg border border-gray-300 shadow-sm px-4 py-2.5 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 sm:mt-0 sm:col-start-1 sm:text-sm transition-colors"
    >
        Cancel
    </button>
                            </div >
                        </form >
                    </div >
                </div >
            </div >
        </div >
    );
};

export default SweetForm;
