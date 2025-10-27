import streamlit as st
import tempfile
import os
from pathlib import Path
from doc_proofreader.proofread_document import proofread_document
from doc_proofreader.proofread_document_inline import proofread_document_with_track_changes_mac
from doc_proofreader.llm.client_factory import ClientFactory

st.set_page_config(
    page_title="Doc Proofreader",
    page_icon="📝",
    layout="wide"
)

st.title("📝 Doc Proofreader")
st.markdown("AI-powered document proofreading with multiple language models")

# Sidebar for settings
with st.sidebar:
    st.header("⚙️ Settings")

    # Provider selection
    provider = st.selectbox(
        "Provider",
        ["openai", "openrouter"],
        help="Select the LLM provider"
    )

    # Model selection based on provider
    if provider == "openai":
        model = st.selectbox(
            "Model",
            ["gpt-4o", "gpt-4o-mini"],
            help="Select the AI model"
        )
    else:  # openrouter
        model = st.selectbox(
            "Model",
            [
                "gpt-5-mini",
                "gemini-2.5-pro",
                "gpt-4o",
                "gpt-4o-mini",
                "claude-3.5-sonnet",
                "claude-3-opus",
                "claude-3-haiku",
                "gemini-1.5-pro",
                "gemini-1.5-flash",
                "llama-3.1-70b",
                "mixtral-8x7b"
            ],
            help="Select the AI model from OpenRouter"
        )

    st.divider()

    # Mode selection
    mode = st.radio(
        "Proofreading Mode",
        ["📋 List corrections", "✏️ Edit inline"],
        help="List mode shows corrections, Inline mode directly edits the document"
    )

    # Custom instructions
    st.divider()
    custom_instructions = st.text_area(
        "Custom Instructions (optional)",
        placeholder="E.g., 'Use British English', 'Focus on grammar only'",
        height=100
    )

# Main content area
col1, col2 = st.columns([3, 2])

with col1:
    uploaded_file = st.file_uploader(
        "Upload your Word document",
        type=['docx'],
        help="Currently supports .docx files only"
    )

    if uploaded_file is not None:
        st.success(f"✅ File uploaded: {uploaded_file.name}")

        # Display file info
        file_size = uploaded_file.size / 1024  # Convert to KB
        st.info(f"📄 File size: {file_size:.1f} KB")

with col2:
    if uploaded_file:
        st.markdown("### Ready to proofread")
        st.markdown(f"**Provider:** {provider}")
        st.markdown(f"**Model:** {model}")
        st.markdown(f"**Mode:** {'Inline editing' if '✏️' in mode else 'Corrections list'}")

# Process button
if uploaded_file:
    if st.button("🚀 Start Proofreading", type="primary", use_container_width=True):
        try:
            # Create a progress indicator
            progress_bar = st.progress(0)
            status_text = st.empty()

            # Save uploaded file to temporary location
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir) / uploaded_file.name
                with open(temp_path, 'wb') as f:
                    f.write(uploaded_file.read())

                status_text.text("Processing document...")
                progress_bar.progress(40)

                # Process based on mode
                inline_mode = "✏️" in mode

                if inline_mode:
                    # Inline editing mode - returns file path
                    output_path = proofread_document_with_track_changes_mac(
                        document_path=str(temp_path),
                        additional_instructions=custom_instructions if custom_instructions else "",
                        provider=provider,
                        model=model
                    )
                    status_text.text("Applying corrections...")
                    progress_bar.progress(80)

                    # Read the output file for download
                    with open(output_path, 'rb') as f:
                        output_data = f.read()

                    output_filename = f"corrected_{uploaded_file.name}"
                    mime_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

                else:
                    # List corrections mode - returns text content
                    corrections_text = proofread_document(
                        document_path=str(temp_path),
                        additional_instructions=custom_instructions if custom_instructions else "",
                        provider=provider,
                        model=model
                    )
                    status_text.text("Generating corrections list...")
                    progress_bar.progress(80)

                    # Use the text content directly
                    output_data = corrections_text.encode('utf-8')
                    output_filename = f"corrections_{uploaded_file.name.replace('.docx', '.txt')}"
                    mime_type = "text/plain"

                progress_bar.progress(100)
                status_text.text("✅ Proofreading complete!")

                # Success message
                st.success("🎉 Proofreading completed successfully!")

                # Download button
                st.download_button(
                    label=f"⬇️ Download {output_filename}",
                    data=output_data,
                    file_name=output_filename,
                    mime=mime_type,
                    type="primary"
                )

                # Show preview for corrections mode
                if not inline_mode:
                    with st.expander("📋 Preview Corrections", expanded=True):
                        st.text_area("Corrections found:", corrections_text, height=200)

                # Display some stats
                st.markdown("### Summary")
                if inline_mode:
                    st.info("✏️ Document has been corrected with inline edits")
                else:
                    st.info("📋 Corrections list has been generated")

        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            st.exception(e)

else:
    # Instructions when no file is uploaded
    st.markdown("### 👋 How to use")
    st.markdown("""
    1. **Upload** your Word document (.docx) using the file uploader
    2. **Configure** your settings in the sidebar (provider, model, mode)
    3. **Add** custom instructions if needed (optional)
    4. **Click** 'Start Proofreading' to process your document
    5. **Download** the corrected document or corrections list
    """)

    st.markdown("### 🌟 Features")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        - 🤖 Multiple AI models (GPT-4, Claude, Gemini)
        - 📝 Two modes: List corrections or edit inline
        - 🎯 Custom instructions support
        """)
    with col2:
        st.markdown("""
        - 📊 OpenAI and OpenRouter support
        - 💾 Download corrected documents
        - 🚀 Fast parallel processing
        """)

# Footer
st.divider()
st.markdown(
    "<center>Made with ❤️ using Streamlit | Doc Proofreader v1.2.0</center>",
    unsafe_allow_html=True
)