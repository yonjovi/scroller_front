from json import JSONDecodeError
import streamlit as st
import requests
from streamlit_tags import st_tags
from streamlit_autorefresh import st_autorefresh

st.title("TASL SCROLLER FRONT OF HOUSE")

URL = "https://task-api-qc0t.onrender.com/"
TICK_ADD_URL = "https://test-api-evpk.onrender.com/get_ticker_data/"

r = requests.get(URL)

results = r.json()
result_names = [result['task'] for result in results]

if r.status_code == 200:
    task_selector = st_tags(
        label="Enter or Delete a share or reminder:",
        text="Enter to add more",
        value=result_names,
        suggestions=['Feed the cat', 'Get Milk', 'Get Coffee', 'Book Flights', 'Coding exercises', 'Book gigs'],
        key='aljnf'
    )

    for i in results:
        if i['task'] not in task_selector:
            r = requests.delete(f'{URL}{i["id"]}')
            if r.status_code == 200:
                st.warning(f'"{i["task"]}" was deleted from the scroller!')
                r = requests.get(URL)
                results = r.json()
                result_names = [result['task'] for result in results]
                refresh = st_autorefresh(interval=3000, limit=2, key='deleting_ticker')
            else:
                st.write(r)

    st.write(result_names)
    for i in task_selector:
        if i not in result_names:
            try:
                r = requests.post(f'{URL}', json={"task": i})
                if r.status_code == 200:
                    st.success(f'"{i}" was added to the scroller!')
                    r = requests.get(URL)
                    results = r.json()
                    result_names = [result['task'] for result in results]
                    refresh = st_autorefresh(interval=3000, limit=2, key='adding_ticker')
                else:
                    st.write(r)
            except JSONDecodeError:
                st.warning("It appears you are using an invalid ticker. Please check yourself and try again! Soz")
            except TypeError:
                st.warning("It appears you are using an invalid ticker. Please check yourself and try again! Soz")
            except ValueError:
                st.warning("It appears you are using an invalid ticker. Please check yourself and try again! Soz")
            finally:
                refresh = st_autorefresh(interval=3000, limit=2, key='error')
