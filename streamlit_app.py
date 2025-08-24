# Import python packages
import streamlit as st
import pandas as pd
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
#sf_df = st.dataframe(data=my_dataframe, use_container_width = True)
#st.stop()

# Convert the Snowpark Dataframe to a Pandas Dataframe so we could use the LOC function 
pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

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
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
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



