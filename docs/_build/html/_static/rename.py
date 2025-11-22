import os

folder = os.getcwd()

for name in os.listdir(folder):
    if name.startswith("logo_") and name.endswith(".ico"):
        old_path = os.path.join(folder, name)

        # ubah prefix dari logo_... ke favicon_...
        new_name = "favicon_" + name[len("logo_"):]
        new_path = os.path.join(folder, new_name)

        # jika target sudah ada, skip
        if os.path.exists(new_path):
            print(f"[SKIP] {new_name} sudah ada")
            continue

        os.rename(old_path, new_path)
        print(f"RENAMED: {name} → {new_name}")
