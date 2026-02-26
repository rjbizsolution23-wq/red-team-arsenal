import React, { useState, useEffect, useRef, useCallback } from 'react'
import ReactMarkdown from 'react-markdown'
import AgentFeed from './components/AgentFeed'
import TaskInput from './components/TaskInput'
import FindingsPanel from './components/FindingsPanel'
import ModelSelector from './components/ModelSelector'
import RemediationPanel from './components/RemediationPanel'
import './styles/main.css'

const API = '/api'

const AGENTS = [
    { key: 'recon_master', name: 'ReconMaster', tier: 1, desc: 'Advanced OSINT & TAA', autonomy: 5 },
    { key: 'academic_agent', name: 'AcademicAgent', tier: 1, desc: 'Deep Research Specialist', autonomy: 5 },
    { key: 'red_team_supreme', name: 'Supreme Red Team', tier: 1, desc: 'Adversarial ML & AI Sec', autonomy: 5 },
    { key: 'polyglot_coder', name: 'Polyglot Coder', tier: 1, desc: 'Elite Exploit Development', autonomy: 5 },
    { key: 'defense_automator', name: 'DefenseAutomator', tier: 1, desc: 'Autonomous Remediation Engine', autonomy: 5 },
    { key: 'vulnbot', name: 'VulnBot', tier: 2, desc: 'Multi-agent exploitation', autonomy: 4 },
    { key: 'research_agent', name: 'Research Agent', tier: 0, desc: 'Academic/Technical DBs', autonomy: 5 },
]

