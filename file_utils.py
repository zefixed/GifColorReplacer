import os


def make_dir(path: str) -> str:
    output_dir = os.path.dirname(path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    return output_dir
