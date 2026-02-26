import React from 'react'
import ReactMarkdown from 'react-markdown'

export default function RemediationPanel({ findings }) {
    const remediated = findings.filter(f => f.remediation)

    return (
        <div style={{ padding: 20 }}>
            <div className="section-title">🛡️ Autonomous Remediation ({remediated.length})</div>
            {remediated.length === 0 ? (
                <div className="feed-empty">
                    <div className="feed-empty-icon">🛡️</div>
                    <div>No remediation patches available.</div>
                    <div style={{ fontSize: 11 }}>Run a mission to generate autonomous fixes.</div>
                </div>
            ) : (
                remediated.map((f, i) => (
                    <div key={i} className="panel" style={{ marginBottom: 16, borderLeft: '4px solid var(--green-ok)' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
                            <div style={{ fontWeight: 700, color: 'var(--text-primary)' }}>{f.title}</div>
                            <span className="feed-badge badge-reporter">PATCH READY</span>
                        </div>
                        <div className="report-content" style={{ padding: 0, background: 'transparent', border: 'none' }}>
                            <ReactMarkdown>{f.remediation}</ReactMarkdown>
                        </div>
                        <div style={{ marginTop: 12, display: 'flex', gap: 10 }}>
                            <button className="btn btn-primary" style={{ fontSize: 11, padding: '6px 12px' }} onClick={() => alert('Patching logic integration pending production deployment...')}>🚀 DEPLOY PATCH</button>
                            <button className="btn btn-secondary" style={{ fontSize: 11, padding: '6px 12px' }}>📋 COPY CODE</button>
                        </div>
                    </div>
                ))
            )
            }
        </div>
    )
}
