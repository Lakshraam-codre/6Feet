import React, { useState } from 'react';
import { createMarketPrice, sendBulkAlerts, createFarmer } from '../services/api';
import '../styles/AdminPanel.css';

function AdminPanel() {
  const [activeTab, setActiveTab] = useState('prices');
  const [formData, setFormData] = useState({});
  const [message, setMessage] = useState('');

  const handlePriceSubmit = async (e) => {
    e.preventDefault();
    try {
      await createMarketPrice(formData);
      setMessage('Market price added successfully!');
      setFormData({});
    } catch (error) {
      setMessage('Error adding price: ' + error.message);
    }
  };

  const handleAlertSubmit = async (e) => {
    e.preventDefault();
    try {
      await sendBulkAlerts(formData);
      setMessage('Alert sent to farmers!');
      setFormData({});
    } catch (error) {
      setMessage('Error sending alert: ' + error.message);
    }
  };

  const handleFarmerSubmit = async (e) => {
    e.preventDefault();
    try {
      await createFarmer(formData);
      setMessage('Farmer added successfully!');
      setFormData({});
    } catch (error) {
      setMessage('Error adding farmer: ' + error.message);
    }
  };

  return (
    <div className="admin-panel">
      <h1>Admin Panel</h1>

      <div className="admin-tabs">
        <button
          className={`tab ${activeTab === 'prices' ? 'active' : ''}`}
          onClick={() => setActiveTab('prices')}
        >
          Market Prices
        </button>
        <button
          className={`tab ${activeTab === 'alerts' ? 'active' : ''}`}
          onClick={() => setActiveTab('alerts')}
        >
          Send Alerts
        </button>
        <button
          className={`tab ${activeTab === 'farmers' ? 'active' : ''}`}
          onClick={() => setActiveTab('farmers')}
        >
          Add Farmer
        </button>
      </div>

      {message && (
        <div className={`message ${message.includes('Error') ? 'error' : 'success'}`}>
          {message}
        </div>
      )}

      {activeTab === 'prices' && (
        <form onSubmit={handlePriceSubmit} className="admin-form">
          <h2>Add Market Price</h2>
          <input
            type="text"
            placeholder="Crop name"
            value={formData.crop_name || ''}
            onChange={(e) => setFormData({ ...formData, crop_name: e.target.value })}
            required
          />
          <input
            type="text"
            placeholder="Location"
            value={formData.location || ''}
            onChange={(e) => setFormData({ ...formData, location: e.target.value })}
            required
          />
          <input
            type="number"
            placeholder="Price per kg"
            step="0.01"
            value={formData.price_per_kg || ''}
            onChange={(e) => setFormData({ ...formData, price_per_kg: parseFloat(e.target.value) })}
            required
          />
          <select
            value={formData.demand_level || ''}
            onChange={(e) => setFormData({ ...formData, demand_level: e.target.value })}
            required
          >
            <option value="">Select demand level</option>
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>
          <button type="submit">Add Price</button>
        </form>
      )}

      {activeTab === 'alerts' && (
        <form onSubmit={handleAlertSubmit} className="admin-form">
          <h2>Send Alert to Farmers</h2>
          <input
            type="text"
            placeholder="Alert title"
            value={formData.title || ''}
            onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            required
          />
          <textarea
            placeholder="Alert message"
            value={formData.message || ''}
            onChange={(e) => setFormData({ ...formData, message: e.target.value })}
            required
          />
          <select
            value={formData.alert_type || ''}
            onChange={(e) => setFormData({ ...formData, alert_type: e.target.value })}
            required
          >
            <option value="">Select alert type</option>
            <option value="pest">Pest</option>
            <option value="weather">Weather</option>
            <option value="drought">Drought</option>
            <option value="frost">Frost</option>
            <option value="market">Market</option>
          </select>
          <select
            value={formData.severity || ''}
            onChange={(e) => setFormData({ ...formData, severity: e.target.value })}
            required
          >
            <option value="">Select severity</option>
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
            <option value="critical">Critical</option>
          </select>
          <button type="submit">Send Alert</button>
        </form>
      )}

      {activeTab === 'farmers' && (
        <form onSubmit={handleFarmerSubmit} className="admin-form">
          <h2>Add Farmer</h2>
          <input
            type="tel"
            placeholder="Phone number"
            value={formData.phone_number || ''}
            onChange={(e) => setFormData({ ...formData, phone_number: e.target.value })}
            required
          />
          <input
            type="text"
            placeholder="Name"
            value={formData.name || ''}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
          />
          <input
            type="text"
            placeholder="Location"
            value={formData.location || ''}
            onChange={(e) => setFormData({ ...formData, location: e.target.value })}
          />
          <input
            type="text"
            placeholder="Primary crop"
            value={formData.primary_crop || ''}
            onChange={(e) => setFormData({ ...formData, primary_crop: e.target.value })}
          />
          <button type="submit">Add Farmer</button>
        </form>
      )}
    </div>
  );
}

export default AdminPanel;
