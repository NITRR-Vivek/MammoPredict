import streamlit as st
import pandas as pd
import pickle

st.set_page_config("MammoPredict", page_icon="👑",layout="wide")

with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

def predict_class(params):
    predicted_class = model.predict(params)
    return predicted_class

def main():
    st.title('Breast Cancer Prediction')
    st.subheader('Input Parameters')
    predicted_class = None

    menopaus = st.slider('Menopausal Status', min_value=0, max_value=10)
    agegrp = st.slider('Age Group', min_value=0, max_value=10)
    density = st.slider('Density', min_value=0, max_value=10)
    race = st.slider('Race', min_value=0, max_value=10)
    Hispanic = st.slider('Hispanic', min_value=0, max_value=10)
    bmi = st.slider('BMI', min_value=0, max_value=10)
    agefirst = st.slider('Age at First Birth', min_value=0, max_value=10)
    nrelbc = st.slider('Number of Relatives with Breast Cancer', min_value=0, max_value=10)
    brstproc = st.slider('Breast Procedures', min_value=0, max_value=10)
    lastmamm = st.slider('Time Since Last Mammogram', min_value=0, max_value=10)
    surgmeno = st.slider('Age at Surgical Menopause', min_value=0, max_value=10)
    hrt = st.slider('Hormone Replacement Therapy', min_value=0, max_value=10)

    input_values = {
        'menopaus': menopaus,
        'agegrp': agegrp,
        'density': density,
        'race': race,
        'Hispanic': Hispanic,
        'bmi': bmi,
        'agefirst': agefirst,
        'nrelbc': nrelbc,
        'brstproc': brstproc,
        'lastmamm': lastmamm,
        'surgmeno': surgmeno,
        'hrt': hrt
    }

    if 'data' not in st.session_state:
        st.session_state['data'] = pd.DataFrame(columns=['menopaus', 'agegrp', 'density', 'race', 'Hispanic', 'bmi',
                                                          'agefirst', 'nrelbc',
                                                          'brstproc', 'lastmamm', 'surgmeno',
                                                          'hrt', 'Predicted Result'])

    if st.button('Predict'):
        input_df = pd.DataFrame(input_values, index=[0])
        predicted_class = predict_class(input_df)
        input_df['Predicted Result'] = predicted_class
        st.session_state['data'] = pd.concat([st.session_state['data'], input_df], ignore_index=True)

    if st.button('Clear Data'):
        st.session_state['data'] = pd.DataFrame(columns=['menopaus', 'agegrp', 'density', 'race', 'Hispanic', 'bmi',
                                                          'agefirst', 'nrelbc',
                                                          'brstproc', 'lastmamm', 'surgmeno',
                                                          'hrt', 'Predicted Result'])

    st.subheader(f'Predicted Result: {predicted_class}')
    st.subheader('Data')
    st.dataframe(st.session_state['data'])

if __name__ == '__main__':
    main()
