import streamlit as st
import pandas as pd
import io

df = pd.read_csv("bt_batch_07.csv", encoding="utf-8-sig")

st.set_page_config(page_title="Backtranslation Rating - Rater 07", layout="centered")
st.title("📝 Simplification Back-Translation Evaluation - Rater 07")

rater_id = "rater07"
ratings = []

for idx, row in df.iterrows():
    st.markdown(f"### 🔢 Sample {idx+1}")
    st.markdown(f"**🟩 Source:**  \n{row['source']}")
    st.markdown(f"**🇩🇪 German Back-Translation:**  \n{row['bt_de']}")
    st.markdown(f"**🇨🇳 Chinese Back-Translation:**  \n{row['bt_zh']}")

    st.markdown("**Rate German Version:**")
    g_meaning = st.slider(f"Meaning (German) [{idx}]", 1, 5, 3, key=f"gm{idx}")
    g_fluency = st.slider(f"Fluency (German) [{idx}]", 1, 5, 3, key=f"gf{idx}")
    g_simplicity = st.slider(f"Simplicity (German) [{idx}]", 1, 5, 3, key=f"gs{idx}")
    g_diversity = st.slider(f"Diversity (German) [{idx}]", 1, 5, 3, key=f"gd{idx}")

    st.markdown("**Rate Chinese Version:**")
    c_meaning = st.slider(f"Meaning (Chinese) [{idx}]", 1, 5, 3, key=f"cm{idx}")
    c_fluency = st.slider(f"Fluency (Chinese) [{idx}]", 1, 5, 3, key=f"cf{idx}")
    c_simplicity = st.slider(f"Simplicity (Chinese) [{idx}]", 1, 5, 3, key=f"cs{idx}")
    c_diversity = st.slider(f"Diversity (Chinese) [{idx}]", 1, 5, 3, key=f"cd{idx}")

    ratings.append({
        "rater_id": rater_id,
        "sample_id": idx + 1,
        "source": row["source"],
        "bt_de": row["bt_de"],
        "bt_zh": row["bt_zh"],
        "g_meaning": g_meaning,
        "g_fluency": g_fluency,
        "g_simplicity": g_simplicity,
        "g_diversity": g_diversity,
        "c_meaning": c_meaning,
        "c_fluency": c_fluency,
        "c_simplicity": c_simplicity,
        "c_diversity": c_diversity,
    })

# 分隔线
st.markdown("---")

# 如果有评分数据，显示下载按钮
if ratings:
    ratings_df = pd.DataFrame(ratings)
    csv_buffer = io.StringIO()
    ratings_df.to_csv(csv_buffer, index=False, encoding="utf-8-sig")
    csv_data = csv_buffer.getvalue()

    st.download_button(
        label="⬇️ Download Ratings as CSV",
        data=csv_data,
        file_name=f"bt_ratings_{rater_id}.csv",
        mime="text/csv"
    )
