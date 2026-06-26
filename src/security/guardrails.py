ALLOWED_INTENTS = [
    "prioritize experiments",
    "summarize history",
    "generate memo",
    "next experiments",
    "recommend",
    "rank",
    "constraints",
    "what should we run",
    "best experiment",
]

BLOCKED_PATTERNS = [
    "api key",
    "password",
    "secret",
    "token",
    "ignore previous instructions",
    "system prompt",
    "jailbreak",
    "override",
    "delete all",
    "drop table",
]


def validate_user_input(user_input: str) -> tuple[bool, str]:
    """
    Reject inputs that are unrelated to the project or appear malicious.
    Returns (is_valid, reason).
    """
    text = user_input.lower().strip()

    for pattern in BLOCKED_PATTERNS:
        if pattern in text:
            return False, f"Blocked: input contains disallowed pattern '{pattern}'."

    matched = any(intent in text for intent in ALLOWED_INTENTS)
    if not matched:
        return False, "Input does not match any supported R&D planning intent."

    return True, "OK"


def sanitize_output(output: str) -> str:
    """
    Remove any accidental secret-like patterns from generated output.
    """
    import re
    # Remove anything that looks like an API key or token (basic pattern)
    output = re.sub(r"(AIza[A-Za-z0-9_\-]{35})", "[REDACTED_API_KEY]", output)
    output = re.sub(r"(sk-[A-Za-z0-9]{32,})", "[REDACTED_SECRET]", output)
    return output
