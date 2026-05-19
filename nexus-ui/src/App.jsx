import React, { useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area } from 'recharts';
import { Terminal, Activity, BrainCircuit, BarChart2, List, Settings, TrendingUp } from 'lucide-react';

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

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');

  return (
    <div style={{ backgroundColor: '#0f172a', color: '#e2e8f0', height: '100vh', display: 'flex', fontFamily: 'monospace', overflow: 'hidden' }}>

      {/* SIDEBAR NAVIGATION */}
      <div style={{ width: '80px', backgroundColor: '#1e293b', borderRight: '1px solid #334155', display: 'flex', flexDirection: 'column', alignItems: 'center', padding: '20px 0', gap: '30px' }}>
        <BrainCircuit color="#38bdf8" size={32} />
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px', marginTop: '20px' }}>
          <NavIcon icon={<Activity />} active={activeTab === 'dashboard'} onClick={() => setActiveTab('dashboard')} />
          <NavIcon icon={<List />} active={activeTab === 'orders'} onClick={() => setActiveTab('orders')} />
          <NavIcon icon={<Terminal />} active={activeTab === 'logs'} onClick={() => setActiveTab('logs')} />
          <NavIcon icon={<Settings />} active={activeTab === 'settings'} onClick={() => setActiveTab('settings')} />
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
              <p style={{ margin: 0, fontSize: '18px', color: '#4ade80', fontWeight: 'bold' }}>+$1,240.50</p>
            </div>
            <span style={{ backgroundColor: 'rgba(22, 101, 52, 0.3)', color: '#4ade80', border: '1px solid #166534', padding: '6px 12px', borderRadius: '4px', fontSize: '13px', fontWeight: 'bold' }}>
              ● ENGINE LIVE
            </span>
          </div>
        </header>

        {/* 3-COLUMN GRID LAYOUT */}
        <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr 1.5fr', gap: '20px', height: '100%' }}>

          {/* COLUMN 1: CHARTING */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
            <div style={{ backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '8px', padding: '15px', flex: 1 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '15px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: '#94a3b8' }}>
                  <TrendingUp size={18} color="#38bdf8" />
                  <h2 style={{ margin: 0, fontSize: '14px', color: '#f8fafc' }}>AAPL / USD</h2>
                </div>
                <span style={{ fontSize: '18px', fontWeight: 'bold', color: '#f8fafc' }}>$155.00</span>
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

            {/* Asks (Selling) */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '4px', marginBottom: '10px' }}>
              {mockOrderBook.asks.map((ask, i) => (
                <div key={i} style={{ display: 'flex', justifyContent: 'space-between', fontSize: '13px', color: '#ef4444' }}>
                  <span>{ask[0].toFixed(2)}</span>
                  <span style={{ color: '#cbd5e1' }}>{ask[1]}</span>
                </div>
              ))}
            </div>

            {/* Spread */}
            <div style={{ textAlign: 'center', padding: '8px 0', borderTop: '1px solid #334155', borderBottom: '1px solid #334155', margin: '5px 0', color: '#38bdf8', fontSize: '14px', fontWeight: 'bold' }}>
              155.00
            </div>

            {/* Bids (Buying) */}
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
              <p><span style={{ color: '#64748b' }}>[12:31:04]</span> <span style={{ color: '#eab308' }}>[SCAN]</span> Ingesting market data for 50 tickers...</p>
              <p><span style={{ color: '#64748b' }}>[12:31:05]</span> <span style={{ color: '#38bdf8' }}>[ANALYSIS]</span> Groq Llama-3 parsing sentiment from recent news events.</p>
              <p><span style={{ color: '#64748b' }}>[12:31:06]</span> <span style={{ color: '#4ade80' }}>[SIGNAL]</span> Strong Bullish divergence detected on AAPL (Confidence: 87%).</p>
              <p><span style={{ color: '#64748b' }}>[12:31:07]</span> <span style={{ color: '#a855f7' }}>[EXECUTION]</span> Routing BUY order to Alpaca. Size: 150 shares.</p>
              <p><span style={{ color: '#64748b' }}>[12:31:08]</span> <span style={{ color: '#4ade80' }}>[SUCCESS]</span> Order filled at $155.00.</p>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}

// Helper component for Sidebar icons
function NavIcon({ icon, active, onClick }) {
  return (
    <div
      onClick={onClick}
      style={{
        cursor: 'pointer',
        padding: '10px',
        borderRadius: '8px',
        backgroundColor: active ? '#334155' : 'transparent',
        color: active ? '#38bdf8' : '#64748b',
        transition: 'all 0.2s'
      }}
    >
      {React.cloneElement(icon, { size: 24, color: active ? '#38bdf8' : '#64748b' })}
    </div>
  );
}