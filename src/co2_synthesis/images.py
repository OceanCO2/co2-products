"""
In this script there are tools to:
    1) download an image from a url and save it to the buffer
    2) resize the image to be certain max dimensions (pixels)
    3) resize the image to be a certain size (MB)
    4) save the image to disk if not already present
    5) return the name of the new image filename as relative path
"""
import io
import re
import requests
from PIL import Image
from pathlib import Path
import pandas as pd
from loguru import logger
from . import cfg


def process_images_in_df(
        df: pd.DataFrame, 
        name_column: str="Product name",
        image_url_column: str="Image URL", 
        save_dir=cfg.ROOT / "docs/images/", 
        target_pixel_size: tuple[int, int]=(1200, 800), 
        target_size_mb: float=0.5, 
        overwrite: bool=False
    ) -> pd.DataFrame:
    """Process images for all rows in a dataframe given an image URL column."""
    processed_image_paths = []

    save_dir = save_dir.relative_to(cfg.ROOT)

    for index, row in df.iterrows():
        url = row[image_url_column]
        product_name = row[name_column]
        # create a safe filename using pathlib
        safe_name = re.sub(r'[^a-zA-Z0-9_\-]', '_', product_name).lower()
        save_path = save_dir / f"{safe_name}.png"
        save_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            processed_path = process_image_from_url(
                url,
                target_pixel_size,
                target_size_mb,
                save_path,
                overwrite
            )
            processed_path = processed_path.relative_to(processed_path.parents[1])
            
        except Exception as e:
            logger.warning(f"Error processing image for {product_name} from {url}: {e}")
            processed_path = url  # fallback to original URL if processing fails
        processed_image_paths.append(processed_path)

    df[image_url_column] = processed_image_paths
    return df


def process_image_from_url(url: str, target_pixel_size: tuple[int, int], target_size_mb: float, save_path: Path, overwrite: bool = False) -> Path:
    """Download, resize, and save an image from a URL."""

    if save_path.exists() and not overwrite:
        return save_path
    
    # Step 1: Download the image
    image_buffer = download_image(url)
    # Step 2: Resize to pixel dimensions
    image_buffer = resize_image_to_pixels(image_buffer, target_pixel_size)
    # Step 3: Resize to target size in MB
    image_buffer = resize_image_to_mb(image_buffer, target_size_mb)
    # Step 4: Save to disk
    with open(save_path, 'wb') as f:
        f.write(image_buffer.getbuffer())
    logger.debug(f"Processed image for URL {url} saved to {save_path}")

    return save_path


def download_image(url: str) -> io.BytesIO:
    """Download an image from a URL and return it as a BytesIO object."""
    headers = {
        "User-Agent": "Mozilla/5.0",
    }
    
    s = requests.Session()
    s.headers.update(headers)

    response = s.get(url)
    response.raise_for_status()
    return io.BytesIO(response.content)


def resize_image_to_pixels(image_buffer: io.BytesIO, target_size: tuple[int, int]) -> io.BytesIO:
    """Resize the image to fit within the target pixel dimensions."""
    image = Image.open(image_buffer)

    # the thumbnail method maintains aspect ratio
    image.thumbnail(target_size)

    output_buffer = io.BytesIO()
    image.save(output_buffer, format=image.format)
    output_buffer.seek(0)
    return output_buffer


def resize_image_to_mb(image_buffer: io.BytesIO, target_size_mb: float) -> io.BytesIO:
    """Resize the image to be under the target size in megabytes."""
    target_size_bytes = target_size_mb * 1024 * 1024
    image = Image.open(image_buffer)

    quality = 100
    output_buffer = io.BytesIO()
    image.save(output_buffer, format=image.format, quality=quality)
    
    while output_buffer.tell() > target_size_bytes and quality > 10:
        quality -= 5
        output_buffer = io.BytesIO()
        image.save(output_buffer, format=image.format, quality=quality)

    output_buffer.seek(0)
    return output_buffer


def get_final_url(doi_link):
    """
    Resolves a DOI link to its final redirected URL.
    """
    try:
        # requests.get follows redirects by default (allow_redirects=True)
        response = requests.get(
            doi_link, 
            allow_redirects=True, 
            timeout=10, 
            headers={"User-Agent": "Mozilla/5.0", "Referer": "https://scholar.google.com"})
        
        # Check if the request was successful
        if response.status_code == 200:
            return response.url
        else:
            return f"Error: Request failed with status code {response.status_code}"
            
    except requests.exceptions.RequestException as e:
        return f"Error during request: {e}"
