import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
streamlit.title ("My Parents healthy diner")

streamlit.header('Breakfast Menu')
streamlit.text('🥣Omega 3 & Blueberry Oatmeal')
streamlit.text(' 🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 🥑 🍞 Hard-Boiled Free-Range Egg')


streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show=my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

#create function
def get_fruity_vice_date(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" +this_fruit_choice)
      # Get data in table normalized form 
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
      # store in dataframe
    return fruityvice_normalized

streamlit.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
      streamlit.error("Please select fruit")
    else:
      back_from_funtion=get_fruity_vice_date(fruit_choice)
      streamlit.dataframe(back_from_funtion)
    
except URLError as e:
    streamlit.error()

streamlit.header("The fruit List contains:")

#snowflake button function
def get_fruit_load_list():
    my_cur = my_cnx.cursor()
    #my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
    my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
    return my_cur.fetchall()
#Add a button to load
if streamlit.button('Get fruit List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows=get_fruit_load_list()
    streamlit.dataframe(my_data_rows)

# Allow the end user to add a fruit to the list
def insert_row_snowflake (new_fruit):
    with my_cnx.cursor () as my_cur:
        my_cur.execute("insert into fruit_load_list values ('from streamlit')") 
        return "Thanks for adding " + new_fruit

add_my_fruit=streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the List'):
    my_cnx = snowflake.connector.connect (**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake (add_my_fruit)
    streamlit.text (back_from_function)
    

streamlit.stop()
fruit_choice1 = streamlit.text_input('What fruit would you like to add?','Kiwi')
streamlit.write('Thanks for adding ', fruit_choice1)

my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('from streamlit')")

