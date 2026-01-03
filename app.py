import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(page_title="Property Performance Snapshot", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('str_performance_data.csv')
    return df

df = load_data()

# --- HEADER SECTION ---
st.title("First Grand Property Performance Snapshot")
st.markdown("### **Region: Cape Town, South Africa**")
st.markdown("**Analysis Period: December 2024**")
st.divider()

# --- PROPERTY IDENTIFICATION ---
col1, col2 = st.columns(2)
with col1:
    st.markdown("#### 🏢 Property 1: Above&Beyond")
    st.markdown("**Location:** Sea Point | **Type:** Apartment | **Bedrooms:** 3")
with col2:
    st.markdown("#### 🏡 Property 2: Cape Town Luxury Villa")
    st.markdown("**Location:** Woodstock | **Type:** House | **Bedrooms:** 3")

st.divider()

# Calculate monthly averages per property
property1_data = df[df['Property_ID'] == 'SP001'].agg({
    'Occupancy_%': 'mean',
    'ADR': 'mean',
    'Guest_Rating': 'mean',
    'Revenue_Achievement_%': 'mean',
    'Days_to_Next_Booking': 'mean'
})

property2_data = df[df['Property_ID'] == 'SP002'].agg({
    'Occupancy_%': 'mean',
    'ADR': 'mean',
    'Guest_Rating': 'mean',
    'Revenue_Achievement_%': 'mean',
    'Days_to_Next_Booking': 'mean'
})

# --- INDIVIDUAL PROPERTY METRICS ---
st.subheader("📈 Individual Property Performance Metrics")

col1, col2 = st.columns(2)

# Property 1 Metrics
with col1:
    st.markdown("### **Above&Beyond - Sea Point**")
    
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    with metric_col1:
        st.metric("Avg Occupancy", f"{property1_data['Occupancy_%']:.1f}%")
        st.metric("Guest Rating", f"{property1_data['Guest_Rating']:.1f} ⭐")
    with metric_col2:
        st.metric("Avg ADR", f"R{property1_data['ADR']:,.0f}")
        st.metric("Revenue Achievement", f"{property1_data['Revenue_Achievement_%']:.1f}%")
    with metric_col3:
        st.metric("Days to Next Booking", f"{property1_data['Days_to_Next_Booking']:.0f} days")
        st.write("")  # Spacer

# Property 2 Metrics
with col2:
    st.markdown("### **Cape Town Luxury Villa - Woodstock**")
    
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    with metric_col1:
        st.metric("Avg Occupancy", f"{property2_data['Occupancy_%']:.1f}%")
        st.metric("Guest Rating", f"{property2_data['Guest_Rating']:.1f} ⭐")
    with metric_col2:
        st.metric("Avg ADR", f"R{property2_data['ADR']:,.0f}")
        st.metric("Revenue Achievement", f"{property2_data['Revenue_Achievement_%']:.1f}%")
    with metric_col3:
        st.metric("Days to Next Booking", f"{property2_data['Days_to_Next_Booking']:.0f} days")
        st.write("")  # Spacer

st.divider()

# --- OCCUPANCY GAUGE COMPARISON (SEMI-CIRCLE) ---
st.subheader("📊 Occupancy Rate Comparison")

col1, col2 = st.columns(2)

with col1:
    fig_gauge1 = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = property1_data['Occupancy_%'],
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Above&Beyond<br>Sea Point", 'font': {'size': 20}},
        number = {'suffix': "%", 'font': {'size': 40}},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "#1f77b4"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 70], 'color': '#FFB6C6'},
                {'range': [70, 80], 'color': '#FFD700'},
                {'range': [80, 100], 'color': '#90EE90'}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 80}}))
    fig_gauge1.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=80, b=20),
        font={'size': 16}
    )
    st.plotly_chart(fig_gauge1, use_container_width=True)

with col2:
    fig_gauge2 = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = property2_data['Occupancy_%'],
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Cape Town Luxury Villa<br>Woodstock", 'font': {'size': 20}},
        number = {'suffix': "%", 'font': {'size': 40}},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "#ff7f0e"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 70], 'color': '#FFB6C6'},
                {'range': [70, 80], 'color': '#FFD700'},
                {'range': [80, 100], 'color': '#90EE90'}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 80}}))
    fig_gauge2.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=80, b=20),
        font={'size': 16}
    )
    st.plotly_chart(fig_gauge2, use_container_width=True)

st.divider()

# --- METRIC COMPARISONS ---
st.subheader("🔍 Side-by-Side Metric Comparison")

# Prepare comparison data
comparison_df = pd.DataFrame({
    'Metric': ['Occupancy %', 'ADR (R)', 'Guest Rating', 'Revenue Achievement %', 'Days to Next Booking'],
    'Above&Beyond': [
        property1_data['Occupancy_%'],
        property1_data['ADR'],
        property1_data['Guest_Rating'],
        property1_data['Revenue_Achievement_%'],
        property1_data['Days_to_Next_Booking']
    ],
    'Cape Town Luxury Villa': [
        property2_data['Occupancy_%'],
        property2_data['ADR'],
        property2_data['Guest_Rating'],
        property2_data['Revenue_Achievement_%'],
        property2_data['Days_to_Next_Booking']
    ]
})

