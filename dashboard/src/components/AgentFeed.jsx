import React from 'react'

const BADGE_MAP = {
    system: 'badge-system', planner: 'badge-planner', executor: 'badge-executor',
    reporter: 'badge-reporter', cloudflare: 'badge-cloudflare', docker: 'badge-docker',
    security: 'badge-security', orchestrator: 'badge-orchestrator',
}

export default function AgentFeed({ feed, feedRef }) {
    if (feed.length === 0) {
        return (
            <div className="feed-empty">
                <div className="feed-empty-icon">💀</div>
                <div>Awaiting mission briefing...</div>
                <div style={{ fontSize: 11 }}>Submit a request to deploy the red team</div>
            </div>
        )
    }

    return (
        <div className="agent-feed" ref={feedRef}>
            {feed.map((entry, i) => {
                const source = (entry.source || 'system').toLowerCase()
                const badgeClass = BADGE_MAP[source] || 'badge-system'
                const ts = new Date(entry.ts * 1000).toLocaleTimeString('en-US', { hour12: false })
                return (
                    <div key={i} className="feed-entry">
                        <span className={`feed-badge ${badgeClass}`}>{source.toUpperCase()}</span>
                        <span className="feed-msg">{entry.message}</span>
                        <span className="feed-ts">{ts}</span>
                    </div>
                )
            })}
        </div>
    )
}
