import React from 'react'

const MODELS = [
    { id: 'deepseek-r1', tier: 'premium', specialty: 'Reasoning/Planning' },
    { id: 'qwen3-235b-a22b', tier: 'premium', specialty: 'Analysis' },
    { id: 'llama-3.1-405b-instruct', tier: 'premium', specialty: 'OSINT/Recon' },
    { id: 'qwen2.5-coder-32b-instruct', tier: 'mid', specialty: 'Exploit Dev' },
    { id: 'deepseek-v3', tier: 'premium', specialty: 'Tool Calling' },
    { id: 'llama-3.3-70b-instruct', tier: 'mid', specialty: 'General' },
    { id: 'gemma-3-27b-it', tier: 'mid', specialty: 'Report Writing' },
    { id: 'mixtral-8x22b-instruct', tier: 'mid', specialty: 'Fast Analysis' },
    { id: 'phi-4', tier: 'cheap', specialty: 'Quick Tasks' },
    { id: 'mistral-nemo-12b', tier: 'cheap', specialty: 'Lightweight' },
]

export default function ModelSelector({ selectedModel, setSelectedModel }) {
    return (
        <div style={{ padding: 16 }}>
            <div className="section-title">🤖 Model Selection</div>
            <div style={{ marginBottom: 10, fontSize: 11, color: 'var(--text-dim)' }}>Leave blank for auto-select</div>
            <div className="model-grid">
                {MODELS.map(m => (
                    <div
                        key={m.id}
                        className={`model-chip ${selectedModel === m.id ? 'selected' : ''}`}
                        onClick={() => setSelectedModel(selectedModel === m.id ? '' : m.id)}
                    >
                        <div>
                            <div className="model-chip-id">{m.id.replace(/-instruct$/, '')}</div>
                            <div style={{ fontSize: 10, color: 'var(--text-dim)' }}>{m.specialty}</div>
                        </div>
                        <span className={`model-chip-tier tier-${m.tier}`}>{m.tier.toUpperCase()}</span>
                    </div>
                ))}
            </div>
        </div>
    )
}
