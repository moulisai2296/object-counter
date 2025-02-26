import streamlit as st
import requests
import pandas as pd

# Flask API URL
API_URL = "http://127.0.0.1:5000"

def upload_image(files, threshold, model_name):
    """ Sends image to Flask API for object detection """
    files_data =[("file", (file.name, file, file.type)) for file in files]
    data = {"threshold": threshold, "model_name": model_name}
    response = requests.post(f"{API_URL}/object-count-pg", files=files_data, data=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to process image"}

def get_total_objects(object_class=None):
    """ Fetches total object counts from the API """
    params = {"object_class": object_class} if object_class else {}
    response = requests.get(f"{API_URL}/get_object_count", params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch object counts"}

# UI with Tabs
st.title("Object Detection App")

tab1, tab2 = st.tabs(["Object Detection", "Total Object Counts"])

with tab1:
    st.header("Upload Images for Detection")
    uploaded_files = st.file_uploader("Choose images...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    threshold = st.slider("Threshold", 0.1, 1.0, 0.5)
    model_name = st.selectbox("Select Model", ["rfcn"])

    if uploaded_files and st.button("Detect Objects"):
        results = upload_image(uploaded_files, threshold, model_name)
        print(results)
        if not results:
            st.error("!!! Failed to process images. Please try again.")
        else:
            data_list = []
            for filename, result in results.items():
                for obj in result["predictions"]:
                    data_list.append({
                        "Filename": filename,
                        "Object Class": obj["object_class"],
                        "Count": obj["count"]
                    })
            
            # Convert to DataFrame
            df = pd.DataFrame(data_list)

            # Display table
            if not df.empty:
                st.success("Objects detected!")
                st.table(df)  # Use st.dataframe(df) for a scrollable table
            else:
                st.warning("No objects detected in the uploaded images.")

with tab2:
    st.header("Total Object Counts")
    object_class_filter = st.text_input("Filter by Object Class (optional)", "")

    if st.button("Fetch Object Counts"):
        total_objects = get_total_objects(object_class_filter if object_class_filter else None)

        if "error" in total_objects:
            st.error("Failed to fetch object counts.")
        elif total_objects:
            st.success("Total object counts retrieved!")

            df_total = pd.DataFrame(total_objects["total_objects"])
            st.table(df_total)
        else:
            st.warning("No objects found.")
