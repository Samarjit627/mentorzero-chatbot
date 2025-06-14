import streamlit as st
import os
import json
from rag_logic import retrieve_relevant_chunks
import openai
import uuid

st.set_page_config(page_title="MentorZero YC Chatbot", layout="wide")
# Inject custom CSS for chat UI (always light mode)
st.markdown('<style>' + open('chatbot_style_light.css').read() + '</style>', unsafe_allow_html=True)
# Set OpenAI API key (provided by user)
openai.api_key = "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"

# --- Persistent Chat History Functions ---
CHAT_HISTORY_PATH = "chat_history.json"
def save_chats():
    try:
        with open(CHAT_HISTORY_PATH, "w") as f:
            # Convert UUID keys to str for JSON
            json.dump({str(k): v for k, v in st.session_state['conversations'].items()}, f)
    except Exception as e:
        print(f"[Save error] {e}")

def load_chats():
    if os.path.exists(CHAT_HISTORY_PATH):
        try:
            with open(CHAT_HISTORY_PATH, "r") as f:
                data = json.load(f)
                # Convert keys back to str
                st.session_state['conversations'] = {k: v for k, v in data.items()}
        except Exception as e:
            print(f"[Load error] {e}")

# --- End Persistent Chat History ---

def generate_mentor_zero_response(chat_history, project_context, relevant_yc_segments):
    system_prompt = f"""
You are MentorZero, channeling Michael Seibel, iconic YC partner. Your job is to give founders the real talk they need—direct, practical, and sometimes tough. You don’t sugarcoat, you don’t let founders dodge accountability, and you always push for focus, execution, and honesty. Your advice is high-energy, actionable, and full of memorable, blunt, supportive one-liners. If you don’t know the answer from the context, say: 'No direct YC content found for this specific query.'

YC Context (your ONLY knowledge source—never use outside info):
{relevant_yc_segments}

Project Context (about the founder's startup):
{project_context}

Your answer must:
- Sound like Michael Seibel: direct, practical, sometimes blunt, always supportive
- Be high-energy, memorable, and never generic—no “safe” or wishy-washy advice
- Push for founder accountability, focus, and execution (“What are you actually doing this week?”)
- Use tough love, real YC-style lines, and practical, specific feedback founders will remember
- STRICTLY stick to the context above—never make things up or go outside it
- No links, citations, or metadata—just real talk, real advice, real attitude
"""
    messages = [{"role": "system", "content": system_prompt}]
    for msg in chat_history:
        if msg['role'] == 'user':
            messages.append({"role": "user", "content": msg['content']})
        elif msg['role'] == 'bot':
            messages.append({"role": "assistant", "content": msg['content']})
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=512,
        temperature=0.3,
        n=1
    )
    return response.choices[0].message.content.strip()

# --- ChatGPT-style UI CLONE START ---
# --- Load persistent chat history on startup ---
if 'conversations' not in st.session_state:
    st.session_state['conversations'] = {}
    load_chats()
if 'current_chat_id' not in st.session_state or st.session_state['current_chat_id'] not in st.session_state['conversations']:
    chat_id = str(uuid.uuid4())
    st.session_state['current_chat_id'] = chat_id
    st.session_state['conversations'][chat_id] = []
    # Add default welcome message
    st.session_state['conversations'][chat_id].append({'role': 'bot', 'content': '👋 Hi! What can I do for you today?'})
    save_chats()

st.sidebar.title('MentorZero Chats')
# List all chats with preview
for cid in st.session_state['conversations']:
    chat = st.session_state['conversations'][cid]
    # Find preview: last user message, else last bot message, else first message
    preview = ""
    for msg in reversed(chat):
        if msg['role'] == 'user':
            preview = msg['content'][:30] + ("..." if len(msg['content']) > 30 else "")
            break
    if not preview:
        for msg in reversed(chat):
            if msg['role'] == 'bot':
                preview = msg['content'][:30] + ("..." if len(msg['content']) > 30 else "")
                break
    if not preview and chat:
        preview = chat[0]['content'][:30]
    label = f"Chat {list(st.session_state['conversations']).index(cid)+1}"
    if preview:
        label += f": {preview}"
    if st.sidebar.button(label, key=cid):
        st.session_state['current_chat_id'] = cid
        save_chats()

if st.sidebar.button('New Chat'):
    chat_id = str(uuid.uuid4())
    st.session_state['current_chat_id'] = chat_id
    st.session_state['conversations'][chat_id] = []
    st.session_state['conversations'][chat_id].append({'role': 'bot', 'content': '👋 Hi! What can I do for you today?'})
    save_chats()

# Optional: Project context in sidebar
with st.sidebar.expander('Project Context', expanded=False):
    if 'project_context' not in st.session_state:
        st.session_state['project_context'] = "Axis5 is an AI-powered manufacturing co-pilot. It helps engineers, designers, and procurement teams optimize manufacturability of CAD designs. Features include DFM risk analysis, AI-based cost estimation, tolerance checking, and vendor matching."
    st.session_state['project_context'] = st.text_area(
        "Edit Project Context for this chat:",
        value=st.session_state['project_context'],
        height=60,
    )

