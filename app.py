import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# -------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------
st.set_page_config(
    page_title="Global Development Dashboard",
    page_icon="🌍",
    layout="wide"
)

# -------------------------------------------------
# TITLE
# -------------------------------------------------
st.title("🌍 Global Development Dashboard")
st.write(
    "Compare the development indicators of two countries "
    "using population, health, economy, technology, environment and tourism data."
)

# -------------------------------------------------
# LOAD EXCEL FILE
# -------------------------------------------------
BASE_DIR = Path(__file__).parent
EXCEL_FILE = BASE_DIR / "World_development_mesurement.xlsx"

if not EXCEL_FILE.exists():
    st.error(
        f"❌ Dataset not found!\n\n"
        f"Expected file: {EXCEL_FILE.name}\n\n"
        "Make sure the Excel file is uploaded to the same GitHub repository "
        "as app.py."
    )
    st.stop()

try:
    df = pd.read_excel(EXCEL_FILE)
except Exception as e:
    st.error(f"❌ Error reading Excel file: {e}")
    st.stop()

# -------------------------------------------------
# CHECK REQUIRED COLUMN
# -------------------------------------------------
if "Country" not in df.columns:
    st.error("❌ The Excel file must contain a 'Country' column.")
    st.stop()

# -------------------------------------------------
# COUNTRY LIST
# -------------------------------------------------
countries = sorted(
    df["Country"].dropna().astype(str).unique().tolist()
)

if len(countries) < 2:
    st.error("❌ At least two countries are required.")
    st.stop()

# -------------------------------------------------
# COUNTRY SELECTION
# -------------------------------------------------
st.subheader("🌎 Select Two Countries for Comparison")

col1, col2 = st.columns(2)

with col1:
    country1 = st.selectbox(
        "Select First Country",
        countries,
        index=0
    )

with col2:
    country2 = st.selectbox(
        "Select Second Country",
        countries,
        index=1
    )

# -------------------------------------------------
# GET COUNTRY DATA
# -------------------------------------------------
data1 = df[df["Country"].astype(str) == country1]

data2 = df[df["Country"].astype(str) == country2]

if data1.empty or data2.empty:
    st.error("❌ Country data not found.")
    st.stop()

country_data1 = data1.iloc[0]
country_data2 = data2.iloc[0]

# -------------------------------------------------
# BASIC DETAILS
# -------------------------------------------------
st.header("📊 Country Comparison")

col1, col2 = st.columns(2)

with col1:

    st.subheader(f"🌍 {country1}")

    st.metric(
        "GDP",
        country_data1.get("GDP", "N/A")
    )

    st.metric(
        "Population",
        country_data1.get("Population Total", "N/A")
    )

    st.metric(
        "Internet Usage",
        country_data1.get("Internet Usage", "N/A")
    )

    st.metric(
        "Life Expectancy Male",
        country_data1.get("Life Expectancy Male", "N/A")
    )

    st.metric(
        "Life Expectancy Female",
        country_data1.get("Life Expectancy Female", "N/A")
    )


with col2:

    st.subheader(f"🌍 {country2}")

    st.metric(
        "GDP",
        country_data2.get("GDP", "N/A")
    )

    st.metric(
        "Population",
        country_data2.get("Population Total", "N/A")
    )

    st.metric(
        "Internet Usage",
        country_data2.get("Internet Usage", "N/A")
    )

    st.metric(
        "Life Expectancy Male",
        country_data2.get("Life Expectancy Male", "N/A")
    )

    st.metric(
        "Life Expectancy Female",
        country_data2.get("Life Expectancy Female", "N/A")
    )

# -------------------------------------------------
# CATEGORIES
# -------------------------------------------------
categories = {

    "Population": [
        "Population 0-14",
        "Population 15-64",
        "Population 65+",
        "Population Total",
        "Population Urban"
    ],

    "Health": [
        "Health Exp % GDP",
        "Health Exp/Capita",
        "Life Expectancy Female",
        "Life Expectancy Male",
        "Infant Mortality Rate"
    ],

    "Economy": [
        "GDP",
        "Business Tax Rate",
        "Ease of Business",
        "Days to Start Business",
        "Hours to do Tax",
        "Lending Interest"
    ],

    "Technology": [
        "Internet Usage",
        "Mobile Phone Usage"
    ],

    "Environment": [
        "CO2 Emissions",
        "Energy Usage",
        "Birth Rate"
    ],

    "Tourism": [
        "Tourism Inbound",
        "Tourism Outbound"
    ]
}

