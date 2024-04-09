import streamlit as st
import pickle

with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

def predict_class(params):
    menopause_status = {
        "Premenopausal": 0,
        "Postmenopausal or age>=55": 1,
        "Unknown": 9
    }
    menopause = menopause_status.get(params['menopaus'].iloc[0], None)

    age_groups = {
        "35-39": 1,
        "40-44": 2,
        "45-49": 3,
        "50-54": 4,
        "55-59": 5,
        "60-64": 6,
        "65-69": 7,
        "70-74": 8,
        "75-79": 9,
        "80-84": 10
    }
    for age_range, value in age_groups.items():
        start, end = map(int, age_range.split('-'))
        if start <= params['agegrp'].iloc[0] <= end:
            age = value

    density_codes = {
        "Almost entirely fat": 1,
        "Scattered fibroglandular densities": 2,
        "Heterogeneously dense": 3,
        "Extremely dense": 4,
        "Unknown or different measurement system": 9
    }
    density = density_codes.get(params['density'].iloc[0], None)

    race_mapping = {
        "White": 1,
        "Asian/Pacific Islander": 2,
        "Black": 3,
        "Native American": 4,
        "Other/Mixed": 5,
        "Unknown": 9
    }
    race = race_mapping.get(params['race'].iloc[0], None)

    hispanic_mapping = {
        "No": 0,
        "Yes": 1,
        "Unknown": 9
    }
    hispanic = hispanic_mapping.get(params['Hispanic'].iloc[0], None)

    bmi_val = params['bmi'].iloc[0]
    if bmi_val < 10:
        bmi = None
    elif 10 <= bmi_val < 25:
        bmi = 1
    elif 25 <= bmi_val < 30:
        bmi = 2
    elif 30 <= bmi_val < 35:
        bmi = 3
    elif bmi_val >= 35:
        bmi = 4
    else:
        bmi = 9

    age_first_mapping = {
        "Age < 30": 0,
        "Age 30 or greater": 1,
        "Nulliparous": 2,
        "Unknown": 9
    }
    age_at_first_birth = age_first_mapping.get(params['agefirst'].iloc[0], None)

    num_rel_mapping = {
        "zero": 0,
        "one": 1,
        "2 or more": 2,
        "Unknown": 9
    }
    num_relatives = num_rel_mapping.get(params['nrelbc'].iloc[0], None)

    brstproc_mapping = {
        "No": 0,
        "Yes": 1,
        "Unknown": 9
    }
    previous_procedure = brstproc_mapping.get(params['brstproc'].iloc[0], None)

    last_mamm_mapping = {
        "Negative": 0,
        "False positive": 1,
        "Unknown": 9
    }
    last_mammogram_result = last_mamm_mapping.get(params['lastmamm'].iloc[0], None)

    surgical_meno_mapping = {
        "Natural": 0,
        "Surgical": 1,
        "Unknown or not menopausal": 9
    }
    surgical_menopause = surgical_meno_mapping.get(params['surgmeno'].iloc[0], None)

    ht_mapping = {
        "No": 0,
        "Yes": 1,
        "Unknown or not menopausal": 9
    }
    hormone_therapy = ht_mapping.get(params['hrt'].iloc[0], None)

    if None in [menopause, age, density, race, hispanic, age_at_first_birth, num_relatives, previous_procedure,
                last_mammogram_result, surgical_menopause, hormone_therapy]:
        st.write("Invalid input! Please check your input values.")
        return "Unknown"
    
    predicted_class = model.predict([[menopause, age, density, race, hispanic, bmi,
                                      age_at_first_birth, num_relatives, previous_procedure,
                                      last_mammogram_result, surgical_menopause, hormone_therapy]])

    predicted_class_mapping = {
        0: "No Breast Cancer",
        1: "Breast Cancer Detected"
    }

    return predicted_class_mapping.get(predicted_class[0], "Unknown")
