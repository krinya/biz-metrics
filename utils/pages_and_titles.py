import streamlit as st


def set_page(layout = 'wide', page_title = 'Biz Metrics'):

    st.set_page_config(layout=layout, page_title=page_title)
    # st.set_page_config(layout=layout, page_title=page_title, page_icon='cleango-logo-small.png')
    # st.sidebar.markdown(f'![CleanGo Logo](https://cleango.hu/sitebuild/img/logo-text.svg)')

    pages = {
        "Home": [st.Page("screens/home.py", title="Home", icon="🏠")],
        "Sample Datasets": [st.Page("screens/sample_datasets.py", title="Sample Datasets", icon="🔵")],
        "Import": [st.Page("screens/import_page.py", title="Import data", icon="🔵")],
        "Registration": [st.Page("screens/registration_statistics.py", title="Registration Statistics", icon="🔵")],
        "Transaction": [st.Page("screens/transaction_statistics.py", title="Transaction Statistics", icon="🔵")],
        "User": [st.Page("screens/user_statistics.py", title="User Statistics", icon="🔵")],
    }
    pg = st.navigation(pages)
    pg.run()


def add_logo_and_set_page(layout = 'wide', page_title = 'Biz Metrics'):

    st.set_page_config(layout=layout, page_title=page_title)
    #st.set_page_config(layout=layout, page_title=page_title, page_icon='cleango-logo-small.png')
    #st.sidebar.markdown(f'![CleanGo Logo](https://cleango.hu/sitebuild/img/logo-text.svg)')

    st.sidebar.page_link("streamlit_app.py", label="Home", icon="🏠")

    st.sidebar.markdown("Import")
    st.sidebar.page_link("screens/import_page.py", label="Import", icon="🔵")

    st.sidebar.markdown("Registration - Statistics")
    st.sidebar.page_link("screens/registration_statistics.py", label="Registration Statistics", icon="🔵")
    
    st.sidebar.markdown("Purchase - Statistics")
    st.sidebar.page_link("screens/purchase_statistics.py", label="Purchase Statistics", icon="🔵")
