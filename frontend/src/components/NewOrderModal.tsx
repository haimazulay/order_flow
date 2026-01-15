import { useState } from 'react';
import { X } from 'lucide-react';

interface NewOrderModalProps {
    isOpen: boolean;
    onClose: () => void;
}

export function NewOrderModal({ isOpen, onClose }: NewOrderModalProps) {
    const [customerSearch, setCustomerSearch] = useState('');
    const [productSearch, setProductSearch] = useState('');
    const [quantity, setQuantity] = useState(1);
    const [priority, setPriority] = useState('NORMAL');
    const [isSubmitting, setIsSubmitting] = useState(false);

    if (!isOpen) return null;

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsSubmitting(true);

        // Simulate API call
        await new Promise(r => setTimeout(r, 1000));

        alert("Order Created! (Mock)");
        setIsSubmitting(false);
        onClose();
        // In real app, trigger dashboard refresh via context or event
    };

    return (
        <div className="modal-overlay" style={{
            position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
            backgroundColor: 'rgba(0,0,0,0.7)', backdropFilter: 'blur(4px)',
            display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000
        }}>
            <div className="modal-content" style={{
                background: '#1e1e2e', width: '500px', borderRadius: '12px',
                border: '1px solid var(--glass-border)', padding: '2rem',
                boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)'
            }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1.5rem' }}>
                    <h2>New Order</h2>
                    <button onClick={onClose} style={{ background: 'transparent', border: 'none', color: '#fff', cursor: 'pointer' }}>
                        <X size={24} />
                    </button>
                </div>

                <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>

                    <div className="form-group">
                        <label style={{ display: 'block', marginBottom: '0.5rem', color: '#a1a1aa' }}>Customer</label>
                        <input
                            type="text"
                            placeholder="Search customer..."
                            value={customerSearch}
                            onChange={e => setCustomerSearch(e.target.value)}
                            style={{ width: '100%', padding: '0.75rem', borderRadius: '6px', border: '1px solid #3f3f46', background: '#27272a', color: '#fff' }}
                            required
                        />
                    </div>

                    <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '1rem' }}>
                        <div className="form-group">
                            <label style={{ display: 'block', marginBottom: '0.5rem', color: '#a1a1aa' }}>Product</label>
                            <input
                                type="text"
                                placeholder="Search product..."
                                value={productSearch}
                                onChange={e => setProductSearch(e.target.value)}
                                style={{ width: '100%', padding: '0.75rem', borderRadius: '6px', border: '1px solid #3f3f46', background: '#27272a', color: '#fff' }}
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label style={{ display: 'block', marginBottom: '0.5rem', color: '#a1a1aa' }}>Quantity</label>
                            <input
                                type="number"
                                min="1"
                                value={quantity}
                                onChange={e => setQuantity(parseInt(e.target.value))}
                                style={{ width: '100%', padding: '0.75rem', borderRadius: '6px', border: '1px solid #3f3f46', background: '#27272a', color: '#fff' }}
                                required
                            />
                        </div>
                    </div>

                    <div className="form-group">
                        <label style={{ display: 'block', marginBottom: '0.5rem', color: '#a1a1aa' }}>Priority</label>
                        <select
                            value={priority}
                            onChange={e => setPriority(e.target.value)}
                            style={{ width: '100%', padding: '0.75rem', borderRadius: '6px', border: '1px solid #3f3f46', background: '#27272a', color: '#fff' }}
                        >
                            <option value="NORMAL">Normal</option>
                            <option value="HIGH">High</option>
                            <option value="URGENT">Urgent</option>
                        </select>
                    </div>

                    <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '1rem', marginTop: '1rem' }}>
                        <button type="button" onClick={onClose} style={{ padding: '0.75rem 1.5rem', borderRadius: '8px', background: 'transparent', border: '1px solid #3f3f46', color: '#fff', cursor: 'pointer' }}>
                            Cancel
                        </button>
                        <button type="submit" className="btn" disabled={isSubmitting}>
                            {isSubmitting ? 'Creating...' : 'Create Order'}
                        </button>
                    </div>

                </form>
            </div>
        </div>
    );
}
