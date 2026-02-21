# TradingAgents/graph/signal_processing.py
import re


class SignalProcessor:
    """Processes trading signals to extract actionable decisions."""

    def __init__(self, quick_thinking_llm=None):
        pass

    def process_signal(self, full_signal: str) -> str:
        """Extract BUY/SELL/HOLD from text using regex."""
        text = full_signal.upper()
        # Look for explicit signal patterns
        for pattern in [r'\b(BUY|SELL|HOLD)\b']:
            matches = re.findall(pattern, text)
            if matches:
                # Count occurrences, return most frequent
                from collections import Counter
                return Counter(matches).most_common(1)[0][0]
        return "HOLD"
