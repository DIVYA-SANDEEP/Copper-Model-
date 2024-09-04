import streamlit as st
from streamlit_option_menu import option_menu
import numpy as np
from PIL import Image
import warnings
warnings.filterwarnings("ignore")
import pickle
import pandas as pd

#set up page configuration for streamlit
icon='https://st2.depositphotos.com/1000128/7250/i/450/depositphotos_72503649-stock-photo-copper-pipes.jpg'
st.set_page_config(page_title='Industrial copper',page_icon=icon,initial_sidebar_state='expanded',layout='wide')

#set up the sidebar with optionmenu
with st.sidebar:
    selected = option_menu("MainMenu",
                            options=["Home","Get Prediction"],
                            icons=["house","lightbulb"],
                            default_index=1,
                            orientation="vertical",)
    
#user input values for selectbox and encoded for respective features
class option():
    
    country_values=[ 25.,  26.,  27.,  28.,  30.,  32.,  38.,  39.,  40.,  77.,  78., 79.,  80.,  84.,  89., 107., 113.]

    status_values=['Won', 'Draft', 'To be approved', 'Lost', 'Not lost for AM','Wonderful', 'Revised',
            'Offered', 'Offerable']

    status_encoded = {'Lost':0, 'Won':1, 'Draft':2, 'To be approved':3, 'Not lost for AM':4,'Wonderful':5, 'Revised':6,
                    'Offered':7, 'Offerable':8}
    
    item_type_values=['W', 'WI', 'S', 'Others', 'PL', 'IPL', 'SLAWR']

    item_type_encoded = {'W':5.0, 'WI':6.0, 'S':3.0, 'Others':1.0, 'PL':2.0, 'IPL':0.0, 'SLAWR':4.0}

    application_values=[2.0, 3.0, 4.0, 5.0, 10.0, 15.0, 19.0, 20.0, 22.0, 25.0, 26.0, 27.0, 28.0, 29.0, 38.0, 39.0, 40.0,
                41.0, 42.0, 56.0, 58.0, 59.0, 65.0, 66.0, 67.0, 68.0, 69.0, 70.0, 79.0, 99.0]
    
    product_ref_values=[611728, 611733, 611993, 628112, 628117, 628377, 640400, 640405, 640665, 164141591, 164336407,
                164337175, 929423819, 1282007633, 1332077137, 1665572032, 1665572374, 1665584320, 1665584642,
                1665584662, 1668701376, 1668701698, 1668701718, 1668701725, 1670798778, 1671863738, 1671876026,
                1690738206, 1690738219, 1693867550, 1693867563, 1721130331, 1722207579]

