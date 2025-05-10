import streamlit as st
import pandas as pd
import io

# 设置页面标题和布局
st.set_page_config(page_title="Backtranslation Rating - Rater 07", layout="centered")
st.title("📝 Simplification Back-Translation Evaluation - Rater 07")

# 📘 展开评分标准
with st.expander("📘 Click here to view the Rating Guidelines"):
    st.markdown("""
### 🎯 **Scoring Guidelines (1–5 scale)**

#### 1️⃣ Meaning (compared to the original sentence)  
- **5:** All key information kept, meaning unchanged  
- **3:** Some loss or minor distortion  
- **1:** Meaning totally changed or missing  
🛑 _Watch out for:_ Omitted facts, Added content, Entity mix-ups  

#### 2️⃣ Fluency (grammar & expression only)  
- **5:** Fully natural and grammatically correct  
- **3:** Understandable but awkward  
- **1:** Hard to read or broken grammar  
🛑 _Watch out for:_ Word order issues, Punctuation, Verb forms  

#### 3️⃣ Simplicity (compared to the original sentence)  
- **5:** Much easier to read, clearly simplified  
- **3:** Slightly easier or similar  
- **1:** Still complex or made worse  
🛑 _Watch out for:_ Long/complex structure, Redundant phrasing  

#### 4️⃣ Diversity (optional, if multiple refs exist)  
- **5:** Very different in style or structure  
- **3:** Some variation  
- **1:** Almost identical to others  
📌 _This measures **variation**, not correctness._  
""")

# 读取 CSV 文件
df = pd.read_csv("bt_batch_07.csv", encoding="utf-8-sig")

rater_id = "rater07"

# 分页和状态保存
samples_per_page = 10
if "page" not in st.session_state:
    st.session_state.page = 0
if "ratings_data" not in st.session_state:
    st.session_state.ratings_data = {}

start_idx = st.session_state.page * samples_per_page
end_idx = min((st.session_state.page + 1) * samples_per_page, len(df))

# 展示样本
for idx in range(start_idx, end_idx):
    row = df.iloc[idx]
    st.markdown(f"### 🔢 Sample {idx + 1}")
    st.markdown(f"**🟩 Source:**  \n{row['source']}")
    st.markdown(f"**🇩🇪 German Back-Translation:**  \n{row['bt_de']}")
    st.markdown(f"**🇨🇳 Chinese Back-Translation:**  \n{row['bt_zh']}")

    g_meaning = st.slider(f"Meaning (German) [{idx}]", 1, 5, 3, key=f"gm{idx}")
    g_fluency = st.slider(f"Fluency (German) [{idx}]", 1, 5, 3, key=f"gf{idx}")
    g_simplicity = st.slider(f"Simplicity (German) [{idx}]", 1, 5, 3, key=f"gs{idx}")
    g_diversity = st.slider(f"Diversity (German) [{idx}]", 1, 5, 3, key=f"gd{idx}")
    c_meaning = st.slider(f"Meaning (Chinese) [{idx}]", 1, 5, 3, key=f"cm{idx}")
    c_fluency = st.slider(f"Fluency (Chinese) [{idx}]", 1, 5, 3, key=f"cf{idx}")
    c_simplicity = st.slider(f"Simplicity (Chinese) [{idx}]", 1, 5, 3, key=f"cs{idx}")
    c_diversity = st.slider(f"Diversity (Chinese) [{idx}]", 1, 5, 3, key=f"cd{idx}")

    st.session_state.ratings_data[idx] = {
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
    }

# 显示进度
st.markdown("---")
st.markdown(f"📊 Progress: {len(st.session_state.ratings_data)} / {len(df)} samples rated.")

# 翻页控制
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("⬅️ Previous") and st.session_state.page > 0:
        st.session_state.page -= 1
with col2:
    if st.button("➡️ Next") and end_idx < len(df):
        st.session_state.page += 1
with col3:
    if st.button("⬇️ Download CSV"):
        all_ratings_df = pd.DataFrame.from_dict(st.session_state.ratings_data, orient="index")
        csv_bytes = all_ratings_df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
        st.download_button(
            label="📥 Click here to download",
            data=csv_bytes,
            file_name=f"bt_ratings_{rater_id}.csv",
            mime="text/csv"
        )
