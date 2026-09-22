import streamlit as st
from PIL import Image

from crop_disease import predict_disease
from crop_recommendation import recommend_crop
from fertilizer_recommendation import recommend_fertilizer
from crop_yield import predict_crop_yield
from mandi_price import predict_mandi_price

# ==========================================
# Page Configuration
# ==========================================

st.set_page_config(
    page_title="Bharat Krishi Intelligence System",
    page_icon="🌾",
    layout="wide"
)

# ==========================================
# Sidebar Navigation
# ==========================================

st.sidebar.title("🌾 BKIS")

st.sidebar.write(
    "Bharat Krishi Intelligence System"
)

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"


def go_to(page_name):
    st.session_state.page = page_name

# ==========================================
# Dashboard
# ==========================================

if st.session_state.page == "Dashboard":

    st.title(
        "🌾 Bharat Krishi Intelligence System"
    )

    st.write(
        "An AI-powered agricultural intelligence "
        "platform for intelligent farming decisions."
    )

    st.divider()

    st.subheader("Agricultural Intelligence Services")

    # --------------------------------------
    # First Row
    # --------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🔬 Crop Disease Detection")

        st.write(
            "Identify crop diseases from leaf images "
            "using deep learning."
        )

        if st.button(
            "Open Crop Disease →",
            key="open_disease",
            use_container_width=True
        ):
            go_to("Crop Disease")
            st.rerun()

    with col2:

        st.subheader("🌱 Crop Recommendation")

        st.write(
            "Get suitable crop recommendations based "
            "on soil and weather conditions."
        )

        if st.button(
            "Open Crop Recommendation →",
            key="open_crop",
            use_container_width=True
        ):
            go_to("Crop Recommendation")
            st.rerun()


    st.write("")


    # --------------------------------------
    # Second Row
    # --------------------------------------

    col3, col4 = st.columns(2)

    with col3:

        st.subheader("🧪 Fertilizer Recommendation")

        st.markdown(
            """
            <div style="height: 56px;">
                Find the most suitable fertilizer based on crop,
                soil and environmental conditions.
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Open Fertilizer Recommendation →",
            key="open_fertilizer",
            use_container_width=True
        ):
            go_to("Fertilizer Recommendation")
            st.rerun()


    with col4:

        st.subheader("🌾 Crop Yield Prediction")

        st.markdown(
            """
            <div style="height: 56px;">
                Predict expected crop yield using agricultural
                and environmental data.
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Open Crop Yield →",
            key="open_yield",
            use_container_width=True
        ):
            go_to("Crop Yield")
            st.rerun()

    # --------------------------------------
    # Third Row
    # --------------------------------------
    
    st.write("")
    
    col5, col6 = st.columns(2)
    
    with col5:
    
        st.subheader("💰 Mandi Price Prediction")
    
        st.write(
            "Predict the expected modal mandi price "
            "of agricultural commodities."
        )
    
        if st.button(
            "Open Mandi Price →",
            key="open_mandi",
            use_container_width=True
        ):
            go_to("Mandi Price")
            st.rerun()


    st.divider()

    st.caption(
        "Bharat Krishi Intelligence System (BKIS)"
    )

    
# ==========================================
# Crop Disease Page
# ==========================================

