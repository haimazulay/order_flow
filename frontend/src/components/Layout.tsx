import { Outlet, NavLink } from 'react-router-dom';
import { LayoutDashboard, ShoppingCart, Package, Users, Factory } from 'lucide-react';

export function Layout() {
    return (
        <div className="layout">
            <nav className="sidebar">
                <h2 style={{ marginBottom: '2rem' }}>OrderFlow</h2>

                <NavLink to="/" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <LayoutDashboard size={20} />
                        <span>Dashboard</span>
                    </div>
                </NavLink>

                <NavLink to="/orders" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <ShoppingCart size={20} />
                        <span>Orders</span>
                    </div>
                </NavLink>

                <NavLink to="/products" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <Package size={20} />
                        <span>Products</span>
                    </div>
                </NavLink>

                <NavLink to="/customers" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <Users size={20} />
                        <span>Customers</span>
                    </div>
                </NavLink>

                <NavLink to="/production" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <Factory size={20} />
                        <span>Production</span>
                    </div>
                </NavLink>
            </nav>

            <main className="main-content">
                <Outlet />
            </main>
        </div>
    );
}
