"""Remediator Agent — generate fixes and open hotfix PRs."""

from logcrew.models import Incident, RootCause


class RemediatorAgent:
    """Generate remediation actions and optionally create GitHub PRs."""

    def __init__(self, github_token: str = "") -> None:
        self.github_token = github_token

    async def remediate(self, incident: Incident, root_cause: RootCause) -> dict:
        """Return remediation plan: commands, patches, and notifications."""
        plan = {
            "incident_id": incident.id,
            "commands": [],
            "pr_url": None,
            "notify": {},
        }

        if root_cause.confidence < 0.6:
            plan["commands"].append("echo 'Low confidence — manual review required'")
            return plan

        # Generate a targeted fix command based on hypothesis
        fix_cmd = self._generate_fix(root_cause.hypothesis)
        plan["commands"].append(fix_cmd)

        # Notification payload for Lark / Feishu
        plan["notify"] = {
            "platform": "lark",
            "title": f"Incident {incident.id} remediated",
            "content": f"Root cause: {root_cause.hypothesis}\nConfidence: {root_cause.confidence}",
        }

        return plan

    def _generate_fix(self, hypothesis: str) -> str:
        """Produce a shell command or code patch string. Placeholder."""
        return f"# Auto-generated fix for: {hypothesis}\nkubectl rollout restart deployment/{hypothesis.split()[-1]}"