#set up information for the 'get prediction' menu
if selected == 'Get Prediction':
    title_text = '''<h1 style='font-size: 32px;text-align: center;color:grey;'>Copper Selling Price and Status Prediction</h1>'''
    st.markdown(title_text, unsafe_allow_html=True)
    
    #set up option menu for selling price and status menu
    select=option_menu('',options=["Selling Price","Status"],
                                    icons=["cash", "toggles"],
                                    orientation='horizontal',)
    
    if select == 'Selling Price':
        st.markdown("<h5 style=color:grey>To predict the selling price of copper, please provide the following information:",unsafe_allow_html=True)
        st.write('')

        # creted form to get the user input 
        with st.form('prediction'):
            col1,col2=st.columns(2)
            with col1:
                country=st.selectbox(label='Country',options=option.country_values,index=None)
                item_type=st.selectbox(label='Item Type',options=option.item_type_values,index=None)
                application=st.selectbox(label='Application',options=option.application_values,index=None)
                product_ref=st.selectbox(label='Product Ref',options=option.product_ref_values,index=None)
                st.write('<p style="font-size:12px;">Minimum value Customer = 10000</p>', unsafe_allow_html=True)
                customer=st.text_input('Customer ID')


            with col2:
                status=st.selectbox(label='Status',options=option.status_values,index=None)
                st.write('<p style="font-size:12px;">Minimum value Quantity = 0.1</p>', unsafe_allow_html=True)
                quantity=st.text_input(label='Quantity')
                st.write('<p style="font-size:12px;">Minimum value Width = 1.0</p>', unsafe_allow_html=True)
                width=st.text_input(label='Width')
                st.write('<p style="font-size:12px;">Minimum value Thickness = 0.1</p>', unsafe_allow_html=True)
                thickness=st.text_input(label='Thickness')
                st.markdown('<br>', unsafe_allow_html=True)
                button=st.form_submit_button('PREDICT',use_container_width=True)

        if button:
            #check whether user fill all required fields
            if not all([country, item_type, application, product_ref,
                        customer, status, quantity, width, thickness]):
                st.error("Please fill in all required fields.")

            else:
                
                #opened pickle model and predict the selling price with user data
                with open('Regression.pkl','rb') as files:
                    predict_model=pickle.load(files)

                # customize the user data to fit the feature 
                status=option.status_encoded[status]
                item_type=option.item_type_encoded[item_type]
                quantity = float(quantity)
                thickness = float(thickness)
                quantity_log=np.log(quantity)
                thickness_log=np.log(thickness)

                #predict the selling price with regressor model
                user_data=np.array([[customer, country, status, item_type ,application, width, product_ref,quantity_log, thickness_log ]])
                pred=predict_model.predict(user_data)
                selling_price=np.exp(pred[0])
                rounded_predicted_selling_price = round(selling_price, 3)


                #display the predicted selling price 
                st.write(f'**Predicted Selling Price : :green[₹] :green[{rounded_predicted_selling_price}]**')
    if select == 'Status':
        st.markdown("<h5 style=color:grey;>To predict the status of copper, please provide the following information:",unsafe_allow_html=True)
        st.write('')

        #creted form to get the user input 
        with st.form('classifier'):
            col1,col2=st.columns(2)
            with col1:
                country=st.selectbox(label='Country',options=option.country_values,index=None)
                item_type=st.selectbox(label='Item Type',options=option.item_type_values,index=None)
                application=st.selectbox(label='Application',options=option.application_values,index=None)
                product_ref=st.selectbox(label='Product Ref',options=option.product_ref_values,index=None)
                st.write('<p style="font-size:12px;">Minimum value Customer = 10000</p>', unsafe_allow_html=True)
                customer=st.text_input('Customer ID')

            with col2:
                st.write('<p style="font-size:12px;">Minimum value Quantity = 0.1</p>', unsafe_allow_html=True)
                quantity=st.text_input(label='Quantity')
                st.write('<p style="font-size:12px;">Minimum value Width = 1.0</p>', unsafe_allow_html=True)
                width=st.text_input(label='Width')
                st.write('<p style="font-size:12px;">Minimum value Thickness = 0.1</p>', unsafe_allow_html=True)
                thickness=st.text_input(label='Thickness')
                selling_price=st.text_input(label='Selling Price')
                st.markdown('<br>', unsafe_allow_html=True)
                button=st.form_submit_button('PREDICT',use_container_width=True)

        if button:
            #check whether user fill all required fields
            if not all([country, item_type, application, product_ref,
                        customer,quantity, width, thickness,selling_price]):
                st.error("Please fill in all required fields.")

            else:
                #opened pickle model and predict status with user data
                with open('Classification_Model.pkl','rb') as files:
                    model=pickle.load(files)

                # customize the user data to fit the feature 
                item_type=option.item_type_encoded[item_type]
                quantity = float(quantity)
                thickness = float(thickness)
                selling_price = float(selling_price)
                quantity_log=np.log(quantity)
                thickness_log=np.log(thickness)
                quantity_log=np.log(quantity)
                thickness_log=np.log(thickness)
                selling_price_log=np.log(selling_price)

                #predict the status with classifier model
                user_data=np.array([[customer, country, item_type ,application, width, product_ref,quantity_log, thickness_log, selling_price_log ]])
                
                status=model.predict(user_data)

                if status==1:
                    st.subheader(f":green[Status of the copper : ] Won")
                else:
                    st.subheader(f":red[Status of the copper :] Lost")   

if selected == "Home":
    title_text = '''<h1 style='font-size: 30px;text-align: center; color:grey;'>INDUSTRIAL COPPER</h1>'''
    st.markdown(title_text, unsafe_allow_html=True)
    st.subheader(':blue[Domain :]')
    st.markdown('<h5> Manufacturing ',unsafe_allow_html=True)

    st.subheader(':blue[Skills & Technologies :]')
    st.markdown('<h5> Python scripting, Data Preprocessing, Machine learning, EDA, Streamlit ',unsafe_allow_html=True)

    st.subheader(':blue[Overview :]')
    st.markdown('''  <h5>Data Preprocessing:   
                <li>Loaded the copper CSV into a DataFrame.            
                <li>Cleaned and filled missing values, addressed outliers, and adjusted data types.  <br>           
                <li>Analyzed data distribution and treated skewness.''',unsafe_allow_html=True)
    st.markdown(''' <h5>Feature Engineering: 
                <li>Assessed feature correlation to identify potential multicollinearity ''',unsafe_allow_html=True)
    st.markdown('''<h5>Modeling: 
                <li >Built a regression model for selling price prediction.
                <li>Built a classification model for status prediction.
                <li>Encoded categorical features and optimized hyperparameters.
                <li>Pickled the trained models for deployment.''',unsafe_allow_html=True)
    st.markdown('''<h5>Streamlit Application:
                <li>Developed a user interface for interacting with the models.
                <li>Predicted selling price and status based on user input.''',unsafe_allow_html=True)