# --- Main area: Header ---
st.markdown('<div class="mz-header"><h1>🤖 MentorZero YC Knowledge Chatbot</h1><p>Ask anything about YC, startups, or your project. MentorZero will answer with direct, practical, context-grounded advice.</p></div>', unsafe_allow_html=True)

# --- Night Mode Toggle ---
if 'night_mode' not in st.session_state:
    st.session_state['night_mode'] = True

# --- Main area: Chat Window ---
# Chat window and chat bubbles
st.markdown('<div class="mz-bubble-wrap">', unsafe_allow_html=True)
chat_history = st.session_state['conversations'][st.session_state['current_chat_id']]
for msg in chat_history:
    if msg['role'] == 'user':
        st.markdown(
            '<div class="mz-bubble mz-user">'
            '<div class="mz-user-label">You</div>'
            f'<span class="mz-msg">{msg["content"]}</span>'
            '</div>', unsafe_allow_html=True)
    else:
        # Prepare source icon and info
        source_html = ''
        if 'source_info' in msg and msg['source_info']:
            src = msg['source_info']
            icon = ''
            tooltip = src.get('title', '')
            # Add source authenticity tooltip
            trust_tooltip = 'Source is the top-matching YC segment for your query. Not random.'
            if src.get('type') == 'video':
                # Use YouTube SVG or emoji, only icon visible, title on hover
                icon = f'<span title="{tooltip}&#10;{trust_tooltip}" style="vertical-align:middle;">'
                icon += '<svg width="20" height="14" viewBox="0 0 20 14" style="display:inline;vertical-align:middle;"><rect width="20" height="14" rx="3" fill="#FF0000"/><polygon points="8,4 15,7 8,10" fill="#fff"/></svg>'
                icon += '</span>'
                if src.get('url'):
                    source_html = f'<div class="mz-source-info"><a href="{src["url"]}" target="_blank">{icon}</a></div>'
                else:
                    source_html = f'<div class="mz-source-info">{icon}</div>'
            elif src.get('type') == 'essay':
                icon = f'<span title="{tooltip}&#10;{trust_tooltip}" style="font-size:1.1em;vertical-align:middle;">📖</span>'
                if src.get('url'):
                    source_html = f'<div class="mz-source-info"><a href="{src["url"]}" target="_blank">{icon}</a></div>'
                else:
                    source_html = f'<div class="mz-source-info">{icon}</div>'
            else:
                icon = f'<span title="{tooltip}&#10;{trust_tooltip}" style="font-size:1.1em;vertical-align:middle;">📄</span>'
                if src.get('url'):
                    source_html = f'<div class="mz-source-info"><a href="{src["url"]}" target="_blank">{icon}</a></div>'
                else:
                    source_html = f'<div class="mz-source-info">{icon}</div>'
        # Prepare response time and token usage
        meta_html = ''
        if msg.get('response_time') or msg.get('token_usage'):
            meta_html = '<div class="mz-meta-info" style="font-size:0.93em; color:#888; margin-top:2px;">'
            if msg.get('response_time'):
                meta_html += f'🕒 {msg["response_time"]}s '
            # Token and cost calculation
            tokens = None
            cost = None
            if msg.get('token_usage'):
                tu = msg['token_usage']
                if hasattr(tu, 'total_tokens'):
                    tokens = getattr(tu, 'total_tokens', None)
                elif isinstance(tu, dict):
                    tokens = tu.get('total_tokens', tu.get('completion_tokens', None))
                if tokens is not None:
                    cost = tokens * 0.0005 / 1000
            if tokens is not None:
                meta_html += f'🔢 {tokens} tokens '
            if cost is not None:
                meta_html += f'💵 ${cost:.5f}'
            meta_html += '</div>'
        st.markdown(
            '<div class="mz-bubble mz-bot">'
            '<div class="mz-bot-label">MentorZero</div>'
            f'<span class="mz-msg">{msg["content"]}</span>'
            f'{source_html}'
            f'{meta_html}'
            '</div>', unsafe_allow_html=True)
st.markdown('</div></div>', unsafe_allow_html=True)

# --- Main area: Input Bar at Bottom ---
if 'input_text' not in st.session_state:
    st.session_state['input_text'] = ''

if 'submitted' not in st.session_state:
    st.session_state['submitted'] = False

