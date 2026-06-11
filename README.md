# ComfyUI Clean Image Metadata

A tiny ComfyUI custom node that saves images without ComfyUI prompt/workflow
metadata.

It is useful when you want to share an output image without embedding the
workflow, prompt, or extra ComfyUI PNG info.

## Node

- `Save Image Without Metadata`

## Install

Clone this repository into your ComfyUI custom nodes folder:

```powershell
cd C:\Users\Administrator\Documents\ComfyUI\custom_nodes
git clone https://github.com/cp199712138-design/ComfyUI-CleanImageMetadata.git
```

Restart ComfyUI, then search for:

```text
Save Image Without Metadata
```

## Usage

Use it as a replacement for ComfyUI's built-in `Save Image` node.

Connect your image output to `images`, then run the workflow. The saved file
will not include ComfyUI prompt/workflow metadata.

## Parameters

- `filename_prefix`: Output filename prefix. This only affects the filename and
  is not written into image metadata.
- `format`: Recommended default is `PNG`. PNG is lossless and does not reduce
  image quality. JPEG is lossy and can reduce quality.
- `png_compress_level`: Recommended default is `4`. This only affects file size
  and save speed, not image quality. `0` is fastest and largest; `9` is smallest
  and slower.
- `jpeg_quality`: Recommended default is `100`. JPEG is still a lossy format;
  higher values are closer to the original image but create larger files.

## Notes

- No extra pip dependencies.
- Does not modify ComfyUI's built-in `Save Image` node.
- Does not remove visible watermarks or anything baked into pixels.
- Supports PNG and JPEG.
