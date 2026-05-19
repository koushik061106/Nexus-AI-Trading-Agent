import { useState, useEffect } from 'react'
import './App.css'

const StatCard = ({ title, value, color }) => {
  return (
    <div className="card">
      <h3>{title}</h3>
      <p className="stat" style={{ color: color }}>{value}</p>
    </div>
  )
}

const TradeRow = ({ time, pair, type, price, status }) => {
  const actionColor = type === 'BUY' ? '#7ee787' : '#da3633';
  return (
    <div className="trade-row">
      <span className="trade-time">{time}</span>
      <span className="trade-pair">{pair}</span>
      <span className="trade-type" style={{ color: actionColor }}>{type}</span>
      <span className="trade-price">{price}</span>
      <span className={`trade-status ${status.toLowerCase()}`}>{status}</span>
    </div>
  )
}

function App() {
  // 1. We start with empty data while React waits for Python
  const [botStatus, setBotStatus] = useState('Connecting...')
  const [tradeStats, setTradeStats] = useState([])
  const [liveTrades, setLiveTrades] = useState([])

  // 2. The Bridge! This runs the exact second the page loads.
  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/data')
      .then(response => response.json()) // Turn the Python response into JSON
      .then(data => {
        // 3. Inject the Python data directly into our React State!
        setBotStatus(data.botStatus)
        setTradeStats(data.stats)
        setLiveTrades(data.recentTrades)
      })
      .catch(error => {
        console.error("Python Server is offline!", error)
        setBotStatus('OFFLINE')
      })
  }, []) // The empty brackets mean "Only run this once when the page loads"

  const toggleBot = () => {
    setBotStatus(botStatus === 'Online' ? 'Paused' : 'Online')
  }

  return (
    <div className="dashboard">
      <header className="header">
        <h1>NEXUS Agentic Ops</h1>
        <div className="header-actions">
          <button className="wallet-btn">Connect Wallet</button>
          <span className={`status ${botStatus.toLowerCase()}`}>{botStatus}</span>
        </div>
      </header>

      {/* 4. We map over the real data that came from Python */}
      <main className="grid">
        {tradeStats.map((item, index) => (
          <StatCard key={index} title={item.title} value={item.value} color={item.color} />
        ))}
      </main>

      <section className="log-section">
        <h2>Live Execution Log</h2>
        <div className="trade-log-container">
          <div className="trade-row header-row">
            <span>Time</span>
            <span>Pair</span>
            <span>Action</span>
            <span>Price</span>
            <span>Status</span>
          </div>
          {/* 5. Map over the live trades from Python */}
          {liveTrades.map((trade, index) => (
            <TradeRow key={index} {...trade} />
          ))}
        </div>
      </section>

      <button className="action-btn" onClick={toggleBot}>
        Toggle System {botStatus === 'Online' ? 'OFF' : 'ON'}
      </button>
    </div>
  )
}

export default App