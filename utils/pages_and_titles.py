import streamlit as st

def add_logo_and_set_page(layout = 'wide', page_title = 'Biz Metrics'):

    st.set_page_config(layout=layout, page_title=page_title)
    #st.set_page_config(layout=layout, page_title=page_title, page_icon='cleango-logo-small.png')
    #st.sidebar.markdown(f'![CleanGo Logo](https://cleango.hu/sitebuild/img/logo-text.svg)')

    st.sidebar.page_link("streamlit_app.py", label="Home", icon="🏠")

    st.sidebar.markdown("Import")
    st.sidebar.page_link("pages/import_page.py", label="Import", icon="🔵")

    st.sidebar.markdown("Registration - Statistics")
    st.sidebar.page_link("pages/registration_statistics.py", label="Registration Statistics", icon="🔵")
    
    st.sidebar.markdown("Purchase - Statistics")
    st.sidebar.page_link("pages/purchase_statistics.py", label="Purchase Statistics", icon="🔵")


def set_page(layout = 'wide', page_title = 'Biz Metrics'):

    st.set_page_config(layout=layout, page_title=page_title)
    # st.set_page_config(layout=layout, page_title=page_title, page_icon='cleango-logo-small.png')
    # st.sidebar.markdown(f'![CleanGo Logo](https://cleango.hu/sitebuild/img/logo-text.svg)')

    pages = {
        "Home": [st.Page("pages/home.py", title="Home", icon="🏠")],
        "Import": [st.Page("pages/import_page.py", title="Import data", icon="🔵")],
        "Registration": [st.Page("pages/registration_statistics.py", title="Registration Statistics", icon="🔵")],
        "Purchase": [st.Page("pages/purchase_statistics.py", title="Purchase Statistics", icon="🔵")]
    }
    pg = st.navigation(pages)
    pg.run()
