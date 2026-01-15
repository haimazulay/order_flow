import { useState, useEffect } from 'react'
import { API_BASE_URL } from "./config";
import './App.css'

interface DashboardStats {
  orders_count: number;
  urgent_orders: number;
  late_shipments: number;
  revenue: number;
}

function App() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await fetch(`${API_BASE_URL}/dashboard/overview`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data: DashboardStats = await res.json();
        setStats(data);
      } catch (e) {
        console.error("Failed to load dashboard stats:", e);
        setStats(null);
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);


  return (
    <div className="layout">
      <nav className="sidebar">
        <h2>OrderFlow</h2>
        <div className="nav-item active">Dashboard</div>
        <div className="nav-item">Orders</div>
        <div className="nav-item">Products</div>
        <div className="nav-item">Customers</div>
        <div className="nav-item">Production</div>
      </nav>

      <button className="btn" onClick={() => alert("click works!")}>
        Test Click
      </button>

      <main className="main-content">
        <header style={{ marginBottom: '2rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h1>Dashboard Overview</h1>
          <button className="btn" onClick={() => alert("New Order functionality coming soon!")}>New Order</button>
        </header>

        {loading ? (
          <div>Loading analytics...</div>
        ) : (
          <div className="grid">
            <div className="card">
              <h3>Total Orders</h3>
              <div className="stat-value">{stats?.orders_count}</div>
              <div style={{ color: 'var(--success-color)' }}>+12% from last week</div>
            </div>

            <div className="card">
              <h3>Urgent Attention</h3>
              <div className="stat-value" style={{ color: 'var(--warning-color)' }}>{stats?.urgent_orders}</div>
              <div style={{ color: 'var(--text-secondary)' }}>Orders pending action</div>
            </div>

            <div className="card">
              <h3>Revenue</h3>
              <div className="stat-value">
                ${stats ? stats.revenue.toLocaleString() : "—"}
              </div>
              <div>YTD</div>
            </div>

            <div className="card">
              <h3>Late Shipments</h3>
              <div className="stat-value" style={{ color: 'var(--danger-color)' }}>
                {stats?.late_shipments ?? "—"}
              </div>
              <div style={{ color: 'var(--text-secondary)' }}>Delayed deliveries</div>
            </div>

            <div className="card" style={{ gridColumn: 'span 2' }}>
              <h3>Recent Activity</h3>
              <ul style={{ listStyle: 'none', padding: 0, marginTop: '1rem', color: 'var(--text-secondary)' }}>
                <li style={{ padding: '0.5rem 0', borderBottom: '1px solid var(--glass-border)' }}>
                  Order #OF-2026-1024 deployed to PRODUCTION
                </li>
                <li style={{ padding: '0.5rem 0', borderBottom: '1px solid var(--glass-border)' }}>
                  New customer registered: Acme Corp
                </li>
                <li style={{ padding: '0.5rem 0' }}>
                  Product "Widget X" low on stock
                </li>
              </ul>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

export default App
