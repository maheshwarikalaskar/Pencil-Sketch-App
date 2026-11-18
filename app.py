import io

import cv2
import numpy as np
import streamlit as st
from PIL import Image, ImageOps, UnidentifiedImageError

MAX_SIDE = 2000  # very large photos are scaled down so the app stays responsive


def load_image(file):
    """Read an uploaded file as an RGB array. Returns (array, was_resized)."""
    image = Image.open(file)
    image = ImageOps.exif_transpose(image)  # respect phone-camera rotation

    # Transparent PNGs: put them on white "paper" instead of letting transparency turn black
    if image.mode in ("RGBA", "LA") or "transparency" in image.info:
        rgba = image.convert("RGBA")
        paper = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
        image = Image.alpha_composite(paper, rgba)

    image = image.convert("RGB")  # also handles greyscale and palette images
    resized = max(image.size) > MAX_SIDE
    if resized:
        image.thumbnail((MAX_SIDE, MAX_SIDE))
    return np.array(image), resized


def to_pencil_sketch(rgb: np.ndarray, blur_kernel: int = 21) -> np.ndarray:
    """Colour-dodge pencil sketch: gray / (255 - blur(255 - gray))."""
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    inverted = 255 - gray
    blurred = cv2.GaussianBlur(inverted, (blur_kernel, blur_kernel), 0)
    inverted_blur = 255 - blurred
    return cv2.divide(gray, inverted_blur, scale=256.0)


def to_png_bytes(array: np.ndarray) -> bytes:
    buffer = io.BytesIO()
    Image.fromarray(array).save(buffer, format="PNG")
    return buffer.getvalue()


st.set_page_config(page_title="Pencil Sketch App", page_icon="✏️", layout="centered")

st.title("✏️ Pencil Sketch App")
st.write("Upload a photo and turn it into a pencil sketch using OpenCV.")

blur_kernel = st.sidebar.slider(
    "Sketch softness (blur size)",
    min_value=3,
    max_value=101,
    value=21,
    step=2,
    help="Kernel size of the Gaussian blur (always odd). Larger values give softer, bolder shading.",
)

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    try:
        rgb, resized = load_image(uploaded_file)
    except (UnidentifiedImageError, OSError):
        st.error("That file could not be read as an image. Please upload a JPG or PNG.")
        st.stop()

    sketch = to_pencil_sketch(rgb, blur_kernel)

    if resized:
        st.caption(f"Large image scaled down to fit within {MAX_SIDE}px.")

    st.subheader("📷 Original image")
    st.image(rgb)

    st.subheader("✏️ Pencil sketch")
    st.image(sketch, clamp=True)

    st.download_button(
        label="📥 Download sketch",
        data=to_png_bytes(sketch),
        file_name="pencil_sketch.png",
        mime="image/png",
    )
