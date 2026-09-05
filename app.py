import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Global Development Dashboard",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Global Development Dashboard")

# Get current app folder
BASE_DIR = Path(__file__).resolve().parent

# Excel file
excel_file = BASE_DIR / "World_development_mesurement.xlsx"

# Check Excel file
if not excel_file.exists():
    st.error(
        "❌ Excel file not found!\n\n"
        "Make sure 'World_development_mesurement.xlsx' "
        "is in the same GitHub folder as app.py."
    )
    st.stop()

# Load Excel
try:
    df = pd.read_excel(excel_file)
except Exception as e:
    st.error(f"❌ Error loading Excel file: {e}")
    st.stop()

# Check Country column
if "Country" not in df.columns:
    st.error("❌ 'Country' column is missing from the Excel file.")
    st.stop()

# Country list
countries = sorted(
    df["Country"].dropna().astype(str).unique()
)

if len(countries) < 2:
    st.error("❌ At least two countries are required.")
    st.stop()

# Country selection
st.subheader("🌎 Select Two Countries")

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

# Get country data
country_data1 = df[
    df["Country"].astype(str) == country1
].iloc[0]

country_data2 = df[
    df["Country"].astype(str) == country2
].iloc[0]

# Basic comparison
st.header("📊 Country Comparison")

col1, col2 = st.columns(2)

with col1:
    st.subheader(f"🌍 {country1}")

    if "GDP" in df.columns:
        st.metric("GDP", country_data1["GDP"])

    if "Population Total" in df.columns:
        st.metric(
            "Population",
            country_data1["Population Total"]
        )

    if "Internet Usage" in df.columns:
        st.metric(
            "Internet Usage",
            country_data1["Internet Usage"]
        )

    if "Life Expectancy Male" in df.columns:
        st.metric(
            "Life Expectancy Male",
            country_data1["Life Expectancy Male"]
        )

    if "Life Expectancy Female" in df.columns:
        st.metric(
            "Life Expectancy Female",
            country_data1["Life Expectancy Female"]
        )


with col2:
    st.subheader(f"🌍 {country2}")

    if "GDP" in df.columns:
        st.metric("GDP", country_data2["GDP"])

    if "Population Total" in df.columns:
        st.metric(
            "Population",
            country_data2["Population Total"]
        )

    if "Internet Usage" in df.columns:
        st.metric(
            "Internet Usage",
            country_data2["Internet Usage"]
        )

    if "Life Expectancy Male" in df.columns:
        st.metric(
            "Life Expectancy Male",
            country_data2["Life Expectancy Male"]
        )

    if "Life Expectancy Female" in df.columns:
        st.metric(
            "Life Expectancy Female",
            country_data2["Life Expectancy Female"]
        )

# Categories
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

# Only use columns that actually exist
available_categories = {}

for category, columns in categories.items():

    available_columns = [
        col for col in columns
        if col in df.columns
    ]

    if available_columns:
        available_categories[category] = available_columns

# Category selection
category = st.selectbox(
    "Select Category",
    list(available_categories.keys())
)

cols = available_categories[category]

st.header(f"📈 {category} Comparison")


# Convert values
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

    except:
        return 0.0


# Create values
values1 = []
values2 = []

for col in cols:

    values1.append(
        convert_value(country_data1[col])
    )

    values2.append(
        convert_value(country_data2[col])
    )


# Comparison table
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


# Bar chart
st.subheader("📊 Comparison Chart")

fig, ax = plt.subplots(figsize=(12, 6))

x = range(len(cols))
width = 0.35

ax.bar(
    [i - width / 2 for i in x],
    values1,
    width,
    label=country1
)

ax.bar(
    [i + width / 2 for i in x],
    values2,
    width,
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
    f"{country1} vs {country2}"
)

ax.legend()

plt.tight_layout()

st.pyplot(fig)

plt.close(fig)


# Highest value
st.subheader("🏆 Highest Value Comparison")

results = []

for i in range(len(cols)):

    value1 = values1[i]
    value2 = values2[i]

    if value1 > value2:
        winner = country1

    elif value2 > value1:
        winner = country2

    else:
        winner = "Equal"

    results.append({
        "Indicator": cols[i],
        country1: value1,
        country2: value2,
        "Highest Value": winner
    })

result_df = pd.DataFrame(results)

st.dataframe(
    result_df,
    use_container_width=True
)


# Final result
st.subheader("🏅 Final Comparison Result")

country1_wins = 0
country2_wins = 0
equal = 0

for i in range(len(cols)):

    if values1[i] > values2[i]:
        country1_wins += 1

    elif values2[i] > values1[i]:
        country2_wins += 1

    else:
        equal += 1


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
        equal
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


# Country details
st.subheader(f"📋 {country1} Details")

st.dataframe(
    df[df["Country"].astype(str) == country1],
    use_container_width=True
)

st.subheader(f"📋 {country2} Details")

st.dataframe(
    df[df["Country"].astype(str) == country2],
    use_container_width=True
)

st.markdown("---")

st.caption(
    "🌍 Global Development Dashboard | "
    "Python + Pandas + Matplotlib + Streamlit"
)
