
import re
from urllib.parse import urlparse

REASONS = {
    "No URL entered.":
        "Please enter a URL to inspect.",

    "Could not identify a hostname.":
        "A valid hostname is needed to inspect the URL.",

    "Invalid URL format.":
        "The URL contains invalid formatting.",

    "Unusually long URL (over 100 characters).":
        "Long URLs can hide important details.",

    "Contains an @ symbol in the URL.":
        "Text before @ can mislead you about the actual hostname.",

    "Uses an IP address instead of a familiar domain.":
        "An IP address may hide the identity of the website.",

    "Contains many hostname segments/subdomains.":
        "Many subdomains can make a hostname confusing.",

    "Contains a punycode-style hostname.":
        "Punycode can represent international characters and may imitate familiar domains.",

    "Uses HTTP instead of HTTPS.":
        "HTTP does not encrypt the connection like HTTPS does.",

    "No listed warning signs found. This does NOT prove safety.":
        "The URL may still be unsafe; this checker uses basic text rules."
}


def inspect_url(raw_url):
    """Check a URL for selected phishing warning signs."""
    url = raw_url.strip()
    findings = []

    if not url:
        return ["No URL entered."]

    candidate = url if "://" in url else "http://" + url

    try:
        parsed = urlparse(candidate)
        host = (parsed.hostname or "").lower()
    except ValueError:
        return ["Invalid URL format."]

    if not host:
        return ["Could not identify a hostname."]

    if len(url) > 100:
        findings.append("Unusually long URL (over 100 characters).")

    if "@" in url:
        findings.append("Contains an @ symbol in the URL.")

    if re.fullmatch(r"(?:\d{1,3}\.){3}\d{1,3}", host):
        findings.append(
            "Uses an IP address instead of a familiar domain."
        )

    labels = [part for part in host.split(".") if part]

    if len(labels) >= 5:
        findings.append(
            "Contains many hostname segments/subdomains."
        )

    if "xn--" in host:
        findings.append("Contains a punycode-style hostname.")

    if parsed.scheme.lower() == "http":
        findings.append("Uses HTTP instead of HTTPS.")

    if not findings:
        findings.append(
            "No listed warning signs found. This does NOT prove safety."
        )

    return findings


def main():
    print("WEB Phishing URL Awareness Checker")
    print("Text checks only - URLs are not opened.")

    while True:
        raw_url = input(
            "\nEnter a URL (or type q to quit): "
        )

        if raw_url.strip().lower() in ("q", "quit", "exit"):
            print("Goodbye! Stay alert online.")
            break

        findings = inspect_url(raw_url)

        print("\nResult:")

        warning_found = any(
            not item.startswith("No listed warning signs found")
            for item in findings
        )

        for item in findings:
            print("- " + item)
            print("  Why: " + REASONS.get(
                item, "Be cautious and verify the URL."
            ))

        if warning_found:
            print("\nReview carefully: warning signs detected.")
        else:
            print("\nNo listed warning signs detected.")

        print("Remember: this checker cannot guarantee URL safety.")


if __name__ == "__main__":
    main()
