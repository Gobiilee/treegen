from pathlib import Path
import re


def create_structure_from_tree(tree_file: str, output_dir: str = "."):
    """
    Create folders and files from a tree structure text file.
    """

    output_dir = Path(output_dir)
    lines = Path(tree_file).read_text(encoding="utf-8").splitlines()

    stack = []
    root_created = False

    for line in lines:
        if not line.strip():
            continue

        # Remove tree drawing characters
        clean = re.sub(r"[├└│─]+", "", line).rstrip()

        if not clean.strip():
            continue

        name = clean.strip()

        # Calculate depth from indentation
        depth = (len(clean) - len(clean.lstrip())) // 4

        while len(stack) - 1 > depth:
            stack.pop()

        if name.endswith("/"):
            folder_name = name[:-1]

            if not root_created:
                current_path = output_dir / folder_name
                root_created = True
            elif stack:
                current_path = stack[-1] / folder_name
            else:
                current_path = output_dir / folder_name

            current_path.mkdir(parents=True, exist_ok=True)
            stack.append(current_path)

            print(f"[DIR ] {current_path}")

        else:
            if stack:
                file_path = stack[-1] / name
            else:
                file_path = output_dir / name

            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.touch(exist_ok=True)

            print(f"[FILE] {file_path}")


if __name__ == "__main__":
    create_structure_from_tree(
        tree_file=r"D:\5_Gobi\Project\RoboCopy\treegen_py\structure_treegen.txt",
        output_dir=r"D:\5_Gobi\Project\RoboCopy"
    )