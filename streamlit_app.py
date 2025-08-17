# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import pandas as pd  # for creating a small DataFrame to insert

# Connect to Snowflake
cnx = st.connection("snowflake")
session = cnx.session()

# Load available fruits
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# Streamlit UI
st.title("Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom smoothie!")

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)

# Prepare the ingredients string
ingredients_string = ''
if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)

time_to_insert = st.button('Submit Order')
st.write(ingredients_string)

if time_to_insert:
    insert_stmt = """
        INSERT INTO smoothies.public.orders (INGREDIENTS, NAME_ON_ORDER)
        VALUES (%s, %s)
    """
    cnx.execute(insert_stmt)
    st.success(f"Your smoothie is ordered, {name_on_order}!", icon="✅")

