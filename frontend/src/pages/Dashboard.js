import React, { useState, useEffect } from 'react';
import { getStatistics, getFarmers, getMarketPrices } from '../services/api';
import '../styles/Dashboard.css';

function Dashboard() {
  const [stats, setStats] = useState(null);
  const [farmers, setFarmers] = useState([]);
  const [prices, setPrices] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      const [statsRes, farmersRes, pricesRes] = await Promise.all([
        getStatistics(),
        getFarmers(0, 10),
        getMarketPrices(),
      ]);

      setStats(statsRes.data);
      setFarmers(farmersRes.data);
      setPrices(pricesRes.data);
    } catch (error) {
      console.error('Error loading dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading dashboard...</div>;
  }

  return (
    <div className="dashboard">
      <h1>Dashboard</h1>

      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Farmers</h3>
          <p className="stat-value">{stats?.total_farmers || 0}</p>
        </div>
        <div className="stat-card">
          <h3>Interactions</h3>
          <p className="stat-value">{stats?.total_interactions || 0}</p>
        </div>
        <div className="stat-card">
          <h3>Alerts Sent</h3>
          <p className="stat-value">{stats?.total_alerts_sent || 0}</p>
        </div>
        <div className="stat-card">
          <h3>Market Prices</h3>
          <p className="stat-value">{stats?.market_prices || 0}</p>
        </div>
      </div>

      <div className="dashboard-section">
        <h2>Recent Farmers</h2>
        <table className="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Phone</th>
              <th>Location</th>
              <th>Crop</th>
              <th>Experience</th>
            </tr>
          </thead>
          <tbody>
            {farmers.map((farmer) => (
              <tr key={farmer.id}>
                <td>{farmer.id}</td>
                <td>{farmer.phone_number}</td>
                <td>{farmer.location || 'N/A'}</td>
                <td>{farmer.primary_crop || 'N/A'}</td>
                <td>{farmer.farming_experience}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="dashboard-section">
        <h2>Market Prices</h2>
        <table className="data-table">
          <thead>
            <tr>
              <th>Crop</th>
              <th>Location</th>
              <th>Price (LSL/kg)</th>
              <th>Demand</th>
              <th>Updated</th>
            </tr>
          </thead>
          <tbody>
            {prices.map((price) => (
              <tr key={price.id}>
                <td>{price.crop_name}</td>
                <td>{price.location}</td>
                <td>M{price.price_per_kg.toFixed(2)}</td>
                <td>{price.demand_level}</td>
                <td>{new Date(price.last_updated).toLocaleDateString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Dashboard;
