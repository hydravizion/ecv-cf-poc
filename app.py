import streamlit as st
import json

# import zipfile as zf
from io import StringIO

st.subheader("Sorter and new data creation for language metadata")
lang_json = st.file_uploader(
    label="Input language files",
    type="json",
    accept_multiple_files=True,
)

if len(lang_json) > 0:
    key = st.text_input("Key for new data", value="(key)")
    input_arr = []
    for x in range(len(lang_json)):
        inp = st.text_area(
            label="New value for " + key + " in " + lang_json[x].name, key=x
        )
        input_arr.append(inp)

    # Print inputs
    # for i in input_arr:
    #     st.write(i)

    # Check if first time or language file changes
    if "lang_len" not in st.session_state or st.session_state.lang_len != len(
        lang_json
    ):
        # reset cache
        st.session_state.lang_len = len(lang_json)
        st.session_state.datas = []

        for index, lang in enumerate(lang_json):
            stringio = StringIO(lang.getvalue().decode("utf-8"))
            string_data = stringio.read()
            data = json.loads(string_data)
            st.session_state.datas.append(data)

    if st.button("Save to JSON"):
        temp = []
        for index, lang in enumerate(st.session_state.datas):
            lang[key] = input_arr[index]
            temp.append(lang)
        st.session_state.datas = temp

        st.experimental_rerun()

    st.write("""---""")
    for index, data in enumerate(st.session_state.datas):
        keys = list(data.keys())
        keys.sort()
        sorted = {i: data[i] for i in keys}
        col1, col2 = st.columns([3, 1])
        text = lang_json[index].name + " contains " + str(len(data)) + " pairs."
        col1.info(text)
        st.json(sorted, expanded=False)
        # for i in range(len(lang_json)):
        #     # for x,y in data.items():
        #     #     st.write(x,":",y)
        #     st.write("Sorted " + lang_json[i].name)
        #     st.write(sorted(data.items()))
        #     st.write("Data length: ", len(data))
        #     st.write("""---""")

        col2.download_button(
            label=("Download " + lang_json[index].name),
            data=json.dumps(sorted),
            key=lang_json[index].name,
            file_name=lang_json[index].name,
        )
        st.write("""---""")

    # st.download_button("Download", json_datas[0], file_name=lang_json[0].name)
    # zipObj = zf("all.zip", "w")
    # zipObj.write(json_datas[0])
    # zipObj.close()
    # st.download_button("down", zipObj)
