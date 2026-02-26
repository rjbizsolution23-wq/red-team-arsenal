import React from 'react'

const sevColor = { CRITICAL: '#ff2233', HIGH: '#ff7700', MEDIUM: '#ffcc00', LOW: '#00ff88', INFO: '#00d4ff' }

export default function FindingsPanel({ findings }) {
    return (
        <div style={{ padding: 16 }}>
            <div className="section-title">🔍 Findings ({findings.length})</div>
            {findings.length === 0 ? (
                <div style={{ color: 'var(--text-dim)', fontSize: 11, padding: '20px 0' }}>
                    No findings yet. Run a task to populate.
                </div>
            ) : (
                findings.map((f, i) => {
                    const sev = f.severity || 'INFO'
                    const color = sevColor[sev] || '#888'
                    return (
                        <div key={i} className={`finding-card finding-${sev.toLowerCase()}`}>
                            <div className="finding-badge" style={{ background: `${color}22`, color, border: `1px solid ${color}44` }}>
                                {sev}
                            </div>
                            <div className="finding-title">{f.title}</div>
                            <div className="finding-desc">{f.description?.slice(0, 120)}</div>
                            {f.agent && <div style={{ fontSize: 10, color: 'var(--text-dim)', marginTop: 4 }}>via {f.agent}</div>}
                        </div>
                    )
                })
            )}
        </div>
    )
}