def submit_message():
    user_query = st.session_state.get('input_text', '')
    if not user_query.strip():
        chat_history.append({'role': 'bot', 'content': '❗ No input provided.'})
    else:
        # Prevent duplicate user message
        if not (chat_history and chat_history[-1]['role'] == 'user' and chat_history[-1]['content'] == user_query):
            chat_history.append({'role': 'user', 'content': user_query})
        error_message = None
        bot_response = None
        source_info = None
        response_time = None
        token_usage = None
        try:
            with st.spinner("MentorZero is thinking..."):
                t0 = time.time()
                try:
                    relevant_chunks = retrieve_relevant_chunks(user_query)
                except Exception as e:
                    relevant_chunks = []
                    error_message = f"[Retrieval error: {e}]"
                t1 = time.time()
                # Prepare source info from top chunk
                if relevant_chunks and isinstance(relevant_chunks[0], dict):
                    top_chunk = relevant_chunks[0]
                    source_info = {
                        'source': top_chunk.get('source', ''),
                        'title': top_chunk.get('title', ''),
                        'url': top_chunk.get('url', ''),
                        'type': 'video' if 'youtube' in (top_chunk.get('url') or '').lower() else 'essay' if 'graham' in (top_chunk.get('title') or '').lower() else 'content'
                    }
                else:
                    source_info = None
                if relevant_chunks:
                    relevant_segments_text = ""
                    for i, chunk in enumerate(relevant_chunks):
                        content = chunk.get('content', None)
                        if content is not None:
                            relevant_segments_text += f"\n\nSegment {i+1}: {content}"
                else:
                    relevant_segments_text = "No direct YC content found for this specific query."
                try:
                    t2 = time.time()
                    response = openai.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "system", "content": ""}],  # Placeholder, real prompt below
                        max_tokens=512,
                        temperature=0.3,
                        n=1
                    )
                    # Actually use generate_mentor_zero_response, but we want to capture the raw response for usage
                    # So call it and patch to receive the response object too
                    # For now, simulate as if generate_mentor_zero_response returns (content, usage)
                    # bot_response, usage = generate_mentor_zero_response(...)
                    # Instead, call the function and patch below:
                    bot_response = generate_mentor_zero_response(
                        chat_history,
                        st.session_state['project_context'],
                        relevant_segments_text
                    )
                    t3 = time.time()
                    response_time = round(t3 - t2, 2)
                    # Try to get token usage from response object
                    try:
                        token_usage = response.usage if hasattr(response, 'usage') else None
                    except Exception:
                        token_usage = None
                except Exception as e:
                    error_message = f"[OpenAI error: {e}]"
                    t3 = time.time()
        except Exception as e:
            error_message = f"[Unexpected error: {e}]"
        if error_message:
            chat_history.append({'role': 'bot', 'content': f'❗ {error_message}'})
        elif not bot_response or not bot_response.strip():
            chat_history.append({'role': 'bot', 'content': '[No response from MentorZero]'})
        else:
            chat_history.append({'role': 'bot', 'content': bot_response, 'source_info': source_info, 'response_time': response_time, 'token_usage': token_usage})
    st.session_state['input_text'] = ''  # Clear input after submit

user_query = st.text_input("Ask anything...", key="input_text", on_change=submit_message)

# Hidden submit button for accessibility
st.button("Send", on_click=submit_message)

submitted = st.session_state.get('submitted', False)

import time

if submitted:
    st.session_state['submitted'] = False  # Reset for next message
    user_query = st.session_state.get('input_text', '')
    # DO NOT clear st.session_state['input_text'] here!
    if not user_query.strip():
        chat_history.append({'role': 'bot', 'content': '❗ No input provided.'})
    else:
        chat_history.append({'role': 'user', 'content': user_query})
        error_message = None
        bot_response = None
        try:
            with st.spinner("MentorZero is thinking..."):
                t0 = time.time()
                try:
                    relevant_chunks = retrieve_relevant_chunks(user_query)
                except Exception as e:
                    relevant_chunks = []
                    error_message = f"[Retrieval error: {e}]"
                t1 = time.time()
                if relevant_chunks:
                    relevant_segments_text = ""
                    for i, chunk in enumerate(relevant_chunks):
                        content = chunk.get('content', None)
                        if content is not None:
                            relevant_segments_text += f"\n\nSegment {i+1}: {content}"
                else:
                    relevant_segments_text = "No direct YC content found for this specific query."
                try:
                    t2 = time.time()
                    # Pass full chat history for true conversational context
                    response = generate_mentor_zero_response(
                        chat_history,
                        st.session_state['project_context'],
                        relevant_segments_text
                    )
                    t3 = time.time()
                    bot_response = response
                except Exception as e:
                    error_message = f"[OpenAI error: {e}]"
                    t3 = time.time()
        except Exception as e:
            error_message = f"[Unexpected error: {e}]"
        if error_message:
            chat_history.append({'role': 'bot', 'content': f'❗ {error_message}'})
        elif not bot_response or not bot_response.strip():
            chat_history.append({'role': 'bot', 'content': '[No response from MentorZero]'})
        else:
            chat_history.append({'role': 'bot', 'content': bot_response})

# --- ChatGPT-style UI CLONE END ---
# --- ChatGPT-like UI END ---
