import os
import re
import streamlit as st
import numpy as np
from sentence_transformers import SentenceTransformer, util
import torch

# Configuration
DEFAULT_REPO_PATH = r"G:\bsc"
MODEL_NAME = "all-MiniLM-L6-v2"
EXCLUDE_DIRS = {'MinGW64', '.git', '.vscode', 'bin', 'obj', 'Debug', 'Release', '__pycache__', '.idea'}

# --- Cache the AI Model so it loads only once ---
@st.cache_resource
def load_model(model_name):
    return SentenceTransformer(model_name)

class CodeSearchEngine:
    def __init__(self, model_name=MODEL_NAME):
        # Use the cached model
        self.model = load_model(model_name)
        self.file_paths = []
        self.code_contents = []
        self.embeddings = None

    def preprocess_code(self, text):
        """
        Removes boilerplate license headers but KEEPS useful comments/descriptions.
        """
        license_markers = ["COPYRIGHT", "ACADEMIC INTEGRITY", "RIGHTS RESERVED", "LICENSE", "DO NOT COPY"]
        
        def filter_comment(match):
            comment_text = match.group(0)
            if any(marker in comment_text.upper() for marker in license_markers):
                return ""
            return comment_text

        # Regex to find block comments and filter them conditionally
        text = re.sub(r'/\*.*?\*/', filter_comment, text, flags=re.DOTALL)
        return " ".join(text.split())

    def load_local_files(self, directory):
        """
        Walks through the local directory and loads .c files.
        Returns a status string and success boolean.
        """
        if not os.path.exists(directory):
            return f"Error: Directory '{directory}' not found.", False

        self.file_paths = []
        self.code_contents = []
        count = 0
        
        # Create a progress bar in the UI
        progress_bar = st.progress(0)
        status_text = st.empty()
        status_text.text(f"Scanning {directory}...")

        # Walk through the directory tree
        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            
            for file in files:
                if file.endswith(".c"):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            raw_content = f.read()
                        
                        clean_content = self.preprocess_code(raw_content)
                        
                        if not clean_content.strip():
                            continue

                        rel_path = os.path.relpath(file_path, directory)
                        self.file_paths.append(rel_path)
                        self.code_contents.append({"raw": raw_content, "clean": clean_content})
                        count += 1
                        
                        # Update status occasionally to avoid UI lag
                        if count % 10 == 0:
                            status_text.text(f"Found {count} files...")
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")
        
        progress_bar.empty()
        status_text.empty()
        return f"Successfully loaded {count} C files.", True

    def build_index(self):
        """
        Generates embeddings. Returns status string.
        """
        if not self.code_contents:
            return "No code to index."

        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(device)
        
        clean_texts = [item["clean"] for item in self.code_contents]
        
        with st.spinner(f" indexing {len(clean_texts)} files on {device.upper()}..."):
            self.embeddings = self.model.encode(clean_texts, convert_to_tensor=True)
        
        return "Indexing complete!"

    def search(self, query, top_k=3):
        """
        Returns a list of result dictionaries.
        """
        if self.embeddings is None:
            return []

        query_embedding = self.model.encode(query, convert_to_tensor=True)
        cos_scores = util.cos_sim(query_embedding, self.embeddings)[0]
        top_results = torch.topk(cos_scores, k=min(top_k, len(self.code_contents)))

        results = []
        for score, idx in zip(top_results.values, top_results.indices):
            idx = idx.item()
            raw_content = self.code_contents[idx]["raw"]
            
            # Smart Preview Logic (Same as before)
            header_match = re.match(r'^\s*/\*.*?\*/', raw_content, flags=re.DOTALL)
            start_index = 0
            if header_match:
                header_text = header_match.group(0)
                if any(marker in header_text.upper() for marker in ["COPYRIGHT", "ACADEMIC INTEGRITY", "LICENSE"]):
                    start_index = header_match.end()
            
            body_text = raw_content[start_index:].strip()
            preview_lines = body_text.splitlines()[:15] # Show a bit more lines in UI
            preview_text = "\n".join(preview_lines)

            results.append({
                "file": self.file_paths[idx],
                "score": score.item(),
                "preview": preview_text,
                "full_code": raw_content
            })
        return results

# --- Main Streamlit App ---
def main():
    st.set_page_config(page_title="BSC Code Search", page_icon="🔍", layout="wide")
    
    st.title("⚡ BSC Code Neural Search")
    st.markdown("Search your C repository using **AI embeddings** instead of just keywords.")

    # initialize session state for the engine
    if 'engine' not in st.session_state:
        st.session_state['engine'] = CodeSearchEngine()
        st.session_state['indexed'] = False

    engine = st.session_state['engine']

    # --- Sidebar for Configuration ---
    with st.sidebar:
        st.header("⚙️ Settings")
        repo_path = st.text_input("Repository Path", value=DEFAULT_REPO_PATH)
        
        if st.button("🔄 Scan & Index Code", type="primary"):
            msg, success = engine.load_local_files(repo_path)
            if success:
                st.success(msg)
                idx_msg = engine.build_index()
                st.success(idx_msg)
                st.session_state['indexed'] = True
            else:
                st.error(msg)
        
        st.markdown("---")
        st.markdown(f"**Status:** {'🟢 Ready' if st.session_state['indexed'] else '🔴 Not Indexed'}")
        if st.session_state['indexed']:
            st.metric("Files Indexed", len(engine.file_paths))

    # --- Main Search Interface ---
    query = st.text_input("Describe the code you need:", placeholder="e.g., how to multiply two matrices or sort an array")

    if query:
        if not st.session_state['indexed']:
            st.warning("Please click 'Scan & Index Code' in the sidebar first.")
        else:
            results = engine.search(query, top_k=3)
            
            st.markdown(f"### Results for: *{query}*")
            
            for i, res in enumerate(results):
                with st.expander(f"📄 {res['file']} (Confidence: {res['score']:.2f})", expanded=(i==0)):
                    st.markdown(f"**Preview:**")
                    st.code(res['preview'], language='c')
                    
                    if st.checkbox(f"Show Full File #{i+1}", key=f"check_{i}"):
                        st.code(res['full_code'], language='c')

if __name__ == "__main__":
    main()