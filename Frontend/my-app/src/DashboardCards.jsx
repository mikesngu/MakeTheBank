import React, { useState } from 'react';

function DashboardCards() {
  const [descr, setDescr] = useState("");
  const [amount, setAmount] = useState(0);
  const [transType, setTransType] = useState("");
  const [category, setCategory] = useState("");
  const [dateOfTrans, setDateOfTrans] = useState("");

  function handleDescription(event) { setDescr(event.target.value); }
  function handleAmount(event) { setAmount(event.target.value); }
  function handleTransType(event) { setTransType(event.target.value); }
  function handleCategory(event) { setCategory(event.target.value); }
  function handleDateOfTrans(event) { setDateOfTrans(event.target.value); }

  const handleSave = () => console.log("Progress saved to draft");
  const handleSubmit = () => console.log("Transaction successfully submitted");

  return (
    <div className="dashboard-wrapper">
      
      {/* 1. TOP ROW: Summary Cards Container */}
      <div className="top-row-container">
        
        {/* Left: Total Income */}
        <div className="allDashCards totIn">
          <h2>Total Income</h2>
          <p>£500</p>
        </div>

        {/* Middle: Net Balance (Featured!) */}
        <div className="allDashCards ovrBala">
          <h2>Net Balance</h2>
          <p>£440</p>
        </div>

        {/* Right: Total Expenses */}
        <div className="allDashCards totExp">
          <h2>Total Expenses</h2>
          <p>£60</p>
        </div>

      </div>

      {/* 2. BOTTOM ROW: Form Container */}
      <div className="bottom-row-container">
        <div className="allDashCards formCard">
          <h2>Add new transaction</h2>
          
          <div className="form-group">
            <label htmlFor="desc-input">Description:</label>
            <input id="desc-input" value={descr} onChange={handleDescription} placeholder='(optional)'/>
          </div>
          
          <div className="form-group">
            <label htmlFor='amount-input'>Amount</label>
            <input id="amount-input" value={amount} onChange={handleAmount} type="number" step="0.01" min="0" placeholder="Amount"/>
          

          
            <select value={transType} onChange={handleTransType}>
              <option value="">Select type</option>
              <option value="income">Income</option>
              <option value="expense">Expense</option>
            </select>
        </div>
         <div className="form-group">
            <select value={category} onChange={handleCategory}>
              <option value="">Select category</option>
              <option value="other">Other</option>
            </select>
            
            <input value={dateOfTrans} onChange={handleDateOfTrans} type="date" />
          </div>

          <div className="button-group">
            <button onClick={handleSave}>Save Progress</button>
            <button onClick={handleSubmit} className="submit-btn">Submit Transaction</button>
          </div>
        </div>
      </div>

    </div>
  );
}

export default DashboardCards;