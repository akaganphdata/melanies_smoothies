# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col, lit

# Connect to Snowflake
cnx = st.connection("snowflake")
session = cnx.session()

# Streamlit UI
st.title("Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom smoothie!")

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# Load available fruits
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
st.stop()

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)

# Prepare the ingredients string
ingredients_string = ''
if ingredients_list:
    #ingredients_string = ' '.join(ingredients_list)
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutrition Information') 
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width = True)

time_to_insert = st.button('Submit Order')

if time_to_insert:
    st.write(ingredients_string)
    st.write(name_on_order)
    insert_stmt = f"""
        INSERT INTO SMOOTHIES.PUBLIC.ORDERS (INGREDIENTS, NAME_ON_ORDER)
        VALUES ('{ingredients_string}', '{name_on_order}')""" 
    st.write(insert_stmt)
    session.sql(insert_stmt).to_pandas()
    st.success(f"Your smoothie is ordered, {name_on_order}!", icon="✅")



