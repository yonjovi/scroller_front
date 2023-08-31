from json import JSONDecodeError
import streamlit as st
import requests
from streamlit_tags import st_tags
from streamlit_autorefresh import st_autorefresh

st.title('STOCK SCROLLER FRONT OF HOUSE')

URL = 'https://share-scroller.onrender.com/'
TICK_ADD_URL = 'https://test-api-evpk.onrender.com/get_ticker_data/'

tab1, tab2 = st.tabs(['Update Stock Scroller Gadget Tickers', 'How does the Stock Scroller Gadget work?'])
with tab1:
    r = requests.get(URL)

    results = r.json()
    maxtags = st.slider('Number of tickers allowed?', 1, 30, 30, key='jfnkerrnfvikwqejn')
    result_names = [result['name'] for result in results]

    if r.status_code == 200:
        ticker_selector = st_tags(
            label="Enter or Delete a share or crypto ticker:",
            text="Enter to add more",
            value=result_names,
            suggestions=['TSLA', 'BTC-USD', 'CBA.AX'],
            maxtags=maxtags,
            key='aljnf'
        )

        for i in results:
            if i['name'] not in ticker_selector:
                r = requests.delete(f'{URL}{i["id"]}')
                if r.status_code == 200:
                    st.warning(f'"{i["name"]}" was deleted from the scroller!')
                    r = requests.get(URL)
                    results = r.json()
                    result_names = [result['name'] for result in results]
                    refresh = st_autorefresh(interval=3000, limit=2, key='deleting_ticker')
                else:
                    st.write(r)

        st.write(result_names)
        for i in ticker_selector:
            if i not in result_names:
                try:
                    r = requests.get(f'{TICK_ADD_URL}{i}')
                    r_json = r.json()
                    i_price = r_json['results']['price']

                    r = requests.post(f'{URL}', json={'name': i, 'price': i_price})
                    if r.status_code == 200:
                        st.success(f'"{i}" was added to the scroller!')
                        r = requests.get(URL)
                        results = r.json()
                        result_names = [result['name'] for result in results]
                        refresh = st_autorefresh(interval=3000, limit=2, key='adding_ticker')
                    else:
                        st.write(r)
                except JSONDecodeError:
                    st.warning('It appears you are using an invalid ticker. Please check yourself and try again! Soz')
                except TypeError:
                    st.warning('It appears you are using an invalid ticker. Please check yourself and try again! Soz')
                except ValueError:
                    st.warning('It appears you are using an invalid ticker. Please check yourself and try again! Soz')
                finally:
                    refresh = st_autorefresh(interval=3000, limit=2, key='error')

with tab2:
    st.subheader('How does the Stock Scroller Gadget work?')
    st.video('https://www.youtube.com/watch?v=O7o5ezDHxTo')