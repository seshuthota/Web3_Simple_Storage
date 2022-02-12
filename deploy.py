import streamlit as st

from deploy_initializer import execute_retrieve, add_person, get_peoples

if st.button("Retrieve Fav Number"):
    result = execute_retrieve()
    st.write("Retrieved Fav number!")
    st.write(result)

form = st.form(key="add_person")
person_name = form.text_input("Enter Person Name", value="")
person_fav_number = form.text_input("Enter Fav Number", value="")
submit = form.form_submit_button("Add")
if submit:
    add_person(person_name, person_fav_number)
    form.empty()
    person_name = ""
    person_fav_number = ""

if st.button("Get All Persons"):
    st.write("List of People And Fav number")
    st.write(get_peoples())
