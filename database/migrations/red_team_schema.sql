-- ═══════════════════════════════════════════
-- RED TEAM MODULE — SUPABASE SCHEMA
-- RJ Business Solutions | 2026-02-26
-- ═══════════════════════════════════════════

CREATE TABLE red_team_scans (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID DEFAULT auth.uid(),
  name VARCHAR(255) NOT NULL,
  target_endpoint TEXT NOT NULL,
  status VARCHAR(50) DEFAULT 'pending',
  vulnerabilities_found INTEGER DEFAULT 0,
  compliance_score INTEGER,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE red_team_vulnerabilities (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  scan_id UUID REFERENCES red_team_scans(id) ON DELETE CASCADE,
  title VARCHAR(500) NOT NULL,
  description TEXT NOT NULL,
  attack_vector VARCHAR(100) NOT NULL,
  severity VARCHAR(20) NOT NULL,
  owasp_category VARCHAR(10),
  remediation TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE red_team_reports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  scan_id UUID REFERENCES red_team_scans(id),
  overall_risk_score INTEGER,
  pdf_url TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);
