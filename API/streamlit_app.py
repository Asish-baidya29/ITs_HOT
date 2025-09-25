import streamlit as st
import traceback
from datetime import datetime
from agent_controler import AgentController

# --- Page Config ---
st.set_page_config(
    page_title="It's HOT - Your AI Barista",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Enhanced Modern CSS Styling ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif !important;
    }
    
    .main {
        padding: 0 !important;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        min-height: 100vh;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #2d3748 0%, #1a202c 100%);
        color: white;
    }
    
    .brand-header {
        text-align: center;
        padding: 2rem 1rem;
        background: linear-gradient(135deg, #2d3748, #4a5568);
        color: white;
        margin-bottom: 2rem;
    }
    
    .brand-logo {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        color: #68d391;
    }
    
    .brand-tagline {
        font-size: 1.1rem;
        opacity: 0.9;
        font-weight: 300;
    }
    
    /* Top Navigation Bar */
    .top-nav {
        position: fixed;
        top: 0;
        right: 0;
        z-index: 1000;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 1rem 2rem;
        border-bottom: 1px solid rgba(0, 0, 0, 0.1);
        border-bottom-left-radius: 15px;
        box-shadow: 0 2px 20px rgba(0, 0, 0, 0.1);
    }
    
    .chat-btn {
        background: linear-gradient(135deg, #68d391, #38b2ac) !important;
        color: white !important;
        border: none !important;
        padding: 0.8rem 1.5rem !important;
        border-radius: 25px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(104, 211, 145, 0.3) !important;
        display: inline-flex !important;
        align-items: center !important;
        gap: 0.5rem !important;
    }
    
    .chat-btn:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(104, 211, 145, 0.4) !important;
    }
    
    /* Add top padding to main content to avoid overlap with fixed nav */
    .main-content {
        padding-top: 80px;
    }
    
    .hero-section {
        background: linear-gradient(135deg, rgba(255,255,255,0.95), rgba(255,255,255,0.8)),
                    url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000"><defs><pattern id="coffee" patternUnits="userSpaceOnUse" width="100" height="100"><circle cx="50" cy="50" r="20" fill="rgba(139,69,19,0.1)"/></pattern></defs><rect width="1000" height="1000" fill="url(%23coffee)"/></svg>');
        padding: 3rem 2rem;
        margin: 1rem;
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        color: #2d3748;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .hero-subtitle {
        font-size: 1.4rem;
        color: #4a5568;
        font-weight: 400;
        margin-bottom: 2rem;
    }
    
    .menu-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1.5rem;
        padding: 2rem 1rem;
    }
    
    .menu-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        border: 1px solid rgba(0,0,0,0.05);
        position: relative;
        overflow: hidden;
    }
    
    .menu-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
    }
    
    .menu-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #68d391, #38b2ac);
    }
    
    .coffee-image {
        width: 100%;
        height: 200px;
        object-fit: cover;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    
    .coffee-name {
        font-size: 1.3rem;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 0.5rem;
    }
    
    .coffee-price {
        font-size: 1.1rem;
        font-weight: 500;
        color: #68d391;
        margin-bottom: 1rem;
    }
    
    .coffee-description {
        font-size: 0.9rem;
        color: #718096;
        line-height: 1.4;
    }
    
    /* Featured Menu Item Styling */
    .featured-menu-item {
        background: white;
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 15px 35px rgba(0,0,0,0.08);
        transition: all 0.4s ease;
        border: 1px solid rgba(0,0,0,0.04);
        position: relative;
        overflow: hidden;
    }
    
    .featured-menu-item:hover {
        transform: translateY(-8px);
        box-shadow: 0 25px 50px rgba(0,0,0,0.15);
    }
    
    .featured-menu-item::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 5px;
        background: linear-gradient(90deg, #68d391, #38b2ac, #9f7aea);
        border-radius: 20px 20px 0 0;
    }
    
    .featured-item-image {
        width: 100%;
        height: 220px;
        object-fit: cover;
        border-radius: 15px;
        margin-bottom: 1.2rem;
        transition: all 0.3s ease;
    }
    
    .featured-menu-item:hover .featured-item-image {
        transform: scale(1.02);
    }
    
    .featured-item-name {
        font-size: 1.4rem;
        font-weight: 700;
        color: #2d3748;
        margin-bottom: 0.8rem;
        text-align: center;
    }
    
    .featured-item-price {
        font-size: 1.3rem;
        font-weight: 600;
        color: #68d391;
        text-align: center;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, #68d391, #38b2ac);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .featured-item-description {
        font-size: 1rem;
        color: #4a5568;
        line-height: 1.6;
        text-align: center;
        font-weight: 400;
    }
    
    .chat-container {
        background: white;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        margin: 1rem;
        overflow: hidden;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
    }
    
    .chat-header {
        background: linear-gradient(135deg, #68d391, #38b2ac);
        color: white;
        padding: 1.5rem;
        text-align: center;
    }
    
    .chat-header h3 {
        margin: 0;
        font-size: 1.4rem;
        font-weight: 600;
    }
    
    .chat-area {
        height: 500px;
        overflow-y: auto;
        padding: 1.5rem;
        background: #0e1117;
    }
    
    .message-user {
        text-align: right;
        margin: 1rem 0;
    }
    
    .message-assistant {
        text-align: left;
        margin: 1rem 0;
    }
    
    .message-bubble-user {
        display: inline-block;
        background: linear-gradient(135deg, #68d391, #38b2ac);
        color: white;
        padding: 0.8rem 1.2rem;
        border-radius: 20px 20px 5px 20px;
        max-width: 75%;
        font-weight: 400;
        box-shadow: 0 3px 10px rgba(104,211,145,0.3);
    }
    
    .message-bubble-assistant {
        display: inline-block;
        background: white;
        color: #2d3748;
        padding: 0.8rem 1.2rem;
        border-radius: 20px 20px 20px 5px;
        max-width: 75%;
        border: 1px solid #e2e8f0;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
    }
    
    .order-summary {
        background: #69a882;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        max-width: 400px;
        margin-left: auto;
        margin-right: auto;
    }
    
    .order-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.8rem 0;
        border-bottom: 1px solid #f1f3f4;
    }
    
    .order-item:last-child {
        border-bottom: none;
        font-weight: 600;
        font-size: 1.1rem;
        color: #2d3748;
    }
    
    .btn-primary {
        background: linear-gradient(135deg, #68d391, #38b2ac);
        color: white;
        border: none;
        padding: 0.8rem 1.5rem;
        border-radius: 25px;
        font-weight: 500;
        transition: all 0.3s ease;
        cursor: pointer;
        width: 100%;
        margin: 0.5rem 0;
    }
    
    .btn-primary:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(104,211,145,0.4);
    }
    
    .btn-secondary {
        background: #f1f3f4;
        color: #2d3748;
        border: 1px solid #e2e8f0;
        padding: 0.8rem 1.5rem;
        border-radius: 25px;
        font-weight: 500;
        transition: all 0.3s ease;
        cursor: pointer;
        width: 100%;
        margin: 0.5rem 0;
    }
    
    .stats-card {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    
    .stats-number {
        font-size: 2rem;
        font-weight: 700;
        color: #68d391;
    }
    
    .stats-label {
        font-size: 0.9rem;
        color: #718096;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .sidebar-nav {
        padding: 1rem 0;
    }
    
    .nav-item {
        padding: 0.8rem 1.5rem;
        color: rgba(255,255,255,0.8);
        font-weight: 500;
        border-left: 3px solid transparent;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .nav-item:hover {
        background: rgba(255,255,255,0.1);
        border-left-color: #68d391;
        color: white;
    }
    
    .nav-item.active {
        background: rgba(104,211,145,0.2);
        border-left-color: #68d391;
        color: white;
    }
    
    .back-btn {
        background: #f1f3f4 !important;
        color: #2d3748 !important;
        border: 1px solid #e2e8f0 !important;
        padding: 0.6rem 1.2rem !important;
        border-radius: 20px !important;
        font-weight: 500 !important;
        margin-bottom: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .back-btn:hover {
        background: #e2e8f0 !important;
        transform: translateX(-2px) !important;
    }
    
    /* Streamlit specific overrides */
    .stButton > button {
        background: linear-gradient(135deg, #68d391, #38b2ac) !important;
        color: white !important;
        border: none !important;
        padding: 0.8rem 1.5rem !important;
        border-radius: 25px !important;
        font-weight: 500 !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 15px rgba(104,211,145,0.4) !important;
    }
    
    .stTextInput > div > div > input {
        border-radius: 25px !important;
        border: 2px solid #e2e8f0 !important;
        padding: 0.8rem 1.2rem !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #68d391 !important;
        box-shadow: 0 0 0 3px rgba(104,211,145,0.1) !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent_controller" not in st.session_state:
    st.session_state.agent_controller = None
if "current_order" not in st.session_state:
    st.session_state.current_order = []
if "active_page" not in st.session_state:
    st.session_state.active_page = "HOME"

# --- Agent Init ---
@st.cache_resource
def init_agent():
    try:
        return AgentController()
    except Exception as e:
        st.error(f"❌ Failed to init agent: {e}")
        return None

# --- Top Navigation with Chat Button ---
if st.session_state.active_page != "CHAT":
    st.markdown("""
    <div class="top-nav">
        <div style="display: flex; justify-content: flex-end; align-items: center;">
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat button in top right
    col1, col2, col3 = st.columns([6, 1, 1])
    with col3:
        if st.button("💬 Chat with AI", key="top_chat_btn"):
            st.session_state.active_page = "CHAT"
            st.rerun()

# --- Sidebar Navigation ---
with st.sidebar:
    st.markdown("""
    <div class="brand-header">
        <div class="brand-logo">IT's HOT</div>
        <div class="brand-tagline">YOUR AI BARISTA</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-nav">', unsafe_allow_html=True)
    
    if st.button("🏠 HOME", key="nav_home", use_container_width=True):
        st.session_state.active_page = "HOME"
    if st.button("📋 MENU", key="nav_menu", use_container_width=True):
        st.session_state.active_page = "MENU"
    if st.button("🛒 YOUR CURRENT ORDER", key="nav_order", use_container_width=True):
        st.session_state.active_page = "ORDER"
    if st.button("📍 LOCATIONS", key="nav_locations", use_container_width=True):
        st.session_state.active_page = "LOCATIONS"
    if st.button("ℹ️ ABOUT US", key="nav_about", use_container_width=True):
        st.session_state.active_page = "ABOUT"
    if st.button("📞 CONTACT", key="nav_contact", use_container_width=True):
        st.session_state.active_page = "CONTACT"
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Show stats only on non-chat pages
    if st.session_state.active_page != "CHAT":
        st.markdown("### 📊 Quick Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="stats-card">
                <div class="stats-number">{len(st.session_state.messages)}</div>
                <div class="stats-label">Messages</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="stats-card">
                <div class="stats-number">{len(st.session_state.current_order)}</div>
                <div class="stats-label">Orders</div>
            </div>
            """, unsafe_allow_html=True)

# --- Main Content ---
st.markdown('<div class="main-content">', unsafe_allow_html=True)

if st.session_state.active_page == "CHAT":
    # Back button
    if st.button("← Back to Home", key="back_home"):
        st.session_state.active_page = "HOME"
        st.rerun()
    
    # Chat Interface
    st.markdown("""
    <div class="chat-container">
        <div class="chat-header">
            <h3>💬 Chat with Botista - Your AI Coffee Assistant</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Assistant Controls
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("🚀 Start Assistant", use_container_width=True):
            st.session_state.agent_controller = init_agent()
            if st.session_state.agent_controller:
                st.success("✅ Assistant Ready!")
    with col2:
        if st.button("🗑️ Reset Chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.current_order = []
            st.success("Chat cleared!")
    with col3:
        debug_mode = st.toggle("🔍 Debug Mode")

    # Chat Messages
    chat_container = st.container()
    with chat_container:
        st.markdown('<div class="chat-area">', unsafe_allow_html=True)
        
        if not st.session_state.messages:
            st.markdown("""
            <div class="message-assistant">
                <div class="message-bubble-assistant">
                    Hi! I'm Botista, your AI Coffee Assistant. How can I help you today? ☕
                </div>
            </div>
            """, unsafe_allow_html=True)

        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f"""
                <div class="message-user">
                    <div class="message-bubble-user">{msg['content']}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                agent = msg.get("memory", {}).get("agent", "Botista")
                st.markdown(f"""
                <div class="message-assistant">
                    <div class="message-bubble-assistant"><strong>{agent}:</strong> {msg['content']}</div>
                </div>
                """, unsafe_allow_html=True)
                if debug_mode:
                    st.json(msg.get("memory", {}))
        
        st.markdown('</div>', unsafe_allow_html=True)

    # User Input
    col1, col2 = st.columns([4, 1])
    with col1:
        user_input = st.text_input("Type your message:", placeholder="I'd like a cappuccino...", key="chat_input")
    with col2:
        send_button = st.button("Send", use_container_width=True)

    if send_button and user_input:
        if not st.session_state.agent_controller:
            st.warning("⚠️ Please initialize the assistant first!")
        else:
            st.session_state.messages.append({"role": "user", "content": user_input})
            try:
                with st.spinner("Botista is thinking..."):
                    resp = st.session_state.agent_controller.get_response({"input": {"messages": st.session_state.messages}})
                st.session_state.messages.append(resp)
                if resp.get("memory", {}).get("agent") == "order_taking_agent":
                    st.session_state.current_order = resp.get("memory", {}).get("order", [])
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")
                if debug_mode:
                    st.code(traceback.format_exc())

    # Order Summary
    if st.session_state.current_order:
        total = sum(item.get("price", 0) for item in st.session_state.current_order)
        order_html = '<div class="order-summary"><h4>🛒 Your Current Order</h4>'
        
        for item in st.session_state.current_order:
            order_html += f"""
            <div class="order-item">
                <span>{item.get('item', '?')} x{item.get('quantity', 1)}</span>
                <span>₹{item.get('price', 0)}</span>
            </div>
            """
        
        order_html += f"""
        <div class="order-item" style="font-weight: 700; font-size: 1.1rem; color:#2d3748;">
            <span>Total</span>
            <span>₹{total}</span>
        </div></div>
        """
        st.markdown(order_html, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Clear Order", use_container_width=True):
                st.session_state.current_order = []
                st.rerun()
        with col2:
            if st.button("Confirm Order", use_container_width=True):
                st.success("🎉 Order confirmed! Thank you!")

elif st.session_state.active_page == "HOME":
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">WELCOME TO IT's HOT</h1>
        <p class="hero-subtitle">Experience the perfect blend of technology and coffee craftsmanship and also hot like you</p>
    </div>
    """, unsafe_allow_html=True)

    # Featured Menu Items
    st.markdown("### ☕ Featured Menu")
    
    menu_items = [
        # Coffee & Espresso
        {"name": "Cappuccino", "price": "₹250", "image": "../products/imgs/Cappuccino.png", "desc": "Rich espresso with foamed milk"},
        {"name": "Espresso Shot", "price": "₹150", "image": "../products/imgs/Espresso_shot.jpg", "desc": "Pure, intense coffee experience"},
        {"name": "Latte", "price": "₹275", "image": "../products/imgs/Latte.jpg", "desc": "Smooth espresso with steamed milk"},
        {"name": "Ouro Brasileiro Shot", "price": "₹200", "image": "../products/imgs/Ouro_Brasileiro_shot.jpeg", "desc": "Strong, bold espresso shot"},

        # Drinking Chocolate
        {"name": "Dark Chocolate", "price": "₹300", "image": "../products/imgs/Dark_chocolate.png", "desc": "Rich and creamy dark chocolate"},
        {"name": "Chili Mayan", "price": "₹350", "image": "../products/imgs/Chili_Mayan.jpeg", "desc": "Spicy Mayan-inspired chocolate drink"},

        # Tea Selection
        {"name": "Traditional Blend Chai", "price": "₹180", "image": "../products/imgs/Traditional_Blend_Chai.png", "desc": "Classic Indian spiced tea"},
        {"name": "Serenity Green Tea", "price": "₹200", "image": "../products/imgs/Serenity_Green_Tea.png", "desc": "Light, calming green tea"},
        {"name": "English Breakfast", "price": "₹190", "image": "../products/imgs/English_Breakfast.png", "desc": "Robust black tea"},
        {"name": "Earl Grey", "price": "₹200", "image": "../products/imgs/Earl_Grey.png", "desc": "Citrus-flavored black tea"},
        {"name": "Morning Sunrise Chai", "price": "₹180", "image": "../products/imgs/Morning_Sunrise_Chai.png", "desc": "Spiced tea to start your day"},
        {"name": "Peppermint", "price": "₹180", "image": "../products/imgs/Peppermint.png", "desc": "Refreshing peppermint tea"},
        {"name": "Lemon Grass", "price": "₹180", "image": "../products/imgs/Lemon_Grass.png", "desc": "Aromatic lemongrass infusion"},
        {"name": "Spicy Eye Opener Chai", "price": "₹220", "image": "../products/imgs/Spicy_Eye_Opener_Chai.png", "desc": "Strong, spiced chai to wake you up"},

        # Bakery & Pastries
        {"name": "Oatmeal Scone", "price": "₹160", "image": "../products/imgs/Oatmeal_Scone.png", "desc": "Hearty oatmeal scone"},
        {"name": "Jumbo Savory Scone", "price": "₹200", "image": "../products/imgs/Jumbo_Savory_Scone.png", "desc": "Large savory scone"},
        {"name": "Chocolate Chip Biscotti", "price": "₹150", "image": "../products/imgs/Chocolate_Chip_Biscotti.png", "desc": "Crunchy chocolate chip biscotti"},
        {"name": "Ginger Biscotti", "price": "₹150", "image": "../products/imgs/Ginger_Biscotti.png", "desc": "Spiced ginger biscotti"},
        {"name": "Chocolate Croissant", "price": "₹220", "image": "../products/imgs/Chocolate_Croissant.png", "desc": "Flaky chocolate-filled croissant"},
        {"name": "Hazelnut Biscotti", "price": "₹150", "image": "../products/imgs/Hazelnut_Biscotti.png", "desc": "Nutty and crunchy biscotti"},
        {"name": "Cranberry Scone", "price": "₹180", "image": "../products/imgs/Cranberry_Scone.png", "desc": "Sweet cranberry scone"},
        {"name": "Scottish Cream Scone", "price": "₹200", "image": "../products/imgs/Scottish_Cream_Scone.png", "desc": "Creamy Scottish-style scone"},
        {"name": "Croissant", "price": "₹180", "image": "../products/imgs/Croissant.png", "desc": "Classic buttery croissant"},
        {"name": "Almond Croissant", "price": "₹250", "image": "../products/imgs/Almond_Croissant.png", "desc": "Flaky croissant with almond filling"},
        {"name": "Ginger Scone", "price": "₹180", "image": "../products/imgs/Ginger_Scone.jpg", "desc": "Spicy ginger scone"},


        ]
    

    items_per_row = 4  

    for i in range(0, len(menu_items), items_per_row):
        row_items = menu_items[i:i+items_per_row]
        cols = st.columns(len(row_items))  # dynamically create columns
        for col, item in zip(cols, row_items):
            with col:
                st.image(item['image'], use_container_width=True)
                st.markdown(f"""
                    <div class="coffee-name">{item['name']}</div>
                    <div class="coffee-price">{item['price']}</div>
                    <div class="coffee-description">{item['desc']}</div>
                """, unsafe_allow_html=True)
                
                

elif st.session_state.active_page == "ORDER":
    st.markdown("### 🛒 Your Current Order")
    
    if st.session_state.current_order:
        # Order Summary with enhanced styling
        total = sum(item.get("price", 0) for item in st.session_state.current_order)
        
        st.markdown("""
        <div style="max-width: 600px; margin: 0 auto;">
        """, unsafe_allow_html=True)
        
        for i, item in enumerate(st.session_state.current_order):
            st.markdown(f"""
            <div class="featured-menu-item" style="margin-bottom: 1.5rem;">
                <div class="order-item">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div class="featured-item-name" style="text-align: left; margin-bottom: 0.5rem;">{item.get('item', '?')}</div>
                            <div style="color: #718096;">Quantity: {item.get('quantity', 1)}</div>
                        </div>
                        <div class="featured-item-price" style="margin-bottom: 0;">₹{item.get('price', 0)}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Total Section
        st.markdown(f"""
        <div class="featured-menu-item" style="background: linear-gradient(135deg, #68d391, #38b2ac); color: white;">
            <div class="order-item">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div class="featured-item-name" style="color: white; text-align: left;">Total Amount</div>
                    <div style="font-size: 1.5rem; font-weight: 700; color: white;">₹{total}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Action Buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("🗑️ Clear Order", use_container_width=True):
                st.session_state.current_order = []
                st.success("Order cleared!")
                st.rerun()
        with col2:
            if st.button("💬 Chat with AI", use_container_width=True):
                st.session_state.active_page = "CHAT"
                st.rerun()
        with col3:
            if st.button("✅ Confirm Order", use_container_width=True):
                st.success("🎉 Order confirmed! Thank you for choosing It's HOT!")
                st.balloons()
    else:
        # Empty Order State
        st.markdown("""
        <div style="text-align: center; padding: 4rem 2rem;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">🛒</div>
            <h3 style="color: #4a5568; margin-bottom: 1rem;">Your cart is empty</h3>
            <p style="color: #718096; margin-bottom: 2rem;">Start adding items by chatting with our AI assistant or browse our menu!</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("💬 Start Ordering", use_container_width=True):
                st.session_state.active_page = "CHAT"
                st.rerun()

elif st.session_state.active_page == "MENU":
    st.markdown("### 📋 Complete Menu")
    
    # Menu sections
    menu_sections = {
        "☕ Coffee & Espresso": [
            {"name": "Cappuccino", "price": "₹250", "desc": "Rich espresso with foamed milk"},
            {"name": "Espresso Shot", "price": "₹150", "desc": "Pure, intense coffee experience"},
            {"name": "Latte", "price": "₹275", "desc": "Smooth espresso with steamed milk"},
            {"name": "Ouro Brasileiro Shot", "price": "₹200", "desc": "Strong, bold espresso shot"},
        ],
        "🍵 Tea Selection": [
            {"name": "Traditional Blend Chai", "price": "₹180", "desc": "Classic Indian spiced tea"},
            {"name": "Serenity Green Tea", "price": "₹200", "desc": "Light, calming green tea"},
            {"name": "English Breakfast", "price": "₹190", "desc": "Robust black tea"},
            {"name": "Earl Grey", "price": "₹200", "desc": "Citrus-flavored black tea"},
            {"name": "Morning Sunrise Chai", "price": "₹180", "desc": "Spiced tea to start your day"},
            {"name": "Peppermint", "price": "₹180", "desc": "Refreshing peppermint tea"},
            {"name": "Lemon Grass", "price": "₹180", "desc": "Aromatic lemongrass infusion"},
            {"name": "Spicy Eye Opener Chai", "price": "₹220", "desc": "Strong, spiced chai to wake you up"},
        ],
        "🥐 Bakery & Pastries": [
            {"name": "Oatmeal Scone", "price": "₹160", "desc": "Hearty oatmeal scone"},
            {"name": "Jumbo Savory Scone", "price": "₹200", "desc": "Large savory scone"},
            {"name": "Chocolate Chip Biscotti", "price": "₹150", "desc": "Crunchy chocolate chip biscotti"},
            {"name": "Ginger Biscotti", "price": "₹150", "desc": "Spiced ginger biscotti"},
            {"name": "Chocolate Croissant", "price": "₹220", "desc": "Flaky chocolate-filled croissant"},
            {"name": "Hazelnut Biscotti", "price": "₹150", "desc": "Nutty and crunchy biscotti"},
            {"name": "Cranberry Scone", "price": "₹180", "desc": "Sweet cranberry scone"},
            {"name": "Scottish Cream Scone", "price": "₹200", "desc": "Creamy Scottish-style scone"},
            {"name": "Croissant", "price": "₹180", "desc": "Classic buttery croissant"},
            {"name": "Almond Croissant", "price": "₹250", "desc": "Flaky croissant with almond filling"},
            {"name": "Ginger Scone", "price": "₹180", "desc": "Spicy ginger scone"},
        ],
        "🍯 Flavours & Syrups": [
            {"name": "Chocolate Syrup", "price": "₹120", "desc": "Rich chocolate syrup"},
            {"name": "Hazelnut Syrup", "price": "₹120", "desc": "Sweet hazelnut syrup"},
            {"name": "Caramel Syrup", "price": "₹130", "desc": "Smooth caramel syrup"},
            {"name": "Sugar Free Vanilla Syrup", "price": "₹120", "desc": "Vanilla syrup without sugar"},
        ],
        "🥶 Cold Beverages": [
            {"name": "Cold Brew", "price": "₹320", "desc": "Smooth, cold-extracted coffee"},
        ],
        "🍫 Drinking Chocolate": [
            {"name": "Dark Chocolate", "price": "₹300", "desc": "Rich and creamy dark chocolate"},
            {"name": "Chili Mayan", "price": "₹350", "desc": "Spicy Mayan-inspired chocolate drink"},
        ],
    }
    
    for section, items in menu_sections.items():
        st.markdown(f"#### {section}")
        cols = st.columns(3)
        for i, item in enumerate(items):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="menu-card">
                    <div class="coffee-name">{item['name']}</div>
                    <div class="coffee-price">{item['price']}</div>
                    <div class="coffee-description">{item['desc']}</div>
                </div>
                """, unsafe_allow_html=True)

elif st.session_state.active_page == "LOCATIONS":
    st.markdown("### 📍 Our Locations")
    st.info("Coming soon! We're expanding to serve you better.")

elif st.session_state.active_page == "ABOUT":
    st.markdown("### ℹ️ About It's HOT")
    st.markdown("""
    Welcome to It's HOT, where cutting-edge AI technology meets the timeless art of coffee making. 
    Our AI Barista is trained to understand your preferences and help you discover your perfect cup.
    
    **Our Mission**: To revolutionize the coffee experience through intelligent automation while preserving 
    the warmth and personal touch that makes every cup special.
    """)

elif st.session_state.active_page == "CONTACT":
    st.markdown("### 📞 Contact Us")
    st.markdown("""
    **Address**: 123 Coffee Street, Brew City  
    **Phone**: +1 (555) 123-COFFEE  
    **Email**: hello@beanandbot.com  
    **Hours**: Mon-Fri 6AM-10PM, Weekends 7AM-11PM
    """)

st.markdown('</div>', unsafe_allow_html=True)

# --- Footer ---
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #555; padding: 1rem;'>"
    "☕ Where AI meets Coffee Excellence • Designed by ASISH"
    "</div>",
    unsafe_allow_html=True
)
