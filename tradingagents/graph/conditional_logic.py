# TradingAgents/graph/conditional_logic.py

from tradingagents.agents.utils.agent_states import AgentState
from langchain_core.messages import ToolMessage

MAX_TOOL_CALLS_PER_ANALYST = 8


def _count_recent_tool_calls(messages):
    """Count consecutive tool call rounds from the end of messages."""
    count = 0
    for msg in reversed(messages):
        if isinstance(msg, ToolMessage):
            count += 1
        elif hasattr(msg, 'tool_calls') and msg.tool_calls:
            continue
        else:
            break
    return count


class ConditionalLogic:
    """Handles conditional logic for determining graph flow."""

    def __init__(self, max_debate_rounds=1, max_risk_discuss_rounds=1):
        """Initialize with configuration parameters."""
        self.max_debate_rounds = max_debate_rounds
        self.max_risk_discuss_rounds = max_risk_discuss_rounds

    def _should_continue_analyst(self, state, tools_node, clear_node):
        messages = state["messages"]
        last_message = messages[-1]
        if last_message.tool_calls and _count_recent_tool_calls(messages) < MAX_TOOL_CALLS_PER_ANALYST:
            return tools_node
        return clear_node

    def should_continue_market(self, state: AgentState):
        return self._should_continue_analyst(state, "tools_market", "Msg Clear Market")

    def should_continue_social(self, state: AgentState):
        return self._should_continue_analyst(state, "tools_social", "Msg Clear Social")

    def should_continue_news(self, state: AgentState):
        return self._should_continue_analyst(state, "tools_news", "Msg Clear News")

    def should_continue_fundamentals(self, state: AgentState):
        return self._should_continue_analyst(state, "tools_fundamentals", "Msg Clear Fundamentals")

    def should_continue_debate(self, state: AgentState) -> str:
        """Determine if debate should continue."""

        if (
            state["investment_debate_state"]["count"] >= 2 * self.max_debate_rounds
        ):  # 3 rounds of back-and-forth between 2 agents
            return "Research Manager"
        if state["investment_debate_state"]["current_response"].startswith("Bull"):
            return "Bear Researcher"
        return "Bull Researcher"

    def should_continue_risk_analysis(self, state: AgentState) -> str:
        """Determine if risk analysis should continue."""
        if (
            state["risk_debate_state"]["count"] >= 3 * self.max_risk_discuss_rounds
        ):  # 3 rounds of back-and-forth between 3 agents
            return "Risk Judge"
        if state["risk_debate_state"]["latest_speaker"].startswith("Risky"):
            return "Safe Analyst"
        if state["risk_debate_state"]["latest_speaker"].startswith("Safe"):
            return "Neutral Analyst"
        return "Risky Analyst"
