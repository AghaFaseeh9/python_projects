import streamlit as st


def convert_unit(value, convert_from, convert_to):
    conversions = {
        "meter_kilometer": 0.001,
        "kilometer_meter": 1000,
        "gram_kilogram": 0.001,
        "kilogram_gram": 1000,
    }
    key = f"{convert_from}_{convert_to}"
    if key in conversions:
       conversion = conversions[key]
       return value * conversion
    else:
        return f"Conversion not supported"


# Streamlit ui:
st.title("Unit Converter")
value = st.number_input("Enter the Value you want to convert", min_value=1.0, step=1.0)
convert_from = st.selectbox(
    "Select the unit from which you want to convert",
    ["meter", "kilometer", "gram", "kilogram"],
)
convert_to = st.selectbox(
    "Select the unit to which you want to convert",
    ["meter", "kilometer", "gram", "kilogram"],
)
result = convert_unit(value, convert_from, convert_to)
if st.button("Convert"):
    st.success(f"The converted Value is {result}")
