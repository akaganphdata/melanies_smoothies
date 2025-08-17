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

if time_to_insert and ingredients_string and name_on_order:
    df_to_insert = pd.DataFrame({
        "INGREDIENTS": [ingredients_string],
        "NAME_ON_ORDER": [name_on_order]
    })

    # Convert to Snowpark DataFrame
    order_df = session.create_dataframe(df_to_insert)

    # Append to table
    order_df.write.mode("append").save_as_table("smoothies.public.orders")
    st.success(f'Your smoothie is ordered, {name_on_order}!', icon="✅")
