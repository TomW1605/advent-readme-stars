if __name__ == "__main__":
    from advent_readme_stars.constants import README_LOCATION
    from advent_readme_stars.update import update_readme

    with open(README_LOCATION, "r", encoding="UTF-8") as f:
        lines = f.read().splitlines()

    edited = update_readme(lines)

    with open(README_LOCATION, "w", encoding="UTF-8") as f:
        f.writelines([line + "\n" for line in edited])
