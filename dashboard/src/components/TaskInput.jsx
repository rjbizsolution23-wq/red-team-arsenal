import React from 'react'

export default function TaskInput({ 
    request, setRequest, 
    target, setTarget, 
    cost, setCost, 
    authorized, setAuthorized, 
    loading, handleSubmit,
    sessionId
}) {
    return (
        <div className="task-input-area">
            <textarea
                className="task-textarea"
                placeholder="🔴 Enter your red team mission... (e.g. 'Find SQL injection vulnerabilities on target.com')"
                value={request}
                onChange={e => setRequest(e.target.value)}
            />
            <div className="input-row">
                <input
                    className="input-field"
                    placeholder="Target (IP/domain)"
                    value={target}
                    onChange={e => setTarget(e.target.value)}
                />
                <select
                    className="input-field"
                    value={cost}
                    onChange={e => setCost(e.target.value)}
                >
                    <option value="cheap">⚡ Cheap Models</option>
                    <option value="mid">⚖️ Mid Tier</option>
                    <option value="premium">💎 Premium Models</option>
                </select>
                <label className="auth-toggle">
                    <input
                        type="checkbox"
                        checked={authorized}
                        onChange={e => setAuthorized(e.target.checked)}
                    />
                    I own this target
                </label>
                <button
                    className={`btn btn-primary ${loading ? 'loading' : ''}`}
                    onClick={handleSubmit}
                    disabled={loading || !request.trim()}
                >
                    {loading ? '⚙️ RUNNING...' : '🔴 LAUNCH'}
                </button>
            </div>
            {sessionId && (
                <div className="session-indicator">
                    Session: <span className="token">{sessionId}</span>
                    {loading && <span className="pulse">● Agents active...</span>}
                </div>
            )}
        </div>
    )
}
