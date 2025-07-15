"""
Utilities Module.

This module provides utility functions that are used across the application,
such as creating download links for content and displaying content with
interactive actions like downloading and deleting.
"""

import streamlit as st
import base64
from datetime import datetime

def create_download_link(content, filename, content_type="text/markdown"):
    """
    Creates a download link for a given content.
    
    Args:
        content (str): The content to be made downloadable.
        filename (str): The name of the file to be downloaded.
        content_type (str, optional): The MIME type of the content. 
                                      Defaults to "text/markdown".
                                      
    Returns:
        str: An HTML anchor tag for the download link.
    """
    b64 = base64.b64encode(content.encode()).decode()
    return f'<a href="data:{content_type};base64,{b64}" download="{filename}" class="action-btn">📥 Download</a>'

def display_content_with_actions(content, title, content_type, note_id):
    """
    Displays content in a styled container with actions like download and delete.
    
    Args:
        content (str): The content to be displayed.
        title (str): The title to be shown in the content header.
        content_type (str): The type of content (e.g., "Summary", "Key Quotes").
        note_id (str): A unique identifier for the note to handle actions.
    """
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{content_type.lower().replace(' ', '_')}_{timestamp}.md"
    
    st.markdown(f"""
    <div class="content-display">
        <div class="content-header">
            <h3 class="content-title">{title}</h3>
            <div class="content-actions">
                {create_download_link(content, filename)}
            </div>
        </div>
        <div style="white-space: pre-wrap;">{content}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Delete button to remove the note from the session state
    if st.button(f"🗑️ Delete {content_type}", key=f"delete_{note_id}", help="Delete this note"):
        if f"note_{note_id}" in st.session_state:
            del st.session_state[f"note_{note_id}"]
            st.rerun()