elif st.session_state.page == "Crop Disease":

    if st.button(
        "← Back to Dashboard",
        key="back_disease"
    ):
        go_to("Dashboard")
        st.rerun()

    st.title("🔬 Crop Disease Detection")

    st.markdown(
    """
    <div style="min-height: 56px;">
        Identify crop diseases from leaf images using
        deep learning.
    </div>
    """,
    unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Upload Crop Image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:

        st.image(
            uploaded_file,
            caption="Uploaded Crop Image",
            use_container_width=True
        )

    # ==========================================
    # Disease Prediction & Validation
    # ==========================================

    if st.button(
        "Predict Disease",
        key="disease_button"
    ):

        try:

            # ----------------------------------
            # Validate Uploaded File
            # ----------------------------------

            if uploaded_file is None:

                st.warning(
                    "Please upload a crop leaf image first."
                )

            else:

                # ----------------------------------
                # Open Image
                # ----------------------------------

                image = Image.open(
                    uploaded_file
                )

                # ----------------------------------
                # Validate Image
                # ----------------------------------

                if image.width == 0 or image.height == 0:

                    st.warning(
                        "The uploaded image is invalid."
                    )

                else:

                    # ----------------------------------
                    # Prediction
                    # ----------------------------------

                    predicted_class, confidence = (
                        predict_disease(image)
                    )

                    st.success(
                        f"Predicted Disease: "
                        f"{predicted_class}"
                    )

                    st.metric(
                        "Confidence",
                        f"{confidence * 100:.2f}%"
                    )

        except Exception as e:

            st.error(
                "Unable to process the uploaded image. "
                "Please upload a valid crop leaf image."
            )

            st.caption(
                f"Technical details: {e}"
        )

# ==========================================
# Crop Recommendation Page
# ==========================================

elif st.session_state.page == "Crop Recommendation":

    if st.button(
        "← Back to Dashboard",
        key="back_crop"
    ):
        go_to("Dashboard")
        st.rerun()

    st.title("🌱 Crop Recommendation")

    st.markdown(
    """
    <div style="min-height: 56px;">
        Get suitable crop recommendations based on soil
        and weather conditions.
    </div>
    """,
    unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        nitrogen = st.number_input(
            "Nitrogen (N)",
            min_value=0.0,
            value=90.0,
            key="crop_nitrogen"
        )

        phosphorus = st.number_input(
            "Phosphorus (P)",
            min_value=0.0,
            value=42.0,
            key="crop_phosphorus"
        )

        potassium = st.number_input(
            "Potassium (K)",
            min_value=0.0,
            value=43.0,
            key="crop_potassium"
        )

    with col2:

        temperature = st.number_input(
            "Temperature (°C)",
            value=20.88,
            key="crop_temperature"
        )

        humidity = st.number_input(
            "Humidity (%)",
            min_value=0.0,
            max_value=100.0,
            value=82.0,
            key="crop_humidity"
        )

    with col3:

        ph = st.number_input(
            "Soil pH",
            min_value=0.0,
            max_value=14.0,
            value=6.50,
            key="crop_ph"
        )

        rainfall = st.number_input(
            "Rainfall (mm)",
            min_value=0.0,
            value=202.94,
            key="crop_rainfall"
        )

    # ==========================================
    # Crop Recommendation Validation & Prediction
    # ==========================================

    if st.button(
        "🌱 Recommend Crop",
        key="crop_button"
    ):

        # --------------------------------------
        # Validate Nutrient Values
        # --------------------------------------

        if nitrogen < 0:

            st.warning(
                "Nitrogen cannot be negative."
            )

        elif phosphorus < 0:

            st.warning(
                "Phosphorus cannot be negative."
            )

        elif potassium < 0:

            st.warning(
                "Potassium cannot be negative."
            )

        # --------------------------------------
        # Validate Temperature
        # --------------------------------------

        elif temperature < -50 or temperature > 70:

            st.warning(
                "Please enter a valid temperature "
                "between -50°C and 70°C."
            )

        # --------------------------------------
        # Validate Humidity
        # --------------------------------------

        elif humidity < 0 or humidity > 100:

            st.warning(
                "Humidity must be between 0% and 100%."
            )

        # --------------------------------------
        # Validate pH
        # --------------------------------------

        elif ph < 0 or ph > 14:

            st.warning(
                "Soil pH must be between 0 and 14."
            )

        # --------------------------------------
        # Validate Rainfall
        # --------------------------------------

        elif rainfall < 0:

            st.warning(
                "Rainfall cannot be negative."
            )

        # --------------------------------------
        # Prediction
        # --------------------------------------

        else:

            try:

                recommended_crop = recommend_crop(
                    nitrogen,
                    phosphorus,
                    potassium,
                    temperature,
                    humidity,
                    ph,
                    rainfall
                )

                st.success(
                    f"Recommended Crop: "
                    f"{recommended_crop}"
                )

            except Exception as e:

                st.error(
                    "Unable to make the crop recommendation. "
                    "Please check your inputs."
                )

                st.caption(
                    f"Technical details: {e}"
                )

# ==========================================
# Fertilizer Recommendation Page
# ==========================================

elif st.session_state.page == "Fertilizer Recommendation":

    if st.button(
        "← Back to Dashboard",
        key="back_fertilizer"
    ):
        go_to("Dashboard")
        st.rerun()

    st.title("🧪 Fertilizer Recommendation")

    st.markdown(
    """
    <div style="min-height: 56px;">
        Find the most suitable fertilizer based on crop,
        soil and environmental conditions.
    </div>
    """,
    unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        fertilizer_temperature = st.number_input(
            "Temperature (°C)",
            value=28.0,
            key="fert_temperature"
        )

        moisture = st.number_input(
            "Moisture",
            min_value=0.0,
            value=45.0,
            key="fert_moisture"
        )

        fertilizer_rainfall = st.number_input(
            "Rainfall (mm)",
            min_value=0.0,
            value=120.0,
            key="fert_rainfall"
        )

    with col2:

        fertilizer_ph = st.number_input(
            "Soil pH",
            min_value=0.0,
            max_value=14.0,
            value=6.5,
            key="fert_ph"
        )

        fertilizer_nitrogen = st.number_input(
            "Nitrogen",
            min_value=0.0,
            value=80.0,
            key="fert_nitrogen"
        )

        phosphorous = st.number_input(
            "Phosphorous",
            min_value=0.0,
            value=45.0,
            key="fert_phosphorous"
        )

    with col3:

        fertilizer_potassium = st.number_input(
            "Potassium",
            min_value=0.0,
            value=40.0,
            key="fert_potassium"
        )

        carbon = st.number_input(
            "Carbon",
            min_value=0.0,
            value=8.0,
            key="fert_carbon"
        )

        soil = st.selectbox(
            "Soil Type",
            [
                "Acidic Soil",
                "Alkaline Soil",
                "Loamy Soil",
                "Neutral Soil",
                "Peaty Soil"
            ],
            key="fert_soil"
        )

    crop = st.selectbox(
        "Crop",
        [
            "Adzuki Beans",
            "Black gram",
            "Chickpea",
            "Coconut",
            "Coffee",
            "Cotton",
            "Ground Nut",
            "Jute",
            "Kidney Beans",
            "Lentil",
            "Moth Beans",
            "Mung Bean",
            "Peas",
            "Pigeon Peas",
            "Rubber",
            "Sugarcane",
            "Tea",
            "Tobacco",
            "apple",
            "banana",
            "grapes",
            "maize",
            "mango",
            "millet",
            "muskmelon",
            "orange",
            "papaya",
            "pomegranate",
            "rice",
            "watermelon",
            "wheat"
        ],
        key="fert_crop"
    )

    # ==========================================
    # Fertilizer Validation & Prediction
    # ==========================================

    if st.button(
        "🧪 Recommend Fertilizer",
        key="fertilizer_button"
    ):

        # --------------------------------------
        # Validate Temperature
        # --------------------------------------

        if fertilizer_temperature < -50 or fertilizer_temperature > 70:

            st.warning(
                "Please enter a valid temperature "
                "between -50°C and 70°C."
            )

        # --------------------------------------
        # Validate Moisture
        # --------------------------------------

        elif moisture < 0 or moisture > 100:

            st.warning(
                "Moisture must be between 0 and 100."
            )

        # --------------------------------------
        # Validate Rainfall
        # --------------------------------------

        elif fertilizer_rainfall < 0:

            st.warning(
                "Rainfall cannot be negative."
            )

        # --------------------------------------
        # Validate pH
        # --------------------------------------

        elif fertilizer_ph < 0 or fertilizer_ph > 14:

            st.warning(
                "Soil pH must be between 0 and 14."
            )

        # --------------------------------------
        # Validate Nitrogen
        # --------------------------------------

        elif fertilizer_nitrogen < 0:

            st.warning(
                "Nitrogen cannot be negative."
            )

        # --------------------------------------
        # Validate Phosphorous
        # --------------------------------------

        elif phosphorous < 0:

            st.warning(
                "Phosphorous cannot be negative."
            )

        # --------------------------------------
        # Validate Potassium
        # --------------------------------------

        elif fertilizer_potassium < 0:

            st.warning(
                "Potassium cannot be negative."
            )

        # --------------------------------------
        # Validate Carbon
        # --------------------------------------

        elif carbon < 0:

            st.warning(
                "Carbon cannot be negative."
            )

        # --------------------------------------
        # Prediction
        # --------------------------------------

        else:

            try:

                fertilizer, remark = (
                    recommend_fertilizer(
                        fertilizer_temperature,
                        moisture,
                        fertilizer_rainfall,
                        fertilizer_ph,
                        fertilizer_nitrogen,
                        phosphorous,
                        fertilizer_potassium,
                        carbon,
                        soil,
                        crop
                    )
                )

                st.success(
                    f"Recommended Fertilizer: "
                    f"{fertilizer}"
                )

                st.info(
                    f"Remark: {remark}"
                )

            except Exception as e:

                st.error(
                    "Unable to make the fertilizer "
                    "recommendation. Please check your inputs."
                )

                st.caption(
                    f"Technical details: {e}"
                )

# ==========================================
# Crop Yield Page
# ==========================================

elif st.session_state.page == "Crop Yield":

    if st.button(
        "← Back to Dashboard",
        key="back_yield"
    ):
        go_to("Dashboard")
        st.rerun()

    st.title("🌾 Crop Yield Prediction")

    st.markdown(
    """
    <div style="min-height: 56px;">
        Predict expected crop yield using agricultural
        and environmental data.
    </div>
    """,
    unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        crop_year = st.number_input(
            "Crop Year",
            min_value=1990,
            max_value=2100,
            value=2024,
            step=1,
            key="yield_year"
        )

        area = st.number_input(
            "Area",
            min_value=0.01,
            value=2.5,
            key="yield_area"
        )

        production = st.number_input(
            "Production",
            min_value=0.0,
            value=8.0,
            key="yield_production"
        )

    with col2:

        annual_rainfall = st.number_input(
            "Annual Rainfall",
            min_value=0.0,
            value=1200.0,
            key="yield_rainfall"
        )

        fertilizer = st.number_input(
            "Fertilizer",
            min_value=0.0,
            value=150.0,
            key="yield_fertilizer"
        )

        pesticide = st.number_input(
            "Pesticide",
            min_value=0.0,
            value=20.0,
            key="yield_pesticide"
        )

    with col3:

        crop = st.selectbox(
            "Crop",
            [
                "Rice",
                "Wheat",
                "Maize",
                "Sugarcane",
                "Cotton(lint)",
                "Groundnut",
                "Soyabean",
                "Potato",
                "Jute",
                "Gram",
                "Onion",
                "Tobacco",
                "Turmeric",
                "Garlic",
                "Banana",
                "Coconut"
            ],
            key="yield_crop"
        )

        season = st.selectbox(
            "Season",
            [
                "Kharif",
                "Rabi",
                "Summer",
                "Whole Year",
                "Winter"
            ],
            key="yield_season"
        )

        state = st.selectbox(
            "State",
            [
                "Maharashtra",
                "Madhya Pradesh",
                "Uttar Pradesh",
                "Punjab",
                "Haryana",
                "Karnataka",
                "Tamil Nadu",
                "Gujarat",
                "Bihar",
                "West Bengal",
                "Rajasthan",
                "Andhra Pradesh",
                "Telangana",
                "Odisha",
                "Kerala"
            ],
            key="yield_state"
        )

    # ==========================================
    # Crop Yield Validation & Prediction
    # ==========================================

    if st.button(
        "🌾 Predict Crop Yield",
        key="yield_button"
    ):

        # --------------------------------------
        # Validate Crop Year
        # --------------------------------------

        if crop_year < 1990 or crop_year > 2100:

            st.warning(
                "Please enter a valid crop year."
            )

        # --------------------------------------
        # Validate Area
        # --------------------------------------

        elif area <= 0:

            st.warning(
                "Area must be greater than zero."
            )

        # --------------------------------------
        # Validate Production
        # --------------------------------------

        elif production < 0:

            st.warning(
                "Production cannot be negative."
            )

        # --------------------------------------
        # Validate Rainfall
        # --------------------------------------

        elif annual_rainfall < 0:

            st.warning(
                "Annual rainfall cannot be negative."
            )

        # --------------------------------------
        # Validate Fertilizer
        # --------------------------------------

        elif fertilizer < 0:

            st.warning(
                "Fertilizer quantity cannot be negative."
            )

        # --------------------------------------
        # Validate Pesticide
        # --------------------------------------

        elif pesticide < 0:

            st.warning(
                "Pesticide quantity cannot be negative."
            )

        # --------------------------------------
        # Prediction
        # --------------------------------------

        else:

            try:

                predicted_yield = predict_crop_yield(
                    crop_year=crop_year,
                    area=area,
                    production=production,
                    annual_rainfall=annual_rainfall,
                    fertilizer=fertilizer,
                    pesticide=pesticide,
                    crop=crop,
                    season=season,
                    state=state
                )

                st.success(
                    f"Predicted Crop Yield: "
                    f"{predicted_yield:.2f}"
                )

            except Exception as e:

                st.error(
                    "Unable to make the crop yield prediction. "
                    "Please check your inputs."
                )

                st.caption(
                    f"Technical details: {e}"
                )

# ==========================================
# Mandi Price Prediction Page
# ==========================================

elif st.session_state.page == "Mandi Price":

    if st.button(
        "← Back to Dashboard",
        key="back_mandi"
    ):
        go_to("Dashboard")
        st.rerun()

    st.title("💰 Mandi Price Prediction")

    st.markdown(
    """
    <div style="min-height: 56px;">
        Predict the expected modal mandi price of
        agricultural commodities.
    </div>
    """,
    unsafe_allow_html=True
    )
    st.divider()

    # ======================================
    # Market Information
    # ======================================

    st.subheader("Market Information")

    col1, col2, col3 = st.columns(3)

    with col1:

        state = st.text_input(
            "State",
            value="Maharashtra",
            key="mandi_state"
        )

        district = st.text_input(
            "District",
            value="nashik",
            key="mandi_district"
        )

    with col2:

        market = st.text_input(
            "Market",
            value="Lasalgaon(Niphad)",
            key="mandi_market"
        )

        commodity = st.text_input(
            "Commodity",
            value="Wheat",
            key="mandi_commodity"
        )

    with col3:

        variety = st.text_input(
            "Variety",
            value="Maharashtra 2189",
            key="mandi_variety"
        )

        grade = st.text_input(
            "Grade",
            value="FAQ",
            key="mandi_grade"
        )


    # ======================================
    # Price Information
    # ======================================

    st.subheader("Price Information")

    col1, col2 = st.columns(2)

    with col1:

        min_price = st.number_input(
            "Minimum Price",
            min_value=0.0,
            value=2172.0,
            key="mandi_min_price"
        )

    with col2:

        max_price = st.number_input(
            "Maximum Price",
            min_value=0.0,
            value=2399.0,
            key="mandi_max_price"
        )


    # ======================================
    # Date Information
    # ======================================

    st.subheader("Arrival Date")

    col1, col2, col3 = st.columns(3)

    with col1:

        year = st.number_input(
            "Year",
            min_value=2000,
            max_value=2100,
            value=2023,
            step=1,
            key="mandi_year"
        )

    with col2:

        month = st.number_input(
            "Month",
            min_value=1,
            max_value=12,
            value=6,
            step=1,
            key="mandi_month"
        )

    with col3:

        day = st.number_input(
            "Day",
            min_value=1,
            max_value=31,
            value=6,
            step=1,
            key="mandi_day"
        )


    # ======================================
    # Prediction & Validation
    # ======================================

    if st.button(
        "💰 Predict Mandi Price",
        key="mandi_button",
        use_container_width=True
    ):

        # ----------------------------------
        # Validate Text Inputs
        # ----------------------------------

        if not state.strip():

            st.warning(
                "Please enter the State."
            )

        elif not district.strip():

            st.warning(
                "Please enter the District."
            )

        elif not market.strip():

            st.warning(
                "Please enter the Market."
            )

        elif not commodity.strip():

            st.warning(
                "Please enter the Commodity."
            )

        elif not variety.strip():

            st.warning(
                "Please enter the Variety."
            )

        elif not grade.strip():

            st.warning(
                "Please enter the Grade."
            )

        # ----------------------------------
        # Validate Prices
        # ----------------------------------

        elif min_price < 0 or max_price < 0:

            st.warning(
                "Prices cannot be negative."
            )

        elif min_price > max_price:

            st.warning(
                "Minimum Price cannot be greater "
                "than Maximum Price."
            )

        # ----------------------------------
        # Validate Date
        # ----------------------------------

        else:

            try:

                import datetime

                datetime.date(
                    int(year),
                    int(month),
                    int(day)
                )

            except ValueError:

                st.warning(
                    "Please enter a valid date."
                )

            else:

                try:

                    predicted_price = predict_mandi_price(
                        state=state,
                        district=district,
                        market=market,
                        commodity=commodity,
                        variety=variety,
                        grade=grade,
                        min_price=min_price,
                        max_price=max_price,
                        year=int(year),
                        month=int(month),
                        day=int(day)
                    )

                    st.success(
                        f"Predicted Modal Price: "
                        f"₹ {predicted_price:,.2f}"
                    )

                except Exception as e:

                    st.error(
                        "Unable to make the prediction. "
                        "Please check your inputs."
                    )

                    st.caption(
                        f"Technical details: {e}"
                    )