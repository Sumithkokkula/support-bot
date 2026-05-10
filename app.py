import streamlit as st
from bot import get_bot_response

st.set_page_config(
    page_title="ShopEase Support",
    page_icon="🛍️",
    layout="centered"
)
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stChatMessage {
        border-radius: 15px;
        padding: 10px;
    }
    .escalation-box {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    .confident-box {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    .header-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 20px;
    }
    .metric-box {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="header-box">
        <h1>🛍️ ShopEase Support</h1>
        <p>Hi! I'm Alex, your personal support assistant. How can I help you today?</p>
    </div>
""", unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "total_messages" not in st.session_state:
    st.session_state.total_messages = 0
if "escalations" not in st.session_state:
    st.session_state.escalations = 0
if "resolved" not in st.session_state:
    st.session_state.resolved = 0

st.markdown("### 📊 Live Analytics")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("💬 Total Messages", st.session_state.total_messages)
with col2:
    st.metric("✅ Resolved", st.session_state.resolved)
with col3:
    st.metric("🚨 Escalations", st.session_state.escalations)

st.markdown("---")


for message in st.session_state.chat_history:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["content"])
    else:
        with st.chat_message("assistant", avatar="🛍️"):
            st.markdown(message["content"])

user_input = st.chat_input("Type your message here...")

if user_input:

    with st.chat_message("user"):
        st.markdown(user_input)

    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input
    })

    with st.spinner("Alex is typing..."):
        result = get_bot_response(
            user_input,
            st.session_state.chat_history[:-1]
        )

    with st.chat_message("assistant", avatar="🛍️"):
        st.markdown(result["reply"])
        if result["escalate"]:
            st.markdown("""
                <div class="escalation-box">
                    🚨 <strong>Escalating to Human Agent</strong><br>
                    A support specialist will contact you within 30 minutes.
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="confident-box">
                    ✅ <strong>Resolved by AI</strong><br>
                    This issue was successfully handled by Alex.
                </div>
            """, unsafe_allow_html=True)

    st.session_state.chat_history.append({
        "role": "model",
        "content": result["reply"]
    }) 
    st.session_state.total_messages += 1
    if result["escalate"]:
        st.session_state.escalations += 1
    else:
        st.session_state.resolved += 1

    st.rerun()

# Sidebar
with st.sidebar:
    st.markdown("## 🛍️ ShopEase Support")
    st.markdown("---")
    st.markdown("### 💡 You can ask about:")
    st.markdown("- 📦 Order tracking")
    st.markdown("- 🔄 Returns & refunds")
    st.markdown("- ❌ Order cancellation")
    st.markdown("- 🚚 Delivery times")
    st.markdown("- 💳 Payment issues")
    st.markdown("- 📍 Address changes")
    st.markdown("- 💵 Cash on delivery")
    st.markdown("---")

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.total_messages = 0
        st.session_state.escalations = 0
        st.session_state.resolved = 0
        st.rerun()

    st.markdown("---")
    st.markdown("### 📈 Session Stats")
    if st.session_state.total_messages > 0:
        resolution_rate = (st.session_state.resolved / st.session_state.total_messages) * 100
        st.markdown(f"**Resolution Rate: {resolution_rate:.0f}%**")
        st.progress(resolution_rate / 100)
    else:
        st.markdown("No messages yet")