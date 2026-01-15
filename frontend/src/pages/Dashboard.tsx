import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { RefreshCw, Plus, AlertCircle, Clock, XCircle, ShoppingCart } from 'lucide-react';
import { API_BASE_URL } from '../config';

interface DashboardStats {
    orders_count: number;
    urgent_orders: number;
    late_shipments: number;
    revenue: number;
    rejects_24h?: number;
}

interface ActivityItem {
    id: string;
    label: string;
    ts: string;
}

export function Dashboard() {
    const navigate = useNavigate();
    const [stats, setStats] = useState<DashboardStats | null>(null);
    const [loading, setLoading] = useState(true);
    const [refreshing, setRefreshing] = useState(false);
    const [activity, setActivity] = useState<ActivityItem[]>([]);

    const fetchDashboardData = async () => {
        try {
            setRefreshing(true);

            // Parallel fetch for stats and activity
            const [statsRes, activityRes] = await Promise.all([
                fetch(`${API_BASE_URL}/dashboard/overview`).then(r => r.ok ? r.json() : null),
                // Mock activity fetch or real endpoint if exists
                Promise.resolve([
                    { id: "1", label: "Order OF-2026-1024 moved to PACKED", ts: "2m ago" },
                    { id: "2", label: "New customer registered: Acme Corp", ts: "15m ago" },
                    { id: "3", label: "Work task completed: PACK (Station PACKING-2)", ts: "1h ago" }
                ])
            ]);

            if (statsRes) setStats(statsRes);
            if (activityRes) setActivity(activityRes);

        } catch (e) {
            console.error("Dashboard fetch failed", e);
        } finally {
            setLoading(false);
            setRefreshing(false);
        }
    };

    useEffect(() => {
        fetchDashboardData();
    }, []);

    const handleRefresh = () => {
        if (refreshing) return;
        fetchDashboardData();
    };

    const handleNewOrder = () => {
        // Logic to open modal (passed from parent or context, for now alert)
        // Implementation of Modal will follow
        window.dispatchEvent(new CustomEvent('open-new-order-modal'));
    };

    return (
        <div>
            <header style={{ marginBottom: '2rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                    <h1>Dashboard Overview</h1>
                    {/* Environment Badge Mock */}
                    <span style={{
                        fontSize: '0.75rem',
                        background: 'rgba(34, 197, 94, 0.2)',
                        color: '#22c55e',
                        padding: '2px 8px',
                        borderRadius: '4px',
                        border: '1px solid rgba(34, 197, 94, 0.3)'
                    }}>DEV</span>
                </div>

                <div style={{ display: 'flex', gap: '1rem' }}>
                    <button className="btn secondary" onClick={handleRefresh} disabled={refreshing} style={{ display: 'flex', alignItems: 'center', gap: '8px', background: 'transparent', border: '1px solid var(--glass-border)' }}>
                        <RefreshCw size={16} className={refreshing ? 'spin' : ''} />
                        Refresh
                    </button>
                    <button className="btn" onClick={handleNewOrder} style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <Plus size={16} />
                        New Order
                    </button>
                </div>
            </header>

            {loading && !stats ? (
                <div>Loading analytics...</div>
            ) : (
                <div className="grid">
                    {/* Total Orders */}
                    <div className="card clickable" onClick={() => navigate('/orders')}>
                        <h3 style={{ display: 'flex', justifyContent: 'space-between' }}>
                            Total Orders
                            <ShoppingCart size={20} color="var(--text-secondary)" />
                        </h3>
                        <div className="stat-value">{stats?.orders_count ?? 0}</div>
                        <div style={{ color: 'var(--success-color)' }}>+12% from last week</div>
                    </div>

                    {/* Urgent Orders */}
                    <div className="card clickable" onClick={() => navigate('/orders?priority=URGENT')}>
                        <h3 style={{ display: 'flex', justifyContent: 'space-between' }}>
                            Urgent Attention
                            <AlertCircle size={20} color="var(--warning-color)" />
                        </h3>
                        <div className="stat-value" style={{ color: 'var(--warning-color)' }}>{stats?.urgent_orders ?? 0}</div>
                        <div style={{ color: 'var(--text-secondary)' }}>Orders pending action</div>
                    </div>

                    {/* Revenue */}
                    <div className="card clickable" onClick={() => navigate('/analytics')}>
                        <h3 style={{ display: 'flex', justifyContent: 'space-between' }}>
                            Revenue
                            <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>YTD</span>
                        </h3>
                        <div className="stat-value">
                            ${stats?.revenue?.toLocaleString() ?? "—"}
                        </div>
                        <div style={{ color: 'var(--success-color)' }}>On track</div>
                    </div>

                    {/* Late Shipments */}
                    <div className="card clickable" onClick={() => navigate('/production?late=true')}>
                        <h3 style={{ display: 'flex', justifyContent: 'space-between' }}>
                            Late Shipments
                            <Clock size={20} color="var(--danger-color)" />
                        </h3>
                        <div className="stat-value" style={{ color: 'var(--danger-color)' }}>
                            {stats?.late_shipments ?? 0}
                        </div>
                        <div style={{ color: 'var(--text-secondary)' }}>Delayed deliveries</div>
                    </div>

                    {/* Alerts Panel - Conceptual */}
                    {/* Right now merging alerts into recent activity visually or separately? 
                User spec asked for "Alerts Panel" vs "Recent Activity". 
                I will put them side-by-side or stacked in the grid.
            */}

                    {/* Recent Activity */}
                    <div className="card" style={{ gridColumn: 'span 2' }}>
                        <h3>Recent Activity</h3>
                        <ul style={{ listStyle: 'none', padding: 0, marginTop: '1rem', color: 'var(--text-secondary)' }}>
                            {activity.map(item => (
                                <li key={item.id} style={{ padding: '0.75rem 0', borderBottom: '1px solid var(--glass-border)', display: 'flex', justifyContent: 'space-between' }}>
                                    <span>{item.label}</span>
                                    <span style={{ fontSize: '0.85rem', opacity: 0.7 }}>{item.ts}</span>
                                </li>
                            ))}
                        </ul>
                    </div>

                    {/* Alerts List Mock */}
                    <div className="card">
                        <h3>Operational Alerts</h3>
                        <ul style={{ listStyle: 'none', padding: 0, marginTop: '1rem' }}>
                            <li style={{ padding: '0.5rem 0', display: 'flex', gap: '0.5rem', alignItems: 'center', color: 'var(--warning-color)' }}>
                                <AlertCircle size={16} />
                                <span>2 Urgent orders pending</span>
                            </li>
                            <li style={{ padding: '0.5rem 0', display: 'flex', gap: '0.5rem', alignItems: 'center', color: 'var(--danger-color)' }}>
                                <XCircle size={16} />
                                <span>1 Rejected work order</span>
                            </li>
                        </ul>
                    </div>

                </div>
            )}
        </div>
    );
}
