import React, { useState, useEffect} from 'react';

function DashboardCards() {
  const [descr, setDescr] = useState("");
  const [amount, setAmount] = useState(0);
  const [transType, setTransType] = useState("");
  const [category, setCategory] = useState("");
  const [dateOfTrans, setDateOfTrans] = useState("");
  const [transactions, setTransactions] = useState([]);
  const today = new Date().toISOString().split('T')[0];
  const totalIncome = transactions
    .filter(t => t.type === 'income')
    .reduce((sum, t) => sum + t.amount, 0);

  const totalExpenses = transactions
    .filter(t => t.type === 'expense')
    .reduce((sum, t) => sum + t.amount, 0);

  const netBalance = totalIncome - totalExpenses;

  function handleDescription(event) { setDescr(event.target.value); }
  function handleAmount(event) { setAmount(event.target.value); }
  function handleTransType(event) { setTransType(event.target.value); }
  function handleCategory(event) { setCategory(event.target.value); }
  function handleDateOfTrans(event) { setDateOfTrans(event.target.value); }
  const fetchTransactions = () => {
        fetch("http://127.0.0.1:8000/api/transactions")
        .then(res => res.json())
        .then(data => setTransactions(data))
        .catch(err => console.error("Error fetching transactions:", err));
    };
  const handleSave = () => console.log("Progress saved to draft");
  const handleSubmit = (e) => {
    e.preventDefault();

    fetch("http://127.0.0.1:8000/api/transactions", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ description: descr, amount: parseFloat(amount), category: category, type: transType, date: dateOfTrans })
    })
    .then(res => {
        if (!res.ok) {
        // If FastAPI sends 422, this prints the exact backend explanation!
        return res.json().then(err => { throw err; });
        }
        return res.json();
    })
    .then((data) => {
        console.log("Success:", data);
        fetchTransactions(); // Refetch DB data to update UI
    })
    .catch((err) => {
        // 👈 PUT IT HERE! This catches network errors or backend crashes.
        console.error("Error submitting transaction:", err);
    });
    };

useEffect(() => {
    fetchTransactions()
  }, []);
  return (
    <div className="dashboard-wrapper">
      
      {/* 1. TOP ROW: Summary Cards Container */}
      <div className="top-row-container">
        
        {/* Left: Total Income */}
        <div className="allDashCards totIn">
          <h2>Total Income</h2>
          <p>£{totalIncome}</p>
        </div>

        {/* Middle: Net Balance (Featured!) */}
        <div className="allDashCards ovrBala">
          <h2>Net Balance</h2>
          <p>£{netBalance}</p>
        </div>

        {/* Right: Total Expenses */}
        <div className="allDashCards totExp">
          <h2>Total Expenses</h2>
          <p>£{totalExpenses}</p>
        </div>

      </div>

{/* 2. BOTTOM ROW: Form Container */}
<div className="bottom-row-container">
  <div className="allDashCards formCard">
    <h2>Add new transaction</h2>
    
    {/* Wrap in <form> */}
    <form onSubmit={handleSubmit}>
      <div className="form-group">
        <label htmlFor="desc-input">Description:</label>
        <input id="desc-input" value={descr} onChange={handleDescription} placeholder='(optional)'/>
      </div>
      
      <div className="form-group">
        <label htmlFor='amount-input'>Amount</label>
        <input id="amount-input" value={amount} onChange={handleAmount} type="number" step="0.01" min="0" placeholder="Amount" required />
      
        <select value={transType} onChange={handleTransType} required>
          <option value="">Select type</option>
          <option value="income">Income</option>
          <option value="expense">Expense</option>
        </select>
      </div>

      <div className="form-group">
        <select value={category} onChange={handleCategory} required>
          <option value="">Select category</option>
          <option value="other">Other</option>
        </select>
        
        <input value={dateOfTrans} onChange={handleDateOfTrans} type="date" max={today} required />
      </div>

      <div className="button-group">
        <button type="button" onClick={handleSave}>Save Progress</button>
        <button type="submit" className="submit-btn">Submit Transaction</button>
      </div>
    </form>

    </div>
    </div>

    </div>
  );
}

export default DashboardCards;