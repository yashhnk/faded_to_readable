import streamlit as st
from PIL import Image
import numpy as np
import io

st.set_page_config(
    page_title="Historical Manuscript Restoration",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .stButton>button {
        width: 100%;
        background-color: #2c3e50;
        color: white;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 500;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #34495e;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .upload-box {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    .image-container {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
    }
    h1 {
        color: #2c3e50;
        text-align: center;
        padding: 1.5rem 0;
        font-weight: 600;
    }
    h3 {
        color: #34495e;
        font-weight: 500;
        margin-top: 1rem;
    }
    .stCheckbox {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>From Faded to Readable: Historical Manuscript Restoration</h1>", unsafe_allow_html=True)

st.markdown('<div class="upload-box">', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Upload Manuscript Image",
    type=["jpg", "jpeg", "png", "tiff", "tif"]
)
st.markdown('</div>', unsafe_allow_html=True)

if uploaded_file is not None:
    original_image = Image.open(uploaded_file)

    st.markdown('<div class="image-container">', unsafe_allow_html=True)
    st.markdown("### Original Manuscript")
    st.image(original_image, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    enhanced_image = original_image.copy()
    from PIL import ImageEnhance
    enhancer = ImageEnhance.Contrast(enhanced_image)
    enhanced_image = enhancer.enhance(1.5)
    enhancer = ImageEnhance.Brightness(enhanced_image)
    enhanced_image = enhancer.enhance(1.1)

    img_array = np.array(original_image.convert('L'))
    threshold = np.percentile(img_array, 50)
    segmentation_mask = np.zeros((*img_array.shape, 3), dtype=np.uint8)

    text_blocks = img_array < threshold
    illustrations = (img_array >= threshold) & (img_array < np.percentile(img_array, 75))
    marginalia = img_array >= np.percentile(img_array, 75)

    segmentation_mask[text_blocks] = [255, 100, 100]
    segmentation_mask[illustrations] = [100, 255, 100]
    segmentation_mask[marginalia] = [100, 100, 255]

    segmentation_image = Image.fromarray(segmentation_mask)

    st.markdown('<div class="image-container">', unsafe_allow_html=True)
    st.markdown("### Preview: Original vs. Enhanced")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Before**")
        st.image(original_image, use_container_width=True)

    with col2:
        st.markdown("**After**")
        st.image(enhanced_image, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    show_overlay = st.checkbox("Show Segmentation Overlay")

    st.markdown('<div class="image-container">', unsafe_allow_html=True)
    if show_overlay:
        st.markdown("### Enhanced with Segmentation Overlay")
        st.markdown("""
        <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
        <strong>Legend:</strong><br>
        🔴 Red: Text blocks<br>
        🟢 Green: Illustrations<br>
        🔵 Blue: Marginalia
        </div>
        """, unsafe_allow_html=True)

        enhanced_array = np.array(enhanced_image.convert('RGB'))
        overlay = np.array(segmentation_image)
        blended = (enhanced_array * 0.6 + overlay * 0.4).astype(np.uint8)
        blended_image = Image.fromarray(blended)

        st.image(blended_image, use_container_width=True)
    else:
        st.markdown("### Enhanced Manuscript")
        st.image(enhanced_image, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="image-container">', unsafe_allow_html=True)
    st.markdown("### Download Options")

    col1, col2 = st.columns(2)

    with col1:
        enhanced_buffer = io.BytesIO()
        enhanced_image.save(enhanced_buffer, format="PNG")
        enhanced_bytes = enhanced_buffer.getvalue()

        st.download_button(
            label="Download Enhanced Image",
            data=enhanced_bytes,
            file_name="enhanced_manuscript.png",
            mime="image/png"
        )

    with col2:
        mask_buffer = io.BytesIO()
        segmentation_image.save(mask_buffer, format="PNG")
        mask_bytes = mask_buffer.getvalue()

        st.download_button(
            label="Download Segmentation Mask",
            data=mask_bytes,
            file_name="segmentation_mask.png",
            mime="image/png"
        )
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown("""
        <div style="background: white; padding: 3rem; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); text-align: center;">
            <h3 style="color: #34495e; margin-bottom: 1rem;">Ready to Restore History</h3>
            <p style="color: #7f8c8d; font-size: 1.1rem;">Upload a manuscript image to begin the restoration process</p>
        </div>
    """, unsafe_allow_html=True)
