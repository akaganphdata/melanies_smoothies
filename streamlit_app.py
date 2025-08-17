# Import Python packages
import streamlit as st
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col

# Connect to Snowflake
cnx = st.connection("snowflake")
session = cnx.session()

# Load available fruits from Snowflake table
fruit_df = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
fruit_list = [row['FRUIT_NAME'] for row in fruit_df.collect()]

# Streamlit UI
st.title("Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom smoothie!")

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruit_list,
    max_selections=5
)

# Only proceed if user selected ingredients and entered a name
if ingredients_list and name_on_order:
    ingredients_string = ' '.join(ingredients_list)

    # Button to submit order
    if st.button('Submit Order'):
        # Create a Snowpark DataFrame for the new order
        order_df = session.create_dataframe(
            [(ingredients_string, name_on_order)],
            schema=["INGREDIENTS", "NAME_ON_ORDER"]  # must match Snowflake table exactly
        )

        # Append the new row to the existing orders table
        order_df.write.mode("append").save_as_table("smoothies.public.orders")

        st.success(f'Your smoothie is ordered, {name_on_order}!', icon="✅")
else:
    if not name_on_order:
        st.info("Please enter a name for your smoothie.")
    if not ingredients_list:
        st.info("Please select at least one ingredient.")
