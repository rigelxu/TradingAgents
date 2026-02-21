"""从 messages 历史中提取最佳 report"""
from langchain_core.messages import AIMessage, ToolMessage


def extract_best_report(messages, current_content=""):
    """如果 current_content 足够长直接返回，否则拼接 tool 结果作为 report"""
    if current_content and len(current_content) > 200:
        return current_content
    # 收集所有 tool 返回的数据
    tool_data = []
    for msg in messages:
        if isinstance(msg, ToolMessage) and msg.content and len(msg.content) > 50:
            tool_data.append(msg.content)
    if tool_data:
        return "\n\n---\n\n".join(tool_data)
    # fallback: 最长的 AI content
    best = current_content or ""
    for msg in messages:
        if isinstance(msg, AIMessage) and msg.content and len(msg.content) > len(best):
            best = msg.content
    return best
