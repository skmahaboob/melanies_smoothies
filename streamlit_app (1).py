# import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie!:cup_with_straw:")
st.write(
    """Choose the fruits you want in your custome Smoothie!
    """
)

name_on_order = st.text_input('Name on Smoothie')
st.write('The Name on Your Smoothie will be ', name_on_order)

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose upto 5 Ingredients :'
    , my_dataframe
    , max_selections=5
)
if ingredients_list :

    ingredients_string=''
    for each_fruit in ingredients_list:
        ingredients_string+=each_fruit +' '
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    #st.write(my_insert_stmt)
    #st.stop()

    time_to_submit=st.button("Submit Order")
    if time_to_submit:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")


