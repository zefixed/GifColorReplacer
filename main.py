import argparse
import os
from PIL import Image, ImageSequence
import numpy as np
from tqdm import tqdm


def hex_to_rgb(hex_color):
    """
    Converts a HEX color (either #RRGGBB or RRGGBB) to RGB.

    Arguments:
        hex_color (str): Color in HEX format, for example, "#33CCCC" or "33CCCC".

    Returns:
        tuple: A tuple with three values (R, G, B).

    Exceptions:
        ValueError: If the HEX color is incorrect (not 6 characters long).
    """
    hex_color = hex_color.lstrip("#")
    if len(hex_color) == 1:
        hex_color = hex_color * 6
    elif len(hex_color) == 2:
        hex_color = hex_color * 3
    elif len(hex_color) == 3:
        hex_color = hex_color * 2
    elif len(hex_color) != 6:
        raise ValueError(f"Invalid HEX color: {hex_color}")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def replace_color_with_tolerance(
    input_path, output_path, target_color, replacement_color, tolerance=30, duration=100
):
    """
    Replaces the specified color (within the tolerance range) with another in a GIF animation.

    Arguments:
        input_path (str): Path to the input GIF file.
        output_path (str): Path to save the output GIF file.
        target_color (tuple): The color to replace, in the format (R, G, B).
        replacement_color (tuple): The new color to replace the target color, in the format (R, G, B).
        tolerance (int, optional): Tolerance for color replacement (default: 30).
        duration (int, optional): Frame duration in milliseconds (default: 100).

    Description:
        This function processes all frames of the GIF animation, replaces the target color within the tolerance
        range, and saves the result to a new file.
    """
    # Check if the output directory exists, if not, create it
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with Image.open(input_path) as img:
        frames = []
        total_frames = sum(
            1 for _ in ImageSequence.Iterator(img)
        )  # Count the number of frames

        print(f"Processing file {input_path}...")
        for frame in tqdm(
            ImageSequence.Iterator(img),
            total=total_frames,
            desc=f"Processing {os.path.basename(input_path)}",
        ):
            frame = frame.convert("RGBA")
            array = np.array(frame)  # Convert frame to NumPy array

            # Mask for pixels within the tolerance range
            mask = np.all(
                np.abs(array[:, :, :3] - np.array(target_color)) <= tolerance, axis=-1
            )

            # Copy the alpha channel separately
            alpha_channel = array[:, :, 3]

            # Replace color with the new one (RGB), alpha channel remains unchanged
            array[mask] = [
                *replacement_color,
                255,
            ]  # Set new color and full opacity (255)

            # Restore the alpha channel
            array[:, :, 3] = alpha_channel

            # Convert back to Image object
            frames.append(Image.fromarray(array, "RGBA"))

        # Check the output file extension
        if not output_path.lower().endswith(".gif"):
            output_path += ".gif"

        print(f"Saving result to {output_path}...")
        # Save all frames as a new GIF
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            loop=0,
            duration=duration,
        )
        print(f"File {output_path} successfully created!")


def get_unique_filename(base_path):
    """
    Generates a unique file name by adding a number if the file already exists.

    Arguments:
        base_path (str): The file path to check for uniqueness.

    Returns:
        str: A unique file name.
    """
    # Split the path into base name and extension
    base, ext = os.path.splitext(base_path)
    if not ext:
        ext = ".gif"
        base_path += ext

    if not os.path.exists(base_path):
        return base_path

    counter = 1
    # Find a unique name by adding a counter
    while os.path.exists(f"{base}_{counter}{ext}"):
        counter += 1
    return f"{base}_{counter}{ext}"


# Command-line argument setup
parser = argparse.ArgumentParser(
    description="A script to replace a color in one or more GIF animations with tolerance."
)
parser.add_argument(
    "-i",
    "--input",
    required=True,
    nargs="+",
    help="Path to one or more input GIF files (can specify multiple files separated by spaces)",
)
parser.add_argument(
    "-o",
    "--output",
    help="Name of the output file (without path). If not specified, the input name is used with '_processed' appended.",
)
parser.add_argument(
    "-od",
    "--output-dir",
    help="Directory to save the processed files. If not specified, files are saved in the same directory as the input.",
)
parser.add_argument(
    "-oc",
    "--old-color",
    required=True,
    help="The old color to replace, in R G B or HEX format (e.g., '51 204 204' or '#33CCCC')",
)
parser.add_argument(
    "-nc",
    "--new-color",
    required=True,
    help="The new color to replace the old color with, in R G B or HEX format (e.g., '201 59 187' or '#C93BBB')",
)
parser.add_argument(
    "-t",
    "--tolerance",
    type=int,
    default=30,
    help="The tolerance for color replacement (default: 30)",
)
parser.add_argument(
    "-d",
    "--duration",
    type=int,
    default=100,
    help="Time between frames in milliseconds (default: 100). It is not recommended to set it below 20",
)
parser.add_argument(
    "-f",
    "--force",
    action="store_true",
    help="Overwrite existing files without adding a number. Doesn't work with multiple input.",
)

args = parser.parse_args()

# Check input files
for input_file in args.input:
    if not os.path.isfile(input_file):
        print(f"File {input_file} not found. Please specify an existing file.")
        exit(1)

# Define old and new colors
try:
    if " " in args.old_color:  # If color is in R G B format
        old_color = tuple(map(int, args.old_color.split()))
    else:  # If color is in HEX format
        old_color = hex_to_rgb(args.old_color)

    if " " in args.new_color:  # If color is in R G B format
        new_color = tuple(map(int, args.new_color.split()))
    else:  # If color is in HEX format
        new_color = hex_to_rgb(args.new_color)
except ValueError as e:
    print(f"Error: {e}")
    exit(1)

# Process each input file
for input_file in args.input:
    # Determine the output file path
    if args.output:
        if not args.output_dir:
            # If the output parameter (-o) is specified and output_dir (-od) is not, save to the current directory
            output_gif = args.output

            if os.path.isabs(output_gif) or "\\" in output_gif or "/" in output_gif:
                print(
                    "Error: the '-o' parameter cannot contain a path. Specify only the file name."
                )
                exit(1)

            if os.path.exists(output_gif) and not args.force:
                output_gif = get_unique_filename(output_gif)  # Generate a unique name
            else:
                output_gif = os.path.join(
                    os.getcwd(), output_gif
                )  # Save in the current directory
        else:
            # If both parameters -o and -od are specified, save in the specified directory with the name from -o
            output_gif = os.path.join(args.output_dir, args.output)

            if os.path.exists(output_gif) and not args.force:
                output_gif = get_unique_filename(
                    os.path.join(args.output_dir, args.output)
                )
    elif not args.output:
        if args.output_dir:
            # If the -od flag for the directory is specified and -o is not, save in the specified directory with _processed appended
            output_gif = os.path.join(
                args.output_dir,
                os.path.basename(input_file).replace(".gif", "_processed.gif"),
            )
            if os.path.exists(output_gif) and not args.force:
                output_gif = get_unique_filename(output_gif)
        else:
            # If neither -o nor -od is specified, save in the current directory with _processed appended
            output_gif = os.path.splitext(input_file)[0] + "_processed.gif"
            if os.path.exists(output_gif) and not args.force:
                output_gif = get_unique_filename(output_gif)

    # Check if the file exists and the --force flag
    if os.path.exists(output_gif) and not args.force:
        output_gif = get_unique_filename(output_gif)  # Generate a unique name

    replace_color_with_tolerance(
        input_file, output_gif, old_color, new_color, args.tolerance, args.duration
    )
