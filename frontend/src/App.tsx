import { useState, useEffect } from 'react';
import './App.css';

// Direct to local API Gateway
const API_BASE_URL = "http://localhost:8000/api";

function App() {
  const [customers, setCustomers] = useState<any[]>([]);
  const [orders, setOrders] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  // Fetch data
  const fetchData = async () => {
    try {
      setLoading(true);
      const cRes = await fetch(`${API_BASE_URL}/customers`);
      const oRes = await fetch(`${API_BASE_URL}/orders`);
      if (cRes.ok) setCustomers(await cRes.json());
      if (oRes.ok) setOrders(await oRes.json());
    } catch (e) {
      console.error("Connection failed", e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchData(); }, []);

  // Handlers
  const handleCreateCustomer = async () => {
    const name = prompt("Customer Name:", "John Doe");
    if (!name) return;

    await fetch(`${API_BASE_URL}/customers`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, email: `${name.replace(/\s/g, '').toLowerCase()}@example.com` })
    });
    fetchData();
  };

  const handleCreateOrder = async () => {
    if (customers.length === 0) {
      alert("Create a customer first!");
      return;
    }
    const title = prompt("Order Title:", "New Order");
    if (!title) return;

    // Pick random customer for simplicity
    const randomCust = customers[Math.floor(Math.random() * customers.length)];

    await fetch(`${API_BASE_URL}/orders`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ customer_id: randomCust.id, title })
    });
    fetchData();
  };

  return (
    <div className="container">
      <h1>OrderFlow (Local Learning)</h1>

      <div className="stats-grid">
        <div className="card">
          <h2>Customers</h2>
          <p className="count">{customers.length}</p>
          <button onClick={handleCreateCustomer}>Create Customer</button>
        </div>

        <div className="card">
          <h2>Orders</h2>
          <p className="count">{orders.length}</p>
          <button onClick={handleCreateOrder}>Create Order</button>
        </div>
      </div>

      <div style={{ marginTop: '2rem', textAlign: 'left', opacity: 0.7 }}>
        <p>Debug Info:</p>
        <pre>
          Start Backend: {'\n'}
          uvicorn main:app --port 8000 (Gateway){'\n'}
          uvicorn main:app --port 8001 (Customer){'\n'}
          uvicorn main:app --port 8002 (Order)
        </pre>
      </div>
    </div>
  );
}

export default App;
