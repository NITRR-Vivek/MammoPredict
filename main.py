import streamlit as st
import pandas as pd
import predictor2

st.set_page_config("MammoPredict", page_icon="👑", layout="wide")

def main():
    st.title('Breast Cancer Prediction')
    st.subheader('Input Parameters')
    predicted_class = None

    menopause = st.selectbox("Select menopause status:", options=["Premenopausal", "Postmenopausal or age>=55", "Unknown"])
    age = st.number_input("Enter your age:", min_value=0, max_value=120, value=35, step=1)
    density = st.selectbox('BI-RADS breast density:',options=["Almost entirely fat","Scattered fibroglandular densities","Heterogeneously dense" ,"Extremely dense" ,"Unknown or different measurement system"])
    race = st.selectbox('Race:',options=["White","Asian/Pacific Islander","Black","Native American","Other/Mixed","Unknown"])
    hispanic = st.selectbox('Hispanic:',options=["No","Yes","Unknown"])
    bmi = st.number_input('Enter BMI:', min_value=10.0, max_value=100.0,value=25.0,step=0.1)
    age_at_first_birth = st.selectbox('Age at First Birth:', options=["Age < 30","Age 30 or greater","Nulliparous","Unknown"])
    num_relatives = st.selectbox('Number of First Degree Relatives with Breast Cancer:', options=["zero","one","2 or more","Unknown"])
    previous_procedure = st.selectbox('Previous Breast Procedures:',options=["No","Yes","Unknown"])
    last_mammogram_result = st.selectbox('Last Mammogram Result:',options=["Negative","False positive","Unknown"])
    surgical_menopause = st.selectbox('Surgical Menopause:', options=["Natural","Surgical","Unknown or not menopausal"])
    hormone_therapy = st.selectbox('Current Hormone Therapy:',options=["No","Yes","Unknown or not menopausal"])

    input_values = {
        'menopaus': menopause,
        'agegrp': age,
        'density': density,
        'race': race,
        'Hispanic': hispanic,
        'bmi': bmi,
        'agefirst': age_at_first_birth,
        'nrelbc': num_relatives,
        'brstproc': previous_procedure,
        'lastmamm': last_mammogram_result,
        'surgmeno': surgical_menopause,
        'hrt': hormone_therapy
    }

    if 'data' not in st.session_state:
        st.session_state['data'] = pd.DataFrame(columns=['menopaus', 'agegrp', 'density', 'race', 'Hispanic', 'bmi',
                                                          'agefirst', 'nrelbc',
                                                          'brstproc', 'lastmamm', 'surgmeno',
                                                          'hrt', 'Predicted Result'])
    st.markdown("<hr>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)  # Split the layout into two columns
    with col1:
        if st.button('Predict Breast Cancer'):
            input_df = pd.DataFrame(input_values, index=[0])
            predicted_class = predictor2.predict_class(input_df)
            input_df['Predicted Result'] = predicted_class
            st.session_state['data'] = pd.concat([st.session_state['data'], input_df.dropna(axis=1)], ignore_index=True)
            st.session_state['data'].index += 1 

    with col2:
        if st.button('Clear Outputs', type='primary'):
            st.session_state['data'] = pd.DataFrame(columns=['menopaus', 'agegrp', 'density', 'race', 'Hispanic', 'bmi',
                                                              'agefirst', 'nrelbc',
                                                              'brstproc', 'lastmamm', 'surgmeno',
                                                              'hrt', 'Predicted Result'])
    if predicted_class == "No Breast Cancer":
        st.success(f'Predicted Result: {predicted_class}')
    elif predicted_class == "Breast Cancer Detected":
        st.error(f'Predicted Result: {predicted_class}')
    else:
        st.info(f'Predicted Result: {predicted_class}')

    st.subheader('Data')
    st.dataframe(st.session_state['data'])
    # st.table(st.session_state['data'])

if __name__ == '__main__':
    main()
