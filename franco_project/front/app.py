import streamlit as st

class App:
    def pages(self) -> list[st.Page]:
        pages = [
            st.Page("./pages/manager.py", title="Gerenciar", icon=":material/bookmark_manager:"),
            st.Page("./pages/prompt.py", title="Prompt", icon=":material/robot_2:")
        ]
        return pages
    
    def render(self):
        pg = st.navigation(self.pages(), position="top")
        pg.run()

if __name__ == "__main__":
    App().render()