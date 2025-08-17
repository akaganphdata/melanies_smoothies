# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

cnx = st.connection("snowflake")
session = cnx.session()
# session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

# Write directly to the app
st.title("Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom smoothie!
  """
)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be: ', name_on_order)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections=5
)

# Prepare the ingredients string
ingredients_string = ''
if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)

time_to_insert = st.button('Submit Order')

if time_to_insert and ingredients_string and name_on_order:
    # Create a small Pandas DataFrame with one row to insert
    df_to_insert = pd.DataFrame({
        "ingredients": [ingredients_string],
        "name_on_order": [name_on_order]
    })

    # Write to Snowflake
    session.write_pandas(df_to_insert, "orders", table_type="BASE")  # appends row to orders table

    st.success(f'Your smoothie is ordered, {name_on_order}!', icon="✅")