# -------------------------------------------------
# FIND AVAILABLE COLUMNS
# -------------------------------------------------
available_categories = {}

for category_name, columns in categories.items():

    available_columns = [
        column for column in columns
        if column in df.columns
    ]

    if available_columns:
        available_categories[category_name] = available_columns

if not available_categories:
    st.error("❌ None of the expected indicator columns were found.")
    st.stop()

# -------------------------------------------------
# SELECT CATEGORY
# -------------------------------------------------
category = st.selectbox(
    "Select Category",
    list(available_categories.keys())
)

cols = available_categories[category]

st.header(f"📈 {category} Comparison")

# -------------------------------------------------
# VALUE CONVERSION FUNCTION
# -------------------------------------------------
def convert_value(value):

    if pd.isna(value):
        return 0.0

    if isinstance(value, str):

        value = (
            value
            .replace("$", "")
            .replace(",", "")
            .replace("%", "")
            .strip()
        )

        try:
            return float(value)
        except ValueError:
            return 0.0

    try:
        return float(value)

    except (ValueError, TypeError):
        return 0.0


# -------------------------------------------------
# CREATE VALUES
# -------------------------------------------------
values1 = []
values2 = []

for column in cols:

    values1.append(
        convert_value(country_data1[column])
    )

    values2.append(
        convert_value(country_data2[column])
    )

# -------------------------------------------------
# COMPARISON TABLE
# -------------------------------------------------
comparison_df = pd.DataFrame({

    "Indicator": cols,

    country1: values1,

    country2: values2

})

st.subheader("📋 Indicator Comparison")

st.dataframe(
    comparison_df,
    use_container_width=True
)

# -------------------------------------------------
# BAR CHART
# -------------------------------------------------
st.subheader("📊 Comparison Chart")

fig, ax = plt.subplots(figsize=(12, 6))

x = range(len(cols))

width = 0.35

ax.bar(
    [i - width / 2 for i in x],
    values1,
    width=width,
    label=country1
)

ax.bar(
    [i + width / 2 for i in x],
    values2,
    width=width,
    label=country2
)

ax.set_xticks(list(x))

ax.set_xticklabels(
    cols,
    rotation=45,
    ha="right"
)

ax.set_ylabel("Value")

ax.set_title(
    f"{country1} vs {country2} - {category}"
)

ax.legend()

plt.tight_layout()

st.pyplot(fig)

plt.close(fig)

# -------------------------------------------------
# HIGHEST VALUE COMPARISON
# -------------------------------------------------
st.subheader("🏆 Highest Value Comparison")

results = []

for i in range(len(cols)):

    indicator = cols[i]

    value1 = values1[i]

    value2 = values2[i]

    if value1 > value2:

        winner = country1

    elif value2 > value1:

        winner = country2

    else:

        winner = "Equal"

    results.append({

        "Indicator": indicator,

        country1: value1,

        country2: value2,

        "Highest Value": winner

    })

result_df = pd.DataFrame(results)

st.dataframe(
    result_df,
    use_container_width=True
)

# -------------------------------------------------
# FINAL RESULT
# -------------------------------------------------
st.subheader("🏅 Final Comparison Result")

country1_wins = 0
country2_wins = 0
equal_count = 0

for i in range(len(cols)):

    if values1[i] > values2[i]:

        country1_wins += 1

    elif values2[i] > values1[i]:

        country2_wins += 1

    else:

        equal_count += 1

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        f"{country1} Wins",
        country1_wins
    )

with col2:

    st.metric(
        f"{country2} Wins",
        country2_wins
    )

with col3:

    st.metric(
        "Equal",
        equal_count
    )

if country1_wins > country2_wins:

    st.success(
        f"🏆 {country1} has higher values in more indicators!"
    )

elif country2_wins > country1_wins:

    st.success(
        f"🏆 {country2} has higher values in more indicators!"
    )

else:

    st.info(
        "🤝 Both countries have the same number of wins!"
    )

# -------------------------------------------------
# COUNTRY DETAILS
# -------------------------------------------------
st.subheader(f"📋 {country1} Details")

st.dataframe(
    data1,
    use_container_width=True
)

st.subheader(f"📋 {country2} Details")

st.dataframe(
    data2,
    use_container_width=True
)

# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.markdown("---")

st.caption(
    "🌍 Global Development Dashboard | "
    "Built with Python, Pandas, Matplotlib and Streamlit"
)
