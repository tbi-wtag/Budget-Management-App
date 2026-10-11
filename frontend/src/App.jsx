import { useEffect, useState } from 'react';
import { 
  getCategories, 
  getTransactions, 
  createCategory, 
  deleteCategory,
  createTransaction, 
  deleteTransaction, 
  getSummary 
} from './api';

function App() {
  const [categories, setCategories] = useState([]);
  const [transactions, setTransactions] = useState([]);
  const [summary, setSummary] = useState({ total_income: 0, total_expenses: 0, balance: 0 });

  // Form states
  const [catName, setCatName] = useState('');
  const [catType, setCatType] = useState('expense');

  const [amount, setAmount] = useState('');
  const [description, setDescription] = useState('');
  const [selectedCatId, setSelectedCatId] = useState('');

  const currentMonth = new Date().toISOString().slice(0, 7);

  const loadData = async () => {
    try {
      const [catRes, txRes, sumRes] = await Promise.all([
        getCategories(),
        getTransactions(),
        getSummary(currentMonth).catch(() => ({ data: { total_income: 0, total_expenses: 0, balance: 0 } }))
      ]);

      setCategories(catRes.data);
      setTransactions(txRes.data);
      setSummary(sumRes.data);

      if (catRes.data.length > 0) {
        if (!selectedCatId || !catRes.data.some(c => c.id === selectedCatId)) {
          setSelectedCatId(catRes.data[0].id);
        }
      } else {
        setSelectedCatId('');
      }
    } catch (err) {
      console.error('Error fetching data:', err);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleAddCategory = async (e) => {
    e.preventDefault();
    if (!catName.trim()) {
      alert('Please enter a category name');
      return;
    }
    try {
      const res = await createCategory({ name: catName, type: catType });
      setCatName('');
      if (!selectedCatId) setSelectedCatId(res.data.id);
      await loadData();
    } catch (err) {
      alert('Failed to add category: ' + (err.response?.data?.detail || err.message));
    }
  };

  const handleDeleteCategory = async (id) => {
    if (!window.confirm('Delete this category? (Associated transactions might be affected)')) return;
    try {
      await deleteCategory(id);
      await loadData();
    } catch (err) {
      alert('Failed to delete category: ' + (err.response?.data?.detail || err.message));
    }
  };

  const handleAddTransaction = async (e) => {
    e.preventDefault();
    if (!amount || !selectedCatId) {
      alert('Please select a category and enter an amount');
      return;
    }

    const category = categories.find((c) => c.id === selectedCatId);

    try {
      await createTransaction({
        amount: parseFloat(amount),
        description: description,
        category_id: selectedCatId,
        type: category ? category.type : 'expense',
      });

      setAmount('');
      setDescription('');
      await loadData();
    } catch (err) {
      alert('Failed to add transaction: ' + (err.response?.data?.detail || err.message));
    }
  };

  const handleDeleteTransaction = async (id) => {
    try {
      await deleteTransaction(id);
      await loadData();
    } catch (err) {
      alert('Failed to delete transaction: ' + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <div style={styles.container}>
      <header style={styles.header}>
        <h1 style={styles.title}>Budget Tracker</h1>
      </header>

      {/* Summary Row */}
      <div style={styles.summaryGrid}>
        <div style={styles.summaryCard}>
          <span style={styles.summaryLabel}>INCOME</span>
          <span style={{ ...styles.summaryVal, color: '#22c55e' }}>+Rs{summary.total_income || 0}</span>
        </div>
        <div style={styles.summaryCard}>
          <span style={styles.summaryLabel}>EXPENSES</span>
          <span style={{ ...styles.summaryVal, color: '#ef4444' }}>-Rs{summary.total_expenses || 0}</span>
        </div>
        <div style={styles.summaryCard}>
          <span style={styles.summaryLabel}>BALANCE</span>
          <span style={{ ...styles.summaryVal, color: '#3b82f6' }}>Rs{summary.balance || 0}</span>
        </div>
      </div>

      {/* Add Category */}
      <div style={styles.card}>
        <h2 style={styles.cardTitle}>Add Category</h2>
        <form onSubmit={handleAddCategory} style={styles.formGroup}>
          <input
            type="text"
            placeholder="Category Name"
            value={catName}
            onChange={(e) => setCatName(e.target.value)}
            style={styles.darkInput}
          />
          <select
            value={catType}
            onChange={(e) => setCatType(e.target.value)}
            style={styles.whiteSelect}
          >
            <option value="expense">Expense</option>
            <option value="income">Income</option>
          </select>
          <button type="submit" style={styles.blueButton}>Add Category</button>
        </form>

        {/* Categories Pills / Badges */}
        <div style={{ marginTop: '16px', display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
          {categories.map((c) => (
            <span key={c.id} style={styles.categoryChip}>
              {c.name} ({c.type})
              <button
                onClick={() => handleDeleteCategory(c.id)}
                style={styles.chipDeleteBtn}
                title="Delete Category"
              >
                ✕
              </button>
            </span>
          ))}
        </div>
      </div>

      {/* Add Transaction */}
      <div style={styles.card}>
        <h2 style={styles.cardTitle}>Add Transaction</h2>
        <form onSubmit={handleAddTransaction} style={styles.formGroup}>
          <input
            type="number"
            step="0.01"
            placeholder="Amount"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            style={{ ...styles.darkInput, maxWidth: '120px' }}
          />
          <input
            type="text"
            placeholder="Description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            style={styles.darkInput}
          />
          <select
            value={selectedCatId}
            onChange={(e) => setSelectedCatId(e.target.value)}
            style={styles.whiteSelect}
          >
            {categories.length === 0 ? (
              <option value="">No categories</option>
            ) : (
              categories.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.name}
                </option>
              ))
            )}
          </select>
          <button type="submit" style={styles.blueButton}>Add Transaction</button>
        </form>
      </div>

      {/* Transactions List */}
      <div style={styles.card}>
        <h2 style={styles.cardTitle}>Transactions</h2>
        {transactions.length === 0 ? (
          <p style={{ color: '#6b7280', textAlign: 'center', fontSize: '14px', margin: '20px 0' }}>
            No transactions added yet.
          </p>
        ) : (
          <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
            {transactions.map((t) => (
              <li key={t.id} style={styles.listItem}>
                <div>
                  <div style={{ fontWeight: '500', fontSize: '15px', color: '#111827' }}>
                    {t.description || 'No description'}
                  </div>
                  <span style={styles.categoryBadge}>
                    {t.category ? t.category.name : 'Uncategorized'}
                  </span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                  <span style={{
                    fontWeight: '600',
                    fontSize: '15px',
                    color: t.type === 'income' ? '#16a34a' : '#dc2626'
                  }}>
                    {t.type === 'income' ? '+' : '-'}${t.amount}
                  </span>
                  <button
                    onClick={() => handleDeleteTransaction(t.id)}
                    style={styles.deleteBtn}
                    title="Delete transaction"
                  >
                    ✕
                  </button>
                </div>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

const styles = {
  container: {
    maxWidth: '650px',
    margin: '0 auto',
    padding: '40px 20px',
  },
  header: {
    textAlign: 'center',
    marginBottom: '24px',
    paddingBottom: '12px',
    borderBottom: '1px solid #2d3748',
  },
  title: {
    margin: 0,
    fontSize: '28px',
    fontWeight: '700',
    color: '#ffffff',
  },
  summaryGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(3, 1fr)',
    gap: '12px',
    marginBottom: '20px',
  },
  summaryCard: {
    backgroundColor: '#ffffff',
    borderRadius: '10px',
    padding: '16px',
    textAlign: 'center',
    boxShadow: '0 2px 8px rgba(0,0,0,0.2)',
  },
  summaryLabel: {
    fontSize: '12px',
    color: '#6b7280',
    fontWeight: '600',
    letterSpacing: '0.5px',
  },
  summaryVal: {
    display: 'block',
    fontSize: '20px',
    fontWeight: '700',
    marginTop: '6px',
  },
  card: {
    backgroundColor: '#ffffff',
    borderRadius: '10px',
    padding: '24px',
    marginBottom: '20px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.2)',
  },
  cardTitle: {
    fontSize: '16px',
    fontWeight: '700',
    marginTop: 0,
    marginBottom: '16px',
    color: '#111827',
    textAlign: 'center',
  },
  formGroup: {
    display: 'flex',
    gap: '10px',
    alignItems: 'center',
  },
  darkInput: {
    flex: 1,
    padding: '10px 14px',
    borderRadius: '6px',
    border: 'none',
    backgroundColor: '#374151',
    color: '#ffffff',
    fontSize: '14px',
    outline: 'none',
  },
  whiteSelect: {
    padding: '10px 14px',
    borderRadius: '6px',
    border: '1px solid #d1d5db',
    backgroundColor: '#ffffff',
    color: '#111827',
    fontSize: '14px',
    outline: 'none',
    minWidth: '90px',
  },
  blueButton: {
    padding: '10px 18px',
    borderRadius: '6px',
    border: 'none',
    backgroundColor: '#2563eb',
    color: '#ffffff',
    fontWeight: '600',
    fontSize: '14px',
    cursor: 'pointer',
    whiteSpace: 'nowrap',
  },
  listItem: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '12px 0',
    borderBottom: '1px solid #e5e7eb',
  },
  categoryBadge: {
    display: 'inline-block',
    marginTop: '4px',
    fontSize: '12px',
    padding: '2px 8px',
    backgroundColor: '#f3f4f6',
    color: '#4b5563',
    borderRadius: '12px',
  },
  categoryChip: {
    display: 'inline-flex',
    alignItems: 'center',
    gap: '6px',
    padding: '4px 10px',
    backgroundColor: '#374151',
    color: '#ffffff',
    borderRadius: '16px',
    fontSize: '12px',
    fontWeight: '500',
  },
  chipDeleteBtn: {
    border: 'none',
    background: 'none',
    color: '#ef4444',
    cursor: 'pointer',
    padding: 0,
    fontSize: '11px',
    fontWeight: 'bold',
  },
  deleteBtn: {
    border: 'none',
    backgroundColor: '#fee2e2',
    color: '#ef4444',
    borderRadius: '50%',
    width: '24px',
    height: '24px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    cursor: 'pointer',
    fontSize: '12px',
    fontWeight: 'bold',
  },
};

export default App;