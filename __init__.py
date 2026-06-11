import os

import numpy as np
from PIL import Image

import folder_paths


TIP_PREFIX = (
    "\u8f93\u51fa\u6587\u4ef6\u540d\u524d\u7f00\u3002"
    "\u53ea\u5f71\u54cd\u6587\u4ef6\u540d\uff0c\u4e0d\u4f1a\u5199\u5165\u56fe\u7247\u5143\u6570\u636e\u3002"
)
TIP_FORMAT = (
    "\u63a8\u8350\u4fdd\u6301 PNG\u3002PNG \u662f\u65e0\u635f\u683c\u5f0f\uff0c"
    "\u4e0d\u4f1a\u538b\u7f29\u753b\u8d28\uff1bJPEG \u662f\u6709\u635f\u683c\u5f0f\uff0c"
    "\u6587\u4ef6\u66f4\u5c0f\u4f46\u753b\u8d28\u53ef\u80fd\u4e0b\u964d\u3002"
)
TIP_PNG_LEVEL = (
    "\u63a8\u8350\u4fdd\u6301\u9ed8\u8ba4 4\u3002PNG \u538b\u7f29\u7b49\u7ea7"
    "\u53ea\u5f71\u54cd\u6587\u4ef6\u5927\u5c0f\u548c\u4fdd\u5b58\u901f\u5ea6\uff0c"
    "\u4e0d\u5f71\u54cd\u753b\u8d28\u30020 \u6700\u5feb\u4f46\u6587\u4ef6\u6700\u5927\uff1b"
    "9 \u6587\u4ef6\u6700\u5c0f\u4f46\u4fdd\u5b58\u66f4\u6162\u3002"
)
TIP_JPEG_QUALITY = (
    "\u63a8\u8350 100\u3002JPEG \u672c\u8eab\u662f\u6709\u635f\u683c\u5f0f\uff0c"
    "\u6570\u503c\u8d8a\u9ad8\u8d8a\u63a5\u8fd1\u539f\u56fe\u4f46\u6587\u4ef6\u8d8a\u5927\uff1b"
    "\u6570\u503c\u8d8a\u4f4e\u6587\u4ef6\u8d8a\u5c0f\uff0c\u538b\u7f29\u75d5\u8ff9\u8d8a\u660e\u663e\u3002"
)


class SaveImageWithoutMetadata:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "filename_prefix": (
                    "STRING",
                    {"default": "NoMetadata", "tooltip": TIP_PREFIX},
                ),
                "format": (
                    ["PNG", "JPEG"],
                    {"default": "PNG", "tooltip": TIP_FORMAT},
                ),
                "png_compress_level": (
                    "INT",
                    {
                        "default": 4,
                        "min": 0,
                        "max": 9,
                        "step": 1,
                        "tooltip": TIP_PNG_LEVEL,
                    },
                ),
                "jpeg_quality": (
                    "INT",
                    {
                        "default": 100,
                        "min": 1,
                        "max": 100,
                        "step": 1,
                        "tooltip": TIP_JPEG_QUALITY,
                    },
                ),
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "save_images"
    OUTPUT_NODE = True
    CATEGORY = "image"
    DESCRIPTION = "Save images without ComfyUI prompt/workflow metadata."

    def save_images(
        self,
        images,
        filename_prefix="NoMetadata",
        format="PNG",
        png_compress_level=4,
        jpeg_quality=100,
    ):
        if len(images) == 0:
            return {"ui": {"images": []}}

        image_format = format.upper()
        extension = "png" if image_format == "PNG" else "jpg"

        full_output_folder, filename, counter, subfolder, filename_prefix = (
            folder_paths.get_save_image_path(
                filename_prefix,
                self.output_dir,
                images[0].shape[1],
                images[0].shape[0],
            )
        )

        results = []
        for image in images:
            array = 255.0 * image.cpu().numpy()
            img = Image.fromarray(np.clip(array, 0, 255).astype(np.uint8))

            file = f"{filename}_{counter:05}_.{extension}"
            path = os.path.join(full_output_folder, file)

            if image_format == "PNG":
                img.save(path, compress_level=png_compress_level)
            else:
                if img.mode != "RGB":
                    img = img.convert("RGB")
                img.save(path, format="JPEG", quality=jpeg_quality)

            results.append({"filename": file, "subfolder": subfolder, "type": self.type})
            counter += 1

        return {"ui": {"images": results}}


NODE_CLASS_MAPPINGS = {
    "SaveImageWithoutMetadata": SaveImageWithoutMetadata,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SaveImageWithoutMetadata": "Save Image Without Metadata",
}