# Create individual bar charts for each metric
col1, col2 = st.columns(2)

with col1:
    
    # Guest Rating Comparison
    fig_rating = go.Figure(data=[
        go.Bar(name='Above&Beyond', x=['Guest Rating'], y=[property1_data['Guest_Rating']], marker_color='#1f77b4'),
        go.Bar(name='Cape Town Luxury Villa', x=['Guest Rating'], y=[property2_data['Guest_Rating']], marker_color='#ff7f0e')
    ])
    fig_rating.update_layout(title='Guest Rating', yaxis_range=[0, 5], height=250, showlegend=False)
    st.plotly_chart(fig_rating, use_container_width=True)
    
    # Revenue Achievement Comparison
    fig_rev = go.Figure(data=[
        go.Bar(name='Above&Beyond', x=['Revenue Achievement %'], y=[property1_data['Revenue_Achievement_%']], marker_color='#1f77b4'),
        go.Bar(name='Cape Town Luxury Villa', x=['Revenue Achievement %'], y=[property2_data['Revenue_Achievement_%']], marker_color='#ff7f0e')
    ])
    fig_rev.update_layout(title='Revenue Achievement %', yaxis_range=[0, 110], height=250, showlegend=False)
    st.plotly_chart(fig_rev, use_container_width=True)

with col2:
    # ADR Comparison
    fig_adr = go.Figure(data=[
        go.Bar(name='Above&Beyond', x=['ADR'], y=[property1_data['ADR']], marker_color='#1f77b4'),
        go.Bar(name='Cape Town Luxury Villa', x=['ADR'], y=[property2_data['ADR']], marker_color='#ff7f0e')
    ])
    fig_adr.update_layout(title='Average Daily Rate (R)', height=250, showlegend=False)
    st.plotly_chart(fig_adr, use_container_width=True)
    
    # Days to Next Booking Comparison
    fig_days = go.Figure(data=[
        go.Bar(name='Above&Beyond', x=['Days to Next Booking'], y=[property1_data['Days_to_Next_Booking']], marker_color='#1f77b4'),
        go.Bar(name='Cape Town Luxury Villa', x=['Days to Next Booking'], y=[property2_data['Days_to_Next_Booking']], marker_color='#ff7f0e')
    ])
    fig_days.update_layout(title='Days to Next Booking', height=250, showlegend=True)
    st.plotly_chart(fig_days, use_container_width=True)

st.divider()

# --- WEEKLY TRENDS ---
st.subheader("📅 Weekly Performance Trends")

# Create week labels
df_with_weeks = df.copy()
week_mapping = {i: f"Week {(i % 4) + 1}" for i in range(len(df))}
df_with_weeks['Week'] = df_with_weeks.index.map(week_mapping)

col1, col2 = st.columns(2)

with col1:
    # Occupancy Trend
    fig_trend_occ = px.line(df, 
                            x=df.index, 
                            y='Occupancy_%', 
                            color='Property_Name',
                            markers=True,
                            title='Weekly Occupancy % Trend',
                            labels={'index': 'Week Number', 'Occupancy_%': 'Occupancy (%)'},
                            color_discrete_map={
                                'Above&Beyond': '#1f77b4',
                                'Cape Town Luxury Villa': '#ff7f0e'
                            })
    fig_trend_occ.add_hline(y=80, line_dash="dash", line_color="green", 
                            annotation_text="Target (80%)")
    fig_trend_occ.update_layout(height=350)
    st.plotly_chart(fig_trend_occ, use_container_width=True)
    
    # Guest Rating Trend
    fig_trend_rating = px.line(df, 
                                x=df.index, 
                                y='Guest_Rating', 
                                color='Property_Name',
                                markers=True,
                                title='Weekly Guest Rating Trend',
                                labels={'index': 'Week Number', 'Guest_Rating': 'Rating'},
                                color_discrete_map={
                                    'Above&Beyond': '#1f77b4',
                                    'Cape Town Luxury Villa': '#ff7f0e'
                                })
    fig_trend_rating.add_hline(y=4.8, line_dash="dash", line_color="green", 
                               annotation_text="Target (4.8)")
    fig_trend_rating.update_layout(height=350)
    st.plotly_chart(fig_trend_rating, use_container_width=True)

with col2:
    # Revenue Achievement Trend
    fig_trend_rev = px.line(df, 
                            x=df.index, 
                            y='Revenue_Achievement_%', 
                            color='Property_Name',
                            markers=True,
                            title='Weekly Revenue Achievement % Trend',
                            labels={'index': 'Week Number', 'Revenue_Achievement_%': 'Achievement (%)'},
                            color_discrete_map={
                                'Above&Beyond': '#1f77b4',
                                'Cape Town Luxury Villa': '#ff7f0e'
                            })
    fig_trend_rev.add_hline(y=90, line_dash="dash", line_color="green", 
                            annotation_text="Target (90%)")
    fig_trend_rev.update_layout(height=350)
    st.plotly_chart(fig_trend_rev, use_container_width=True)
    
    # ADR Trend
    fig_trend_adr = px.line(df, 
                            x=df.index, 
                            y='ADR', 
                            color='Property_Name',
                            markers=True,
                            title='Weekly ADR Trend',
                            labels={'index': 'Week Number', 'ADR': 'ADR (R)'},
                            color_discrete_map={
                                'Above&Beyond': '#1f77b4',
                                'Cape Town Luxury Villa': '#ff7f0e'
                            })
    fig_trend_adr.update_layout(height=350)
    st.plotly_chart(fig_trend_adr, use_container_width=True)

