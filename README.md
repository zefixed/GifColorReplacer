# GIF Color Replacement Script

## Description
This script allows you to replace a specific color in one or more GIF animations with a new color, within a specified tolerance range. It supports both HEX and RGB color formats and allows you to specify an output file name and directory.

The script processes all frames of the input GIF and saves a new GIF with the modified colors.

## Features
- Replace any color in a GIF animation with a new one.
- Adjustable color tolerance for more flexible replacements.
- Supports both HEX (`#RRGGBB` or `RRGGBB`) and RGB (`R G B`) color formats.
- Allows you to specify output file names and directories.
- Overwrite existing files or generate unique filenames.

## Requirements
- Python 3.x
- `Pillow` (for image processing)
- `numpy` (for array manipulations)
- `tqdm` (for progress bar)

Install required libraries:
```bash
pip install -r requirements.txt
```

## Usage

### Command-Line Arguments:
- `-i`, `--input` (required): Path to one or more input GIF files. You can specify multiple files separated by spaces.
- `-o`, `--output`: Name of the output GIF file. If not specified, the input name will be used with `_processed` appended.
- `-od`, `--output-dir`: Directory to save the processed GIF files. If not specified, files are saved in the same directory as the input file.
- `-oc`, `--old-color` (required): The color to be replaced, in either RGB or HEX format. Example: `'51 204 204'`, `'#33CCCC'` or `'33CCCC'`.
- `-nc`, `--new-color` (required): The new color to replace the old color with, in RGB or HEX format. Example: `'201 59 187'`, `'#C93BBB'` or `'C93BBB'`.
- `-t`, `--tolerance`: The tolerance for color replacement. Default is `30`. This defines the acceptable deviation from the target color for replacement.
- `-d`, `--duration`: Time between frames in milliseconds. Default is `100`. It is not recommended to set it below `20`.
- `-f`, `--force`: Force overwrite of existing files without adding a unique number to the file name. Doesn't work with multiple input.

### Example Usage:

1. **Replace a specific color in a GIF:**
   ```bash
   python main.py -i input.gif -oc "#FF0000" -nc "#00FF00" -d 100
   ```

2. **Process multiple GIF files and save the results in a specific directory:**
   ```bash
   python main.py -i input1.gif input2.gif -oc FF0000 -nc 00FF00 -od /path/to/output/
   ```

3. **Force overwrite the output file without renaming:**
   ```bash
   python main.py -i input.gif -oc FF0000 -nc 00FF00 -o output.gif -f
   ```

## Color Format:
- RGB format: `R G B` (e.g., `51 204 204`)
- HEX format: `#RRGGBB` or `RRGGBB` (e.g., `#33CCCC` or `33CCCC`)

## Color Replacement Logic:
The script uses a tolerance value to determine which pixels should be replaced. The target color is matched with all pixels within the given tolerance. The default tolerance is `30`, but you can adjust it based on the range of colors you want to replace.

## Notes:
- Ensure that your input GIFs are not too large, as processing might take time depending on the number of frames.
- The script saves the output in the same directory by default, appending `_processed` to the original filename unless specified otherwise.
- The script can overwrite files if the `--force` option is used.

## License:
This script is open-source and distributed under the MIT License. You are free to use, modify, and distribute it as per the terms of the license.