import streamlit as st
import requests
from streamlit_ace import st_ace
from src.utils.logger import logger

st.set_page_config(
    page_title="Code Iterator AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

class CodeIteratorUI:
    def __init__(self):
        self.api_base_url = "http://localhost:8000/api"
        self.health_endpoint = f"{self.api_base_url}/health"
        self.suggest_code_endpoint = f"{self.api_base_url}/suggest-code"
        
        if 'current_code' not in st.session_state:
            st.session_state.current_code = ""
        if 'previous_code' not in st.session_state:
            st.session_state.previous_code = ""
        if 'current_prompt' not in st.session_state:
            st.session_state.current_prompt = ""
        if 'last_prompt' not in st.session_state:
            st.session_state.last_prompt = ""
        if 'api_result' not in st.session_state:
            st.session_state.api_result = None
        if 'force_editor_update' not in st.session_state:
            st.session_state.force_editor_update = False

    def check_api_health(self):
        try:
            response = requests.get(self.health_endpoint, timeout=5)
            return response.status_code == 200
        except:
            return False

    def render_header(self):
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0; background: linear-gradient(90deg, #1a1a1a 0%, #2d2d2d 100%); border-radius: 10px; margin-bottom: 2rem;">
            <h1 style="color: white; margin: 0; font-size: 2.5rem;">🚀 Code Iterator AI</h1>
            <p style="color: #e0e6ed; margin: 0.5rem 0 0 0; font-size: 1.1rem;">AI-powered code improvement tool for any programming language</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if self.check_api_health():
                st.success("✅ API is running and ready")
            else:
                st.error("❌ API is not running. Please start the FastAPI server first.")
        
        st.markdown("---")

    def render_sidebar(self):
        with st.sidebar:
            st.markdown("""
            <div style="background: linear-gradient(145deg, #2d3748, #4a5568); padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
                <h2 style="color: white; text-align: center; margin: 0;">ℹ️ About</h2>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            **Code Iterator AI** helps you improve your code using advanced AI.
            
            **✨ Features:**
            - 🤖 AI-powered code suggestions using Gemini 2.5 Flash
            - 🌐 Universal language support
            - 📊 Beautiful code diff visualization  
            - ✅ Seamless in-place code integration
            - 🔄 Iterative improvements with undo
            - 🎨 Dark-themed syntax-highlighted editor
            """)
            
            st.markdown("""
            <div style="background: linear-gradient(145deg, #2d3748, #4a5568); padding: 1rem; border-radius: 10px; margin: 1rem 0;">
                <h3 style="color: white; text-align: center; margin: 0;">🛠️ How to Use</h3>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            1. **✍️ Write/paste your code** in the dark editor
            2. **📝 Describe improvements** you want
            3. **🚀 Click 'Get AI Code Suggestion'**
            4. **👀 Review the enhanced results**
            5. **✅ Integrate changes** or use undo if needed
            """)
            
            st.markdown("---")
            
            if st.button("🔄 Check API Health", use_container_width=True):
                if self.check_api_health():
                    st.success("🎉 API is healthy and responsive!")
                else:
                    st.error("💥 API is not responding")

    def render_input_section(self):
        st.markdown("""
        <div style="background: linear-gradient(145deg, #1a202c, #2d3748); padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
            <h2 style="color: white; text-align: center; margin: 0;">📝 Universal Code Editor</h2>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.write("💻 Your Code")
            
            editor_key = "code_editor"
            if st.session_state.force_editor_update:
                editor_key = f"code_editor_{hash(st.session_state.current_code)}"
                st.session_state.force_editor_update = False
            
            current_code = st_ace(
                value=st.session_state.current_code,
                language='typescript',
                theme='dracula',
                key=editor_key,
                height=380,
                font_size=14,
                tab_size=4,
                show_gutter=True,
                show_print_margin=False,
                auto_update=True,
                wrap=False,
                placeholder="Write or paste your code here..."
            )
            
            if current_code != st.session_state.current_code:
                st.session_state.current_code = current_code
            
            col1_1, col1_2, col1_3 = st.columns([1, 1, 1])
            
            with col1_1:
                if st.session_state.previous_code and st.session_state.previous_code != st.session_state.current_code:
                    if st.button("↩️ Undo", help="Restore previous version", use_container_width=True):
                        st.session_state.current_code = st.session_state.previous_code
                        st.session_state.force_editor_update = True
                        st.success("✅ Previous version restored!")
                        st.rerun()
            
            with col1_2:
                if st.button("🗑️ Clear", use_container_width=True):
                    st.session_state.previous_code = st.session_state.current_code
                    st.session_state.current_code = ""
                    st.session_state.force_editor_update = True
                    st.rerun()
            
            with col1_3:
                if current_code:
                    lines = len(current_code.split('\n'))
                    chars = len(current_code)
                    st.markdown(f"<p style='font-size: 12px; text-align: center; margin-top: 8px;'>📊 {lines} Lines, {chars} Chars</p>", unsafe_allow_html=True)
        
        with col2:
            st.write("🎯 Improvement Request")
            
            user_prompt = st.text_area(
                label="What would you like to improve?",
                value=st.session_state.current_prompt,
                height=280,
                placeholder="""🎯 Describe your improvement goals:

                            🔧 Examples:
                            • Add comprehensive error handling
                            • Optimize for better performance  
                            • Improve code readability & comments
                            • Add type hints and documentation
                            • Implement design patterns
                            • Fix potential bugs and issues
                            • Add input validation
                            • Refactor for maintainability
                            • Add unit tests
                            • Improve security""",
                help="Be specific about what you want to improve",
                label_visibility="collapsed"
            )
            
            if user_prompt != st.session_state.current_prompt:
                st.session_state.current_prompt = user_prompt
            
            st.markdown("---")
            
            submit_button = st.button(
                "🚀 Get AI Code Suggestion",
                type="primary",
                use_container_width=True,
                help="Analyze and improve your code using AI"
            )
            
            if st.button("🗑️ Clear All", use_container_width=True):
                st.session_state.current_code = ""
                st.session_state.current_prompt = ""
                st.session_state.previous_code = ""
                st.session_state.api_result = None
                st.session_state.force_editor_update = True
                st.rerun()
        
        return current_code, user_prompt, submit_button

    def call_api(self, original_code: str, user_prompt: str):
        try:
            with st.spinner("🤖 AI is analyzing your code... Please wait"):
                response = requests.post(
                    self.suggest_code_endpoint,  
                    json={
                        "original_code": original_code,
                        "user_prompt": user_prompt
                    },
                    headers={"Content-Type": "application/json"},
                    timeout=120
                )
                
            if response.status_code == 200:
                result = response.json()
                logger.info("Successfully received API response")
                return result
            else:
                error_msg = f"API Error: {response.status_code}"
                try:
                    error_detail = response.json().get("detail", "Unknown error")
                    error_msg += f" - {error_detail}"
                except:
                    error_msg += f" - {response.text}"
                
                st.error(error_msg)
                logger.error(f"API error: {error_msg}")
                return None
                
        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to API. Make sure the FastAPI server is running on port 8000.")
            return None
        except requests.exceptions.Timeout:
            st.error("⏱️ Request timed out. The AI might be taking longer than usual. Please try again.")
            return None
        except requests.exceptions.RequestException as e:
            st.error(f"🔗 Connection Error: {str(e)}")
            logger.error(f"API call failed: {str(e)}")
            return None

    def render_results(self, result_data):
        if not result_data:
            return
            
        if not result_data.get("success"):
            st.error("❌ Failed to get code suggestions")
            if result_data.get("explanation"):
                st.error(f"Error: {result_data['explanation']}")
            return

        st.markdown("""
        <div style="background: linear-gradient(145deg, #1a202c, #2d3748); padding: 1rem; border-radius: 10px; margin: 1rem 0;">
            <h2 style="color: white; text-align: center; margin: 0;">✨ AI Code Improvement Results</h2>
        </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["🔧 Improved Code", "📊 Diff Analysis", "💡 AI Explanation"])
        
        with tab1:
            st.subheader("🎉 Enhanced Code")
            improved_code = result_data["improved_code"]
            
            st.code(improved_code, language="python", line_numbers=True)
            
            if st.button("✅ Integrate Into Editor", type="primary", use_container_width=True, key="integrate_btn"):
                st.session_state.previous_code = st.session_state.current_code
                st.session_state.current_code = improved_code
                st.session_state.force_editor_update = True
                st.session_state.api_result = None
                st.rerun()

        with tab2:
            st.subheader("📊 Code Changes Analysis")
            diff_data = result_data.get("diff", {})
            
            if diff_data.get("has_changes", False):
                changes = diff_data.get("changes_summary", {})
                
                metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                
                with metric_col1:
                    st.metric(
                        "➕ Lines Added", 
                        changes.get("lines_added", 0),
                        delta=f"+{changes.get('lines_added', 0)}" if changes.get('lines_added', 0) > 0 else None,
                        delta_color="normal"
                    )
                with metric_col2:
                    st.metric(
                        "➖ Lines Removed", 
                        changes.get("lines_removed", 0),
                        delta=f"-{changes.get('lines_removed', 0)}" if changes.get('lines_removed', 0) > 0 else None,
                        delta_color="inverse"
                    )
                with metric_col3:
                    st.metric("📄 Original Lines", changes.get("original_lines", 0))
                with metric_col4:
                    st.metric("📄 New Lines", changes.get("improved_lines", 0))
                
                diff_text = diff_data.get("diff_text", "")
                if diff_text and diff_text != "No changes detected":
                    with st.expander("🔍 Detailed Diff View", expanded=True):
                        st.code(diff_text, language="diff")
                else:
                    st.info("ℹ️ No detailed diff available.")
            else:
                st.info("ℹ️ No changes detected in the code.")

        with tab3:
            st.subheader("🤖 AI Analysis & Explanation")
            explanation = result_data.get("explanation", "No explanation available.")
            
            st.markdown("### 🎯 What was improved:")
            st.markdown(explanation)
            
            with st.expander("📝 Your Request Context", expanded=False):
                st.markdown(f"**Original Request:** {st.session_state.get('last_prompt', 'N/A')}")
                if st.session_state.previous_code:
                    st.markdown("**Previous Version Available:** ✅ Yes (use Undo to restore)")
                else:
                    st.markdown("**Previous Version Available:** ❌ No")

    def run(self):
        self.render_header()
        self.render_sidebar()
        
        original_code, user_prompt, submit_clicked = self.render_input_section()
        
        if submit_clicked:
            if not original_code.strip():
                st.warning("⚠️ Please enter some code to improve.")
                return
            elif not user_prompt.strip():
                st.warning("⚠️ Please describe what you want to improve.")
                return
            else:
                st.session_state.last_prompt = user_prompt
                
                result = self.call_api(original_code, user_prompt)
                if result:
                    st.session_state.api_result = result

        if st.session_state.api_result:
            self.render_results(st.session_state.api_result)

if __name__ == "__main__":
    app = CodeIteratorUI()
    app.run()
