// frontend/src/App.js

import { useState, useEffect } from "react";

const BACKEND = "http://localhost:8000";

function App() {
  const [alerts, setAlerts] = useState([]);
  const [tracked, setTracked] = useState([]);

  // Poll backend every second for alerts and tracked persons
  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        // Fetch alerts
        const alertRes = await fetch(`${BACKEND}/alerts`);
        const alertData = await alertRes.json();
        setAlerts(alertData.alerts);

        // Fetch tracked persons
        const trackRes = await fetch(`${BACKEND}/tracked`);
        const trackData = await trackRes.json();
        setTracked(trackData.tracked);
      } catch (err) {
        console.log("Backend not reachable");
      }
    }, 1000);

    // Cleanup interval when component unmounts
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={styles.app}>
      {/* Header */}
      <div style={styles.header}>
        <h1 style={styles.title}>🛡️ VisionGuard AI</h1>
        <p style={styles.subtitle}>Real-time Workplace Safety Monitoring</p>
      </div>

      {/* Main dashboard */}
      <div style={styles.dashboard}>

        {/* Left: Live video feed */}
        <div style={styles.videoPanel}>
          <h2 style={styles.panelTitle}>📹 Live Feed</h2>
          <img
            src={`${BACKEND}/video`}
            alt="Live detection feed"
            style={styles.videoFeed}
          />
        </div>

        {/* Right: Alerts + Tracked */}
        <div style={styles.sidePanel}>

          {/* Alerts panel */}
          <div style={styles.panel}>
            <h2 style={styles.panelTitle}>
              🚨 Active Alerts
              {alerts.length > 0 && (
                <span style={styles.alertBadge}>{alerts.length}</span>
              )}
            </h2>
            {alerts.length === 0 ? (
              <p style={styles.safeText}>✅ All clear — no violations</p>
            ) : (
              alerts.map((alert) => (
                <div key={alert.track_id} style={styles.alertCard}>
                  <p style={styles.alertTitle}>⚠️ Person #{alert.track_id}</p>
                  <p style={styles.alertDetail}>{alert.violation}</p>
                  <p style={styles.alertTimer}>
                    Duration: {alert.duration_seconds}s
                  </p>
                </div>
              ))
            )}
          </div>

          {/* Tracked persons panel */}
          <div style={styles.panel}>
            <h2 style={styles.panelTitle}>
              👥 Tracked Persons
              <span style={styles.countBadge}>{tracked.length}</span>
            </h2>
            {tracked.length === 0 ? (
              <p style={styles.safeText}>No persons in frame</p>
            ) : (
              tracked.map((obj) => (
                <div key={obj.track_id} style={styles.trackedCard}>
                  <p style={styles.trackedTitle}>
                    Person #{obj.track_id}
                  </p>
                  <p style={styles.trackedDetail}>
                    Confidence: {(obj.confidence * 100).toFixed(0)}%
                  </p>
                </div>
              ))
            )}
          </div>

        </div>
      </div>
    </div>
  );
}

// Styles
const styles = {
  app: {
    backgroundColor: "#0f172a",
    minHeight: "100vh",
    color: "#f1f5f9",
    fontFamily: "'Segoe UI', sans-serif",
    padding: "0",
  },
  header: {
    backgroundColor: "#1e293b",
    padding: "16px 32px",
    borderBottom: "1px solid #334155",
  },
  title: {
    margin: 0,
    fontSize: "24px",
    color: "#f1f5f9",
  },
  subtitle: {
    margin: "4px 0 0 0",
    fontSize: "13px",
    color: "#94a3b8",
  },
  dashboard: {
    display: "flex",
    gap: "16px",
    padding: "16px",
    height: "calc(100vh - 80px)",
  },
  videoPanel: {
    flex: 2,
    backgroundColor: "#1e293b",
    borderRadius: "12px",
    padding: "16px",
    border: "1px solid #334155",
  },
  sidePanel: {
    flex: 1,
    display: "flex",
    flexDirection: "column",
    gap: "16px",
  },
  panel: {
    backgroundColor: "#1e293b",
    borderRadius: "12px",
    padding: "16px",
    border: "1px solid #334155",
    flex: 1,
    overflowY: "auto",
  },
  panelTitle: {
    margin: "0 0 12px 0",
    fontSize: "15px",
    color: "#e2e8f0",
    display: "flex",
    alignItems: "center",
    gap: "8px",
  },
  videoFeed: {
    width: "100%",
    borderRadius: "8px",
    border: "1px solid #334155",
  },
  alertBadge: {
    backgroundColor: "#ef4444",
    color: "white",
    borderRadius: "50%",
    padding: "2px 7px",
    fontSize: "12px",
  },
  countBadge: {
    backgroundColor: "#3b82f6",
    color: "white",
    borderRadius: "50%",
    padding: "2px 7px",
    fontSize: "12px",
  },
  alertCard: {
    backgroundColor: "#450a0a",
    border: "1px solid #ef4444",
    borderRadius: "8px",
    padding: "10px 12px",
    marginBottom: "8px",
  },
  alertTitle: {
    margin: "0 0 4px 0",
    fontSize: "14px",
    color: "#fca5a5",
    fontWeight: "600",
  },
  alertDetail: {
    margin: "0 0 4px 0",
    fontSize: "12px",
    color: "#fca5a5",
  },
  alertTimer: {
    margin: 0,
    fontSize: "12px",
    color: "#f87171",
    fontWeight: "600",
  },
  trackedCard: {
    backgroundColor: "#0f2942",
    border: "1px solid #3b82f6",
    borderRadius: "8px",
    padding: "10px 12px",
    marginBottom: "8px",
  },
  trackedTitle: {
    margin: "0 0 4px 0",
    fontSize: "14px",
    color: "#93c5fd",
    fontWeight: "600",
  },
  trackedDetail: {
    margin: 0,
    fontSize: "12px",
    color: "#93c5fd",
  },
  safeText: {
    color: "#4ade80",
    fontSize: "13px",
  },
};

export default App;