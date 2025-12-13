
import DashboardLayout from '../../core/components/DashboardLayout';
import { useAuth } from '../../core/context/AuthContext';

const Dashboard = () => {
    const { user } = useAuth();

    return (
        <DashboardLayout>
            <div className="px-4 py-6 sm:px-0">
                <div className="border-4 border-dashed border-gray-200 rounded-lg h-96 flex items-center justify-center">
                    <div className="text-center">
                        <h2 className="text-2xl font-bold text-gray-900">Welcome, {user?.username}!</h2>
                        <p className="mt-2 text-gray-600">Select an option from the menu to get started.</p>
                    </div>
                </div>
            </div>
        </DashboardLayout>
    );
};

export default Dashboard;
