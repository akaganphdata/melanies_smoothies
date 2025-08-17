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

time_to_insert = st.button('Submit Order')

if time_to_insert:
    df_to_insert = pd.DataFrame({
    "INGREDIENTS": [' '.join(ingredients_list)],
    "NAME_ON_ORDER": [name_on_order]
    })

    session.write_pandas(
        df_to_insert,
        table_name="orders",
        schema="public",
        database="smoothies"
    )
    st.success(f"Your smoothie is ordered, {name_on_order}!", icon="✅")

