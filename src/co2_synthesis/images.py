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
from PIL import Image, ImageChops
from pathlib import Path
import pandas as pd
from loguru import logger
from . import cfg


def process_images_in_df(
        df: pd.DataFrame, 
        name_column: str="card-title",
        image_url_column: str="card-image", 
        save_dir=cfg.ROOT / "docs/images/", 
        target_size_mb: float=0.4, 
        overwrite: bool=False
    ) -> pd.DataFrame:
    """Process images for all rows in a dataframe given an image URL column."""
    processed_image_paths = []

    for _, row in df.iterrows():
        url = row[image_url_column]
        product_name = row[name_column]
        # create a safe filename using pathlib
        safe_name = re.sub(r'[^a-zA-Z0-9_\-]', '_', product_name).lower()
        save_path = save_dir / f"{safe_name}.png"
        save_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            logger.debug(f"Processing image for {product_name} from {url}")
            processed_path = process_image_from_url(
                url,
                save_path=save_path,
                target_size_mb=target_size_mb,
                overwrite=overwrite
            )
            relative_to = cfg.ROOT / "docs/" if cfg.LOCAL_BUILD else cfg.ROOT
            processed_path = processed_path.relative_to(relative_to)
            
        except Exception as e:
            logger.warning(f"Error processing image for {product_name} from {url}: {e}")
            processed_path = url  # fallback to original URL if processing fails
        processed_image_paths.append(processed_path)

    df[image_url_column] = processed_image_paths
    return df


def process_image_from_url(url: str, save_path: Path, target_size_mb: float=0.3, overwrite: bool = False) -> Path:
    """Download, resize, and save an image from a URL."""

    if save_path.exists() and not overwrite:
        return save_path
    
    # Step 1: Download the image
    image = download_image(url)
    # Step 3: Resize to target size in MB
    image_trimmed = trim_image(image)
    image_downsized = resize_image_to_mb(image_trimmed, target_size_mb)
    # Step 4: Save to disk
    image_downsized.save(save_path, format="png")
    logger.debug(f"Processed image for URL {url} saved to {save_path}")

    return save_path


def download_image(url: str) -> Image.Image:
    """Download an image from a URL and return it as a PIL Image object."""
    headers = {
        "User-Agent": "Mozilla/5.0",
    }
    
    s = requests.Session()
    s.headers.update(headers)

    response = s.get(url)
    response.raise_for_status()
    bytes = io.BytesIO(response.content)
    image = Image.open(bytes)
    return image


def resize_image_to_pixels(image: Image.Image, target_size: tuple[float, float]) -> Image.Image:
    """Resize the image to fit within the target pixel dimensions."""
    image = image.copy()
    # the thumbnail method maintains aspect ratio
    image.thumbnail(target_size)

    return image


def resize_image_to_mb(image: Image.Image, target_size_mb: float) -> Image.Image:
    """Resize the image to be under the target size in megabytes."""
    target_size_bytes = target_size_mb * 1024 * 1024
    image = image.copy()

    output_buffer = io.BytesIO()
    image.save(output_buffer, format="png")

    while output_buffer.tell() > target_size_bytes:
        new_dims = tuple([int(dim * 0.9) for dim in image.size])
        output_buffer = io.BytesIO()
        image = resize_image_to_pixels(image, new_dims)
        image.save(output_buffer, format="png")

    output_buffer.seek(0)
    image = Image.open(output_buffer)
    return image


def trim_image(im:Image.Image) -> Image.Image:
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)
    else:
        return im  # no contents found


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
