import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area } from 'recharts';
import { Terminal, Activity, BrainCircuit, BarChart2, List, Settings, TrendingUp, ShieldAlert, Cpu } from 'lucide-react';

// --- MOCK DATA FOR UI ---
const mockChartData = [
  { time: '09:30', price: 150.2 }, { time: '10:00', price: 151.5 },
  { time: '10:30', price: 149.8 }, { time: '11:00', price: 152.1 },
  { time: '11:30', price: 153.4 }, { time: '12:00', price: 152.9 },
  { time: '12:30', price: 155.0 }
];

const mockOrderBook = {
  asks: [[155.5, 120], [155.4, 300], [155.2, 150], [155.1, 80]],
  bids: [[154.9, 200], [154.8, 450], [154.5, 100], [154.2, 320]]
};

const mockOrderHistory = [
  { id: 'ORD-8921', time: '12:31:08', pair: 'AAPL/USD', type: 'BUY', size: 150, price: 155.00, status: 'FILLED' },
  { id: 'ORD-8920', time: '11:14:22', pair: 'TSLA/USD', type: 'SELL', size: 50, price: 202.50, status: 'FILLED' },
  { id: 'ORD-8919', time: '10:05:11', pair: 'MSFT/USD', type: 'BUY', size: 100, price: 410.20, status: 'FILLED' },
];

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  
  // --- THE BRIDGE: Backend Connection State ---
  const [isEngineLive, setIsEngineLive] = useState(false);
  const [netPnl, setNetPnl] = useState(1240.50);

  useEffect(() => {
    const fetchLiveData = async () => {
      try {
        const response = await fetch('https://nexus-ai-trading-agent.onrender.com/api/data');
        if (response.ok) {
          const data = await response.json();
          setIsEngineLive(true);
          setNetPnl(data.net_pnl);
        } else {
          setIsEngineLive(false);
        }
      } catch (error) {
        setIsEngineLive(false);
      }
    };

    fetchLiveData();
    const interval = setInterval(fetchLiveData, 10000);
    return () => clearInterval(interval);
  }, []);
  // --------------------------------------------

  // --- VIEWS ---
  const renderDashboard = () => (
    <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr 1.5fr', gap: '20px', height: '100%' }}>
      {/* COLUMN 1: CHARTING */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
        <div style={{ backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '8px', padding: '15px', flex: 1 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '15px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: '#94a3b8' }}>
              <TrendingUp size={18} color="#38bdf8" />
              <h2 style={{ margin: 0, fontSize: '14px', color: '#f8fafc' }}>NIFTY 50 / INR</h2>
            </div>
            <span style={{ fontSize: '18px', fontWeight: 'bold', color: '#f8fafc' }}>$₹2,950.00</span>
          </div>
          <ResponsiveContainer width="100%" height="85%">
            <AreaChart data={mockChartData}>
              <defs>
                <linearGradient id="colorPrice" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#38bdf8" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#38bdf8" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" vertical={false} />
              <XAxis dataKey="time" stroke="#94a3b8" tick={{ fontSize: 12 }} />
              <YAxis domain={['dataMin - 2', 'dataMax + 2']} stroke="#94a3b8" tick={{ fontSize: 12 }} />
              <Tooltip contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #38bdf8', borderRadius: '4px' }} />
              <Area type="monotone" dataKey="price" stroke="#38bdf8" fillOpacity={1} fill="url(#colorPrice)" strokeWidth={2} />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* COLUMN 2: ORDER BOOK */}
      <div style={{ backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '8px', padding: '15px', display: 'flex', flexDirection: 'column' }}>
        <h2 style={{ margin: '0 0 15px 0', fontSize: '14px', color: '#94a3b8', borderBottom: '1px solid #334155', paddingBottom: '10px' }}>ORDER BOOK</h2>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '4px', marginBottom: '10px' }}>
          {mockOrderBook.asks.map((ask, i) => (
            <div key={i} style={{ display: 'flex', justifyContent: 'space-between', fontSize: '13px', color: '#ef4444' }}>
              <span>{ask[0].toFixed(2)}</span>
              <span style={{ color: '#cbd5e1' }}>{ask[1]}</span>
            </div>
          ))}
        </div>
        <div style={{ textAlign: 'center', padding: '8px 0', borderTop: '1px solid #334155', borderBottom: '1px solid #334155', margin: '5px 0', color: '#38bdf8', fontSize: '14px', fontWeight: 'bold' }}>
          155.00
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '4px', marginTop: '10px' }}>
          {mockOrderBook.bids.map((bid, i) => (
            <div key={i} style={{ display: 'flex', justifyContent: 'space-between', fontSize: '13px', color: '#4ade80' }}>
              <span>{bid[0].toFixed(2)}</span>
              <span style={{ color: '#cbd5e1' }}>{bid[1]}</span>
            </div>
          ))}
        </div>
      </div>

      {/* COLUMN 3: AI AGENT TELEMETRY */}
      <div style={{ backgroundColor: '#000000', border: '1px solid #334155', borderRadius: '8px', padding: '15px', overflowY: 'auto' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', borderBottom: '1px solid #334155', paddingBottom: '10px', marginBottom: '15px' }}>
          <Terminal color="#a855f7" size={16} />
          <h2 style={{ margin: 0, fontSize: '14px', color: '#a855f7' }}>AGENT TELEMETRY LOG</h2>
        </div>
        <div style={{ fontSize: '12px', lineHeight: '1.7', color: '#cbd5e1' }}>
          <p><span style={{ color: '#64748b' }}>[{new Date().toLocaleTimeString()}]</span> <span style={{ color: '#eab308' }}>[SYSTEM]</span> Connection established with Render backend.</p>
          <p><span style={{ color: '#64748b' }}>[12:31:04]</span> <span style={{ color: '#eab308' }}>[SCAN]</span> Ingesting market data for 50 tickers...</p>
          <p><span style={{ color: '#64748b' }}>[12:31:05]</span> <span style={{ color: '#38bdf8' }}>[ANALYSIS]</span> Groq Llama-3 parsing sentiment from recent news events.</p>
          <p><span style={{ color: '#64748b' }}>[12:31:06]</span> <span style={{ color: '#4ade80' }}>[SIGNAL]</span> Strong Bullish divergence detected on AAPL (Confidence: 87%).</p>
          <p><span style={{ color: '#64748b' }}>[12:31:07]</span> <span style={{ color: '#a855f7' }}>[EXECUTION]</span> Routing BUY order to broker. Size: 150 shares.</p>
          <p><span style={{ color: '#64748b' }}>[12:31:08]</span> <span style={{ color: '#4ade80' }}>[SUCCESS]</span> Order filled at $155.00.</p>
        </div>
      </div>
    </div>
  );

  const renderOrders = () => (
    <div style={{ backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '8px', padding: '20px', height: '100%' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '20px' }}>
        <List color="#38bdf8" />
        <h2 style={{ margin: 0, color: '#f8fafc', fontSize: '18px' }}>ORDER LEDGER</h2>
      </div>
      <table style={{ width: '100%', textAlign: 'left', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ borderBottom: '1px solid #334155', color: '#94a3b8', fontSize: '14px' }}>
            <th style={{ padding: '10px 0' }}>ORDER ID</th>
            <th>TIME</th>
            <th>PAIR</th>
            <th>TYPE</th>
            <th>SIZE</th>
            <th>PRICE</th>
            <th>STATUS</th>
          </tr>
        </thead>
        <tbody>
          {mockOrderHistory.map((order, i) => (
            <tr key={i} style={{ borderBottom: '1px solid #334155', color: '#cbd5e1', fontSize: '14px' }}>
              <td style={{ padding: '12px 0' }}>{order.id}</td>
              <td>{order.time}</td>
              <td style={{ fontWeight: 'bold' }}>{order.pair}</td>
              <td style={{ color: order.type === 'BUY' ? '#4ade80' : '#ef4444', fontWeight: 'bold' }}>{order.type}</td>
              <td>{order.size}</td>
              <td>₹{order.price.toFixed(2)}</td>
              <td><span style={{ backgroundColor: 'rgba(74, 222, 128, 0.2)', color: '#4ade80', padding: '4px 8px', borderRadius: '4px', fontSize: '12px' }}>{order.status}</span></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );

  const renderLogs = () => (
    <div style={{ backgroundColor: '#000000', border: '1px solid #334155', borderRadius: '8px', padding: '20px', height: '100%', overflowY: 'auto' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '20px', borderBottom: '1px solid #334155', paddingBottom: '15px' }}>
        <Cpu color="#a855f7" />
        <h2 style={{ margin: 0, color: '#a855f7', fontSize: '18px' }}>FULL SYSTEM DIAGNOSTICS</h2>
      </div>
      <div style={{ fontSize: '14px', lineHeight: '1.8', color: '#cbd5e1', fontFamily: 'monospace' }}>
        <p><span style={{ color: '#64748b' }}>[08:00:00]</span> <span style={{ color: '#38bdf8' }}>[INIT]</span> Nexus Quantitative Terminal booting...</p>
        <p><span style={{ color: '#64748b' }}>[08:00:02]</span> <span style={{ color: '#4ade80' }}>[AUTH]</span> Connection to Kotak Neo API successful.</p>
        <p><span style={{ color: '#64748b' }}>[08:00:05]</span> <span style={{ color: '#4ade80' }}>[AUTH]</span> Groq Llama-3 neural engine loaded.</p>
        <p><span style={{ color: '#64748b' }}>[08:15:00]</span> <span style={{ color: '#eab308' }}>[SCAN]</span> Market open detected. Commencing sector rotation analysis.</p>
        <p><span style={{ color: '#64748b' }}>[09:30:00]</span> <span style={{ color: '#a855f7' }}>[AI_THOUGHT]</span> Evaluating high volatility in tech sector. Applying momentum strategy.</p>
        <p><span style={{ color: '#64748b' }}>[12:31:08]</span> <span style={{ color: '#4ade80' }}>[EXECUTION]</span> Buy order AAPL filled. Monitoring trailing stop loss.</p>
        <div className="animate-pulse mt-4 text-slate-500">_ waiting for next signal...</div>
      </div>
    </div>
  );

  const renderSettings = () => (
    <div style={{ backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '8px', padding: '20px', height: '100%', maxWidth: '800px' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '30px' }}>
        <Settings color="#94a3b8" />
        <h2 style={{ margin: 0, color: '#f8fafc', fontSize: '18px' }}>ENGINE CONFIGURATION</h2>
      </div>
      
      <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
          <label style={{ color: '#94a3b8', fontSize: '12px' }}>API STATUS</label>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', backgroundColor: '#0f172a', padding: '10px 15px', borderRadius: '6px', border: '1px solid #334155' }}>
            <div style={{ width: '8px', height: '8px', borderRadius: '50%', backgroundColor: '#4ade80' }}></div>
            <span style={{ color: '#cbd5e1', fontSize: '14px' }}>Connected to Kotak Neo</span>
          </div>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
          <label style={{ color: '#94a3b8', fontSize: '12px' }}>RISK PARAMETERS</label>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px' }}>
            <div style={{ backgroundColor: '#0f172a', padding: '15px', borderRadius: '6px', border: '1px solid #334155' }}>
              <p style={{ margin: '0 0 5px 0', color: '#64748b', fontSize: '12px' }}>Max Position Size</p>
              <p style={{ margin: 0, color: '#f8fafc', fontSize: '16px' }}>₹50,000</p>
            </div>
            <div style={{ backgroundColor: '#0f172a', padding: '15px', borderRadius: '6px', border: '1px solid #334155' }}>
              <p style={{ margin: '0 0 5px 0', color: '#64748b', fontSize: '12px' }}>Daily Stop Loss</p>
              <p style={{ margin: 0, color: '#ef4444', fontSize: '16px' }}>2.5%</p>
            </div>
          </div>
        </div>
        
        <button style={{ marginTop: '20px', padding: '12px', backgroundColor: '#38bdf8', color: '#0f172a', border: 'none', borderRadius: '6px', fontWeight: 'bold', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px' }}>
          <ShieldAlert size={16} />
          UPDATE PARAMETERS
        </button>
      </div>
    </div>
  );

  // --- MAIN RENDER ---
  return (
    <div style={{ backgroundColor: '#0f172a', color: '#e2e8f0', height: '100vh', display: 'flex', fontFamily: 'monospace', overflow: 'hidden' }}>
      
      {/* SIDEBAR NAVIGATION */}
      <div style={{ width: '80px', backgroundColor: '#1e293b', borderRight: '1px solid #334155', display: 'flex', flexDirection: 'column', alignItems: 'center', padding: '20px 0', gap: '30px', zIndex: 10 }}>
        <BrainCircuit color="#38bdf8" size={32} />
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px', marginTop: '20px' }}>
          <NavIcon icon={<Activity />} active={activeTab === 'dashboard'} onClick={() => setActiveTab('dashboard')} tooltip="Dashboard" />
          <NavIcon icon={<List />} active={activeTab === 'orders'} onClick={() => setActiveTab('orders')} tooltip="Order Ledger" />
          <NavIcon icon={<Terminal />} active={activeTab === 'logs'} onClick={() => setActiveTab('logs')} tooltip="System Logs" />
          <NavIcon icon={<Settings />} active={activeTab === 'settings'} onClick={() => setActiveTab('settings')} tooltip="Configuration" />
        </div>
      </div>

      {/* MAIN WORKSPACE */}
      <div style={{ flex: 1, padding: '20px', display: 'flex', flexDirection: 'column', gap: '20px', overflowY: 'auto' }}>
        
        {/* TOP BAR */}
        <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid #334155', paddingBottom: '15px' }}>
          <h1 style={{ margin: 0, fontSize: '22px', color: '#f8fafc', letterSpacing: '1px' }}>
            NEXUS <span style={{ color: '#38bdf8' }}>//</span> QUANTITATIVE TERMINAL
          </h1>
          <div style={{ display: 'flex', gap: '15px', alignItems: 'center' }}>
            <div style={{ textAlign: 'right' }}>
              <p style={{ margin: 0, fontSize: '12px', color: '#94a3b8' }}>NET PNL</p>
              <p style={{ margin: 0, fontSize: '18px', color: '#4ade80', fontWeight: 'bold' }}>
              +₹{netPnl.toFixed(2)}
              </p>
            </div>
            
            <span style={{ 
              backgroundColor: isEngineLive ? 'rgba(74, 222, 128, 0.15)' : 'rgba(239, 68, 68, 0.15)', 
              color: isEngineLive ? '#4ade80' : '#ef4444', 
              border: `1px solid ${isEngineLive ? '#22c55e' : '#ef4444'}`, 
              padding: '6px 12px', 
              borderRadius: '4px', 
              fontSize: '13px', 
              fontWeight: 'bold',
              transition: 'all 0.3s ease'
            }}>
              {isEngineLive ? '● ENGINE LIVE' : '○ ENGINE OFFLINE'}
            </span>
          </div>
        </header>

        {/* DYNAMIC CONTENT AREA */}
        <div style={{ flex: 1, overflow: 'hidden' }}>
          {activeTab === 'dashboard' && renderDashboard()}
          {activeTab === 'orders' && renderOrders()}
          {activeTab === 'logs' && renderLogs()}
          {activeTab === 'settings' && renderSettings()}
        </div>
        
      </div>
    </div>
  );
}

// Helper component for Sidebar icons
function NavIcon({ icon, active, onClick, tooltip }) {
  return (
    <div
      onClick={onClick}
      title={tooltip}
      style={{
        cursor: 'pointer',
        padding: '12px',
        borderRadius: '8px',
        backgroundColor: active ? '#334155' : 'transparent',
        color: active ? '#38bdf8' : '#64748b',
        transition: 'all 0.2s ease-in-out',
        boxShadow: active ? '0 0 10px rgba(56, 189, 248, 0.2)' : 'none'
      }}
    >
      {React.cloneElement(icon, { size: 24, color: active ? '#38bdf8' : '#64748b' })}
    </div>
  );
}