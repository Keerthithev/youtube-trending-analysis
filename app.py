import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set seaborn style
sns.set_style('darkgrid')

st.set_page_config(page_title="YouTube Trending Video Analysis", layout="wide")

# Title and description
st.title("📊 YouTube Trending Video Analysis")
st.markdown("""
Explore trending videos on YouTube by category, publish time, views, likes, comments, and more.
Data Source: Kaggle YouTube Trending Dataset (Nov 2017 - Jun 2018)
""")

@st.cache_data
def load_data():
    df = pd.read_csv('cleaned_youtube_trending.csv')
    # Ensure publish_time is datetime
    df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
    # Fill missing category_name with 'Unknown'
    df['category_name'] = df['category_name'].fillna('Unknown').astype(str)
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("🔎 Filters")

# Fix category list for sidebar filter
categories = sorted(df['category_name'].unique().tolist())
selected_category = st.sidebar.selectbox("Select a category", options=['All'] + categories)

hour_min = int(df['publish_hour'].min())
hour_max = int(df['publish_hour'].max())
selected_hour = st.sidebar.slider("Select publish hour range", hour_min, hour_max, (hour_min, hour_max))

# Filter data based on sidebar selection
filtered_df = df.copy()
if selected_category != 'All':
    filtered_df = filtered_df[filtered_df['category_name'] == selected_category]

filtered_df = filtered_df[
    (filtered_df['publish_hour'] >= selected_hour[0]) &
    (filtered_df['publish_hour'] <= selected_hour[1])
]

# Dataset overview
st.markdown("## Dataset Overview")
st.write(f"Total videos: {len(df)}")
st.write(f"Videos after filtering: {len(filtered_df)}")
st.write(f"Date range: {df['publish_time'].min().date()} to {df['publish_time'].max().date()}")

st.write("### Data Sample")
st.dataframe(filtered_df.head(10))

# ====== Charts ======

# 1. Video Counts by Category (Overall)
st.markdown("## 🎥 Video Counts by Category (All Data)")
fig1, ax1 = plt.subplots(figsize=(12, 6))
order = df['category_name'].value_counts().index
sns.countplot(data=df, y='category_name', order=order, palette='magma', ax=ax1)
ax1.set_xlabel("Count")
ax1.set_ylabel("Category")
st.pyplot(fig1)

st.markdown("---")

# 2. Publish Day Distribution (Filtered)
st.markdown(f"## 📅 Publish Day Distribution (Filtered by Category & Hour)")

# Convert publish_time to day name
filtered_df['publish_day'] = filtered_df['publish_time'].dt.day_name()

day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
fig2, ax2 = plt.subplots(figsize=(10, 5))
sns.countplot(data=filtered_df, x='publish_day', order=day_order, palette='viridis', ax=ax2)
ax2.set_xlabel("Day of Week")
ax2.set_ylabel("Number of Videos")
st.pyplot(fig2)

st.markdown("---")

# 3. Publish Hour Distribution (Filtered)
st.markdown("## ⏰ Publish Hour Distribution (Filtered)")

fig3, ax3 = plt.subplots(figsize=(12, 5))
sns.countplot(data=filtered_df, x='publish_hour', palette='rocket', ax=ax3)
ax3.set_xlabel("Hour of Day")
ax3.set_ylabel("Number of Videos")
st.pyplot(fig3)

st.markdown("---")

# 4. Top 10 Videos by Views (Filtered)
st.markdown("## 🔝 Top 10 Videos by Views")

top10_views = filtered_df.sort_values(by='views', ascending=False).head(10)
fig4, ax4 = plt.subplots(figsize=(12, 6))
sns.barplot(data=top10_views, y='title', x='views', palette='crest', ax=ax4)
ax4.set_xlabel("Views")
ax4.set_ylabel("Video Title")
ax4.tick_params(axis='y', labelsize=9)
st.pyplot(fig4)

st.markdown("---")

# 5. Likes vs Dislikes Scatter (Filtered)
st.markdown("## 👍 Likes vs 👎 Dislikes")

fig5, ax5 = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=filtered_df, x='likes', y='dislikes', hue='category_name', palette='tab10', alpha=0.7, ax=ax5)
ax5.set_xlabel("Likes")
ax5.set_ylabel("Dislikes")
ax5.legend(title="Category", bbox_to_anchor=(1.05, 1), loc='upper left')
st.pyplot(fig5)

st.markdown("---")

# 6. Comments vs Views Scatter (Filtered)
st.markdown("## 💬 Comments vs Views")

fig6, ax6 = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=filtered_df, x='views', y='comment_count', hue='category_name', palette='tab10', alpha=0.7, ax=ax6)
ax6.set_xlabel("Views")
ax6.set_ylabel("Comments")
ax6.legend([],[], frameon=False)  # hide duplicate legend
st.pyplot(fig6)

st.markdown("---")

# 7. Summary Insights
st.markdown("## 🧠 Summary Insights")
st.markdown("""
- Most trending videos come from categories like **Music, Entertainment, and Gaming**.
- Videos published in the **afternoon (12 PM - 6 PM)** tend to have higher views.
- Likes and dislikes generally increase together, showing engagement patterns.
- Comments correlate positively with views but vary widely by category.
""")

# Footer
st.markdown("---")
st.markdown("Made by **Keerthi Dev** | Data Science Student | Powered by Streamlit & Seaborn")


