import streamlit as st
import pandas as pd
import io
import datetime

st.set_page_config(page_title="Statement Processor", layout="wide")
st.title("📊 Multi-Step Statement Processor")

tab1, tab2, tab3 = st.tabs(["📁 Step 1: Merge & Tag", "🔍 Step 2: PO Check", "💳 Step 3: Remittance Merge"])

# Tab 1 – Statement Merging and Classification
with tab1:
    st.subheader("Upload Statement and Reference File")
    file_main = st.file_uploader("📄 Upload Statement File", type=["xlsx"])
    file_ref = st.file_uploader("📄 Upload Reference File", type=["xlsx"])

    if file_main and file_ref:
        df_main = pd.read_excel(file_main)
        df_ref = pd.read_excel(file_ref)

        st.write("✅ Files Loaded")

        required_cols = ['UniqueID', 'PO', 'ReferenceNumber', 'Amount']
        if not all(col in df_main.columns for col in required_cols):
            st.error(f"Statement file must include these columns: {required_cols}")
        else:
            merged_df = pd.merge(df_main, df_ref, on='UniqueID', how='left', indicator=True)
            matched = merged_df[merged_df['_merge'] == 'both'].copy()
            unmatched = merged_df[merged_df['_merge'] == 'left_only'].copy()

            matched["Status"] = "Matched"
            unmatched["Status"] = "Unmatched"

            combined_df = pd.concat([matched, unmatched], ignore_index=True)

            # Optional enrichment (anonymized)
            combined_df["CalculatedField"] = combined_df["Amount"] * 0.1  # Example: 10% rule
            combined_df["Flag"] = combined_df["CalculatedField"].apply(lambda x: "High" if x > 100 else "Normal")

            st.dataframe(combined_df)

            st.session_state["merged_data"] = combined_df

            # Download button
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
                combined_df.to_excel(writer, index=False, sheet_name="Processed")
            buffer.seek(0)
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            st.download_button(
                label="📥 Download Processed File",
                data=buffer.getvalue(),
                file_name=f"processed_output_{timestamp}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )

# Tab 2 – PO Presence Checker
with tab2:
    st.subheader("Upload File for PO Cross-Check")

    if "merged_data" not in st.session_state:
        st.warning("Please complete Step 1 first.")
    else:
        df_merged = st.session_state["merged_data"]
        file_check = st.file_uploader("📄 Upload File with PO Column", type=["xlsx"])

        if file_check:
            df_check = pd.read_excel(file_check)

            if 'PO' not in df_check.columns:
                st.error("Uploaded file must have a 'PO' column.")
            else:
                df_check['PO'] = df_check['PO'].astype(str)
                df_merged['PO'] = df_merged['PO'].astype(str)
                df_merged['PO_Status'] = df_merged['PO'].apply(lambda po: "Exists" if po in df_check['PO'].values else "Missing")
                st.dataframe(df_merged)

                # Download check result
                buffer2 = io.BytesIO()
                with pd.ExcelWriter(buffer2, engine="xlsxwriter") as writer:
                    df_merged.to_excel(writer, index=False, sheet_name="PO_Check")
                buffer2.seek(0)
                st.download_button(
                    "📥 Download PO Check File",
                    data=buffer2.getvalue(),
                    file_name="po_check_result.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

# Tab 3 – Remittance Merge
with tab3:
    st.subheader("Upload Remittance File for Final Merge")

    if "merged_data" not in st.session_state:
        st.warning("Please complete Step 1 first.")
    else:
        df_merged = st.session_state["merged_data"]
        file_remit = st.file_uploader("📄 Upload Remittance File", type=["xlsx"])

        if file_remit:
            df_remit = pd.read_excel(file_remit)

            if "PO" not in df_remit.columns:
                st.error("Remittance file must include a 'PO' column.")
            else:
                df_remit['PO'] = pd.to_numeric(df_remit['PO'], errors='coerce').astype('Int64')
                df_merged['PO'] = pd.to_numeric(df_merged['PO'], errors='coerce').astype('Int64')

                final_df = pd.merge(df_merged, df_remit, on="PO", how="left")
                st.dataframe(final_df)

                buffer3 = io.BytesIO()
                with pd.ExcelWriter(buffer3, engine="xlsxwriter") as writer:
                    final_df.to_excel(writer, index=False, sheet_name="Final_Merged")
                buffer3.seek(0)
                st.download_button(
                    "📥 Download Final Merged File",
                    data=buffer3.getvalue(),
                    file_name="final_merged_output.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