export default function App() {
    const [tab, setTab] = useState('feed')
    const [request, setRequest] = useState('')
    const [target, setTarget] = useState('')
    const [cost, setCost] = useState('premium')
    const [selectedModel, setSelectedModel] = useState('')
    const [authorized, setAuthorized] = useState(false)
    const [loading, setLoading] = useState(false)
    const [sessionId, setSessionId] = useState(null)
    const [feed, setFeed] = useState([])
    const [report, setReport] = useState('')
    const [findings, setFindings] = useState([])
    const [knowledge, setKnowledge] = useState([])
    const [researchQuery, setResearchQuery] = useState('')
    const feedRef = useRef(null)
    const wsRef = useRef(null)

    useEffect(() => {
        if (feedRef.current) {
            feedRef.current.scrollTop = feedRef.current.scrollHeight
        }
    }, [feed])

    const connectWS = useCallback((sid) => {
        const proto = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
        const ws = new WebSocket(`${proto}//${window.location.host}/api/ws/${sid}`)
        wsRef.current = ws
        ws.onmessage = (e) => {
            try {
                const data = JSON.parse(e.data)
                if (data.type === 'complete') {
                    setLoading(false)
                    if (data.session?.result?.report) setReport(data.session.result.report)
                    if (data.session?.result?.findings) setFindings(data.session.result.findings)
                    if (data.session?.result?.knowledge) setKnowledge(data.session.result.knowledge)
                    setTab('report')
                } else {
                    setFeed(prev => [...prev, data])
                }
            } catch { }
        }
    }, [])

    const pollSession = useCallback((sid) => {
        const interval = setInterval(async () => {
            try {
                const resp = await fetch(`${API}/session/${sid}`)
                const data = await resp.json()
                if (data.status === 'done' || data.status === 'error') {
                    clearInterval(interval)
                    setLoading(false)
                    if (data.result?.report) setReport(data.result.report)
                    if (data.result?.findings) setFindings(data.result.findings)
                    if (data.result?.knowledge) setKnowledge(data.result.knowledge)
                }
            } catch { }
        }, 3000)
        return () => clearInterval(interval)
    }, [])

    const handleSubmit = async () => {
        if (!request.trim() || loading) return
        setLoading(true)
        setFeed([])
        setReport('')
        setFindings([])
        setKnowledge([])
        setTab('feed')
        try {
            const resp = await fetch(`${API}/task`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    request, target: target || null, cost_preference: cost,
                    preferred_model: selectedModel || null, authorized,
                }),
            })
            const data = await resp.json()
            setSessionId(data.session_id)
            connectWS(data.session_id)
            pollSession(data.session_id)
        } catch (e) {
            setFeed(prev => [...prev, { source: 'system', message: `❌ Error: ${e.message}`, ts: Date.now() / 1000 }])
            setLoading(false)
        }
    }

    const handleResearch = async () => {
        if (!researchQuery.trim()) return
        try {
            const resp = await fetch(`${API}/research?query=${encodeURIComponent(researchQuery)}&max_results=10`)
            const data = await resp.json()
            setKnowledge(data.results || [])
            setTab('knowledge')
        } catch (e) { console.error(e) }
    }

    return (
        <div className="layout">
            <div className="scan-line" />
            <header className="header">
                <div className="header-logo">
                    <span className="logo-icon glitch">🔴</span>
                    <div>
                        <div className="logo-text"><span>RED</span> TEAM <span>ARSENAL</span></div>
                        <div style={{ fontSize: 10, color: 'var(--text-dim)', letterSpacing: 2 }}>SUPREME META AGI SYSTEM</div>
                    </div>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: 24 }}>
                    <div className="header-status"><div className="status-dot" /> ONLINE</div>
                    <div className="header-meta">RJ Business Solutions<br /><span style={{ color: 'var(--red-bright)' }}>AUTHORIZED OPERATOR</span></div>
                </div>
            </header>

            <div className="main-content">
                <aside className="sidebar">
                    <div className="panel" style={{ padding: 12 }}>
                        <div className="panel-header">
                            <div className="panel-title">⚔️ Arsenal</div>
                            <span style={{ fontSize: 10, color: 'var(--text-dim)' }}>{AGENTS.length} agents</span>
                        </div>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
                            {AGENTS.map(a => (
                                <div key={a.key} className="agent-card">
                                    <span className={`agent-tier-badge tier-${a.tier}`}>T{a.tier === 0 ? 'INT' : a.tier}</span>
                                    <div className="agent-info"><div className="agent-name">{a.name}</div><div className="agent-desc">{a.desc}</div></div>
                                    <div className="autonomy-stars">{'★'.repeat(a.autonomy)}</div>
                                </div>
                            ))}
                        </div>
                    </div>
                    <div className="panel" style={{ padding: 12 }}>
                        <div className="panel-title" style={{ marginBottom: 10 }}>📚 Research</div>
                        <input className="input-field" style={{ width: '100%', marginBottom: 8 }} placeholder="Search arXiv..." value={researchQuery} onChange={e => setResearchQuery(e.target.value)} onKeyDown={e => e.key === 'Enter' && handleResearch()} />
                        <button className="btn btn-secondary" style={{ width: '100%', fontSize: 11 }} onClick={handleResearch}>🔍 Search Academic DB</button>
                    </div>
                </aside>

                <div className="center-panel">
                    <TaskInput 
                        request={request} setRequest={setRequest} target={target} setTarget={setTarget}
                        cost={cost} setCost={setCost} authorized={authorized} setAuthorized={setAuthorized}
                        loading={loading} handleSubmit={handleSubmit} sessionId={sessionId}
                    />
                    <div className="tabs">
                        <div className={`tab ${tab === 'feed' ? 'active' : ''}`} onClick={() => setTab('feed')}>⚡ Agent Feed {loading && <span className="pulse">●</span>}</div>
                        <div className={`tab ${tab === 'report' ? 'active' : ''}`} onClick={() => setTab('report')}>📋 Report {report && '✓'}</div>
                        <div className={`tab ${tab === 'remediation' ? 'active' : ''}`} onClick={() => setTab('remediation')}>🛡️ Purple Team {findings.some(f => f.remediation) && '✓'}</div>
                        <div className={`tab ${tab === 'knowledge' ? 'active' : ''}`} onClick={() => setTab('knowledge')}>📚 Knowledge {knowledge.length > 0 && `(${knowledge.length})`}</div>
                    </div>
                    {tab === 'feed' && <AgentFeed feed={feed} feedRef={feedRef} />}
                    {tab === 'report' && (
                        <div className="report-viewer">
                            {!report ? <div className="feed-empty">No report yet</div> : <div className="report-content"><ReactMarkdown>{report}</ReactMarkdown></div>}
                        </div>
                    )}
                    {tab === 'remediation' && <RemediationPanel findings={findings} />}
                    {tab === 'knowledge' && (
                        <div className="report-viewer">
                            {knowledge.length === 0 ? <div className="feed-empty">No knowledge items yet</div> : (
                                knowledge.map((k, i) => (
                                    <div key={i} className="knowledge-item">
                                        <div className="knowledge-source">{k.source?.toUpperCase()}</div>
                                        <div className="knowledge-title">{k.title}</div>
                                        <div className="knowledge-summary">{k.summary?.slice(0, 200)}</div>
                                    </div>
                                ))
                            )}
                        </div>
                    )}
                </div>
                <aside className="right-panel">
                    <FindingsPanel findings={findings} />
                    <div className="divider" />
                    <ModelSelector selectedModel={selectedModel} setSelectedModel={setSelectedModel} />
                </aside>
            </div>
        </div>
    )
}