st.divider()

# --- DETAILED DATA TABLE ---
st.subheader("📋 Detailed Weekly Performance Data")

# Color coding function
def color_occupancy(val):
    if val >= 80:
        return 'background-color: #399e39'
    elif val >= 70:
        return 'background-color: #bda008'
    else:
        return 'background-color: #cc2146'

def color_rating(val):
    if val >= 4.8:
        return 'background-color: #399e39'
    elif val >= 4.5:
        return 'background-color: #bda008'
    else:
        return 'background-color: #cc2146'

def color_achievement(val):
    if val >= 90:
        return 'background-color: #399e39'
    elif val >= 75:
        return 'background-color: #bda008'
    else:
        return 'background-color: #cc2146'

# Display styled dataframe
styled_df = df.style.applymap(color_occupancy, subset=['Occupancy_%']) \
                    .applymap(color_rating, subset=['Guest_Rating']) \
                    .applymap(color_achievement, subset=['Revenue_Achievement_%']) \
                    .format({
                        'Occupancy_%': '{:.0f}%',
                        'ADR': 'R{:.0f}',
                        'Guest_Rating': '{:.1f}',
                        'Revenue_Achievement_%': '{:.0f}%',
                        'Revenue_Potential': 'R{:,.0f}',
                        'Weekly_Revenue': 'R{:,.0f}'
                    })

st.dataframe(styled_df, use_container_width=True)

st.divider()

# --- KEY INSIGHTS ---
st.subheader("🎯 Key Performance Insights")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🟢 **Above&Beyond - Sea Point**")
    if property1_data['Occupancy_%'] >= 80:
        st.success(f"✓ Strong occupancy at {property1_data['Occupancy_%']:.1f}%")
    else:
        st.warning(f"⚠ Below target occupancy: {property1_data['Occupancy_%']:.1f}%")
    
    if property1_data['Guest_Rating'] >= 4.8:
        st.success(f"✓ Excellent guest rating: {property1_data['Guest_Rating']:.1f}★")
    else:
        st.info(f"• Guest rating: {property1_data['Guest_Rating']:.1f}★")
    
    if property1_data['Revenue_Achievement_%'] >= 90:
        st.success(f"✓ Meeting revenue targets: {property1_data['Revenue_Achievement_%']:.1f}%")
    else:
        st.warning(f"⚠ Revenue achievement: {property1_data['Revenue_Achievement_%']:.1f}%")

with col2:
    st.markdown("#### 🟡 **Cape Town Luxury Villa - Woodstock**")
    if property2_data['Occupancy_%'] >= 80:
        st.success(f"✓ Strong occupancy at {property2_data['Occupancy_%']:.1f}%")
    else:
        st.warning(f"⚠ Below target occupancy: {property2_data['Occupancy_%']:.1f}%")
    
    if property2_data['Guest_Rating'] >= 4.8:
        st.success(f"✓ Excellent guest rating: {property2_data['Guest_Rating']:.1f}★")
    else:
        st.info(f"• Guest rating: {property2_data['Guest_Rating']:.1f}★")
    
    if property2_data['Revenue_Achievement_%'] >= 90:
        st.success(f"✓ Meeting revenue targets: {property2_data['Revenue_Achievement_%']:.1f}%")
    else:
        st.warning(f"⚠ Revenue achievement: {property2_data['Revenue_Achievement_%']:.1f}%")

st.divider()

# --- RECOMMENDATIONS ---
st.subheader("💡 Recommended Actions")

# Determine which property needs more attention
if property1_data['Occupancy_%'] < property2_data['Occupancy_%']:
    weaker_property = "Above&Beyond"
    weaker_occ = property1_data['Occupancy_%']
else:
    weaker_property = "Cape Town Luxury Villa"
    weaker_occ = property2_data['Occupancy_%']

st.markdown(f"""
**Priority Actions:**
- **{weaker_property}** requires immediate attention with {weaker_occ:.1f}% occupancy
- Review and optimize pricing strategy for properties with <90% revenue achievement
- Monitor guest feedback for properties with ratings below 4.8

**Investigation Areas:**
- Review seasonal demand trends for December-January transition
- Assess impact of ADR adjustments on occupancy rates
- Evaluate property listing quality (photos, descriptions, amenities)
""")

st.divider()


# --- REQUIREMNTS ---
st.subheader("Installation Requirements")

st.markdown(f"""
**Tech Stack needed to install & run:**
- streamlit
- pandas
- plotly
""")
