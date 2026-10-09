from pathlib import Path

def test_compliance_domain_does_not_import_django():
    domain_dir = Path(__file__).resolve().parents[2] / "domain"
    violations = []
    for path in domain_dir.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        if "import django" in text or "from django" in text:
            violations.append(str(path))
    assert not violations, f"Compliance domain depends on Django: {violations}"
