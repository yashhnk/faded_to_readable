import streamlit as st
from PIL import Image
import numpy as np
import io

st.set_page_config(
    page_title="Historical Manuscript Restoration",
    layout="wide"
)

st.title("From Faded to Readable: Historical Manuscript Restoration")

st.markdown("---")

uploaded_file = st.file_uploader(
    "Upload Manuscript Image",
    type=["jpg", "jpeg", "png", "tiff", "tif"]
)

if uploaded_file is not None:
    original_image = Image.open(uploaded_file)

    st.markdown("### Original Manuscript")
    st.image(original_image, use_container_width=True)

    st.markdown("---")

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

    st.markdown("### Preview: Original vs. Enhanced")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Before**")
        st.image(original_image, use_container_width=True)

    with col2:
        st.markdown("**After**")
        st.image(enhanced_image, use_container_width=True)

    st.markdown("---")

    show_overlay = st.checkbox("Show Segmentation Overlay")

    if show_overlay:
        st.markdown("### Enhanced with Segmentation Overlay")
        st.markdown("""
        **Legend:**
        - 🔴 Red: Text blocks
        - 🟢 Green: Illustrations
        - 🔵 Blue: Marginalia
        """)

        enhanced_array = np.array(enhanced_image.convert('RGB'))
        overlay = np.array(segmentation_image)
        blended = (enhanced_array * 0.6 + overlay * 0.4).astype(np.uint8)
        blended_image = Image.fromarray(blended)

        st.image(blended_image, use_container_width=True)
    else:
        st.markdown("### Enhanced Manuscript")
        st.image(enhanced_image, use_container_width=True)

    st.markdown("---")

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

else:
    st.info("Please upload a manuscript image to begin.")
