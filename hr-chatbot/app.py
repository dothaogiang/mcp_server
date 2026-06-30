# app.py
import asyncio
import os

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

from mcp_client import list_mcp_tools, call_mcp_tool

load_dotenv()

st.set_page_config(page_title="HR Chatbot (MCP test)", page_icon="🗂️")
st.title("HR Chatbot — test kết nối MCP")

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
MODEL = "gemini-2.5-pro"

SYSTEM_PROMPT = (
    "Bạn là trợ lý tra cứu hồ sơ lưu trữ nhân sự. "
    "Dùng các tool được cung cấp để tìm kiếm, lấy chi tiết hồ sơ, "
    "hồ sơ cán bộ, file, hoặc tìm kiếm ngữ nghĩa (rag_query) khi cần. "
    "Trả lời bằng tiếng Việt, ngắn gọn, dựa trên dữ liệu tool trả về."
)

if "mcp_tools" not in st.session_state:
    with st.spinner("Đang kết nối MCP server..."):
        try:
            st.session_state.mcp_tools = asyncio.run(list_mcp_tools())
        except Exception as e:
            st.error(f"Không kết nối được MCP server: {e}")
            st.session_state.mcp_tools = []

if st.session_state.mcp_tools:
    with st.expander(f"Đã tải {len(st.session_state.mcp_tools)} tool từ MCP server"):
        for t in st.session_state.mcp_tools:
            first_line = t["description"].strip().splitlines()[0] if t["description"] else ""
            st.write(f"- **{t['name']}**: {first_line}")

gemini_tools = [types.Tool(function_declarations=st.session_state.mcp_tools)] if st.session_state.mcp_tools else None

if "history" not in st.session_state:
    st.session_state.history = []  # list[types.Content]
if "display_messages" not in st.session_state:
    st.session_state.display_messages = []  # chỉ để hiển thị trên UI

for m in st.session_state.display_messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])


def run_agent_turn(user_text: str):
    st.session_state.history.append(
        types.Content(role="user", parts=[types.Part(text=user_text)])
    )

    while True:
        response = client.models.generate_content(
            model=MODEL,
            contents=st.session_state.history,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                tools=gemini_tools,
            ),
        )

        candidate = response.candidates[0]

        if candidate.content is None or not candidate.content.parts:
            reason = getattr(candidate, "finish_reason", "UNKNOWN")
            return f"Gemini không trả về nội dung (finish_reason={reason}). Thử lại hoặc kiểm tra prompt/tool schema."

        st.session_state.history.append(candidate.content)

        function_calls = [
            part.function_call for part in candidate.content.parts if part.function_call
        ]

        if not function_calls:
            final_text = "".join(
                part.text for part in candidate.content.parts if part.text
            )
            return final_text or "(Không có nội dung text trả về)"

        response_parts = []
        for fc in function_calls:
            with st.spinner(f"Đang gọi tool `{fc.name}`..."):
                try:
                    result_text = asyncio.run(call_mcp_tool(fc.name, dict(fc.args)))
                except Exception as e:
                    result_text = f"Lỗi khi gọi tool: {e}"
            response_parts.append(
                types.Part.from_function_response(
                    name=fc.name, response={"result": result_text}
                )
            )

        st.session_state.history.append(types.Content(role="user", parts=response_parts))

user_input = st.chat_input("Hỏi về hồ sơ, cán bộ, tài liệu...")
if user_input:
    st.session_state.display_messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    with st.chat_message("assistant"):
        with st.spinner("Đang xử lý..."):
            answer = run_agent_turn(user_input)
        st.markdown(answer)
    st.session_state.display_messages.append({"role": "assistant", "content": answer})