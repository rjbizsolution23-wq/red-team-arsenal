"""
🔴💀 REMEDIATION ENGINE — The "Fix" for the Red Team Arsenal
Automatically generates code and patches to resolve identified vulnerabilities.
"""
import os
from typing import Dict, Any, List, Optional
from loguru import logger

class RemediationEngine:
    def __init__(self):
        self.patch_templates = {
            "sqli": "Use parameterized queries or ORM-based abstraction layers.",
            "xss": "Implement context-aware output encoding and Content Security Policy (CSP).",
            "s3_public": "Restrict S3 bucket ACLs and enable Block Public Access settings via Terraform.",
            "open_ssh": "Restrict SSH access to specific CIDR ranges and enforce key-based authentication.",
            "weak_auth": "Enforce Multi-Factor Authentication (MFA) and strong password policies.",
            "cleartext_secrets": "Use AWS Secrets Manager, HashiCorp Vault, or encrypted environment variables.",
        }

    def generate_patch(self, finding: Dict[str, Any]) -> str:
        """
        Generates a remediation recommendation and code snippet for a finding.
        """
        title = finding.get("title", "").lower()
        description = finding.get("description", "").lower()
        
        remediation = "Generic security hardening recommended."
        code_snippet = ""

        if "sql injection" in title or "sqli" in description:
            remediation = self.patch_templates["sqli"]
            code_snippet = "## [FIX] Python SQLAlchemy Example\nquery = session.query(User).filter(User.username == username)"
        elif "s3" in title and ("public" in description or "acl" in description):
            remediation = self.patch_templates["s3_public"]
            code_snippet = "## [FIX] Terraform\nresource \"aws_s3_bucket_public_access_block\" \"block\" {\n  bucket = aws_s3_bucket.my_bucket.id\n  block_public_acls = true\n  block_public_policy = true\n}"
        elif "ssh" in title and "open" in description:
            remediation = self.patch_templates["open_ssh"]
            code_snippet = "## [FIX] AWS Security Group\ningress {\n  from_port = 22\n  to_port = 22\n  protocol = \"tcp\"\n  cidr_blocks = [\"ALLOWED_IP/32\"]\n}"

        return f"### 🛡️ Remediation Strategy\n{remediation}\n\n```markdown\n{code_snippet}\n```"

    def audit_and_repair(self, findings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Processes a list of findings and appends remediation data.
        """
        repaired_findings = []
        for finding in findings:
            finding_copy = finding.copy()
            finding_copy["remediation"] = self.generate_patch(finding)
            repaired_findings.append(finding_copy)
        return repaired_findings
