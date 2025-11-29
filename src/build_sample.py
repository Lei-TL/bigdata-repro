from pathlib import Path

import yaml
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "configs" / "config.yaml"


def main():
    print("[build_sample] ROOT:", ROOT)
    print("[build_sample] CONFIG_PATH:", CONFIG_PATH)

    # 1. Đọc config
    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    data_cfg = config["data"]
    raw_big_path = ROOT / data_cfg["raw_big_path"]
    sample_path = ROOT / data_cfg["sample_path"]
    n_rows = int(data_cfg["sample_n_rows"])
    random_state = int(data_cfg["random_state"])

    print("[build_sample] RAW:", raw_big_path)
    print("[build_sample] SAMPLE:", sample_path)
    print("[build_sample] N_ROWS:", n_rows)
    print("[build_sample] SEED:", random_state)

    # 2. Kiểm tra file raw
    if not raw_big_path.exists():
        raise FileNotFoundError(f"Raw CSV not found: {raw_big_path}")

    sample_path.parent.mkdir(parents=True, exist_ok=True)

    # 3. Đọc file lớn
    print("[build_sample] Reading raw dataset...")
    df_big = pd.read_csv(raw_big_path)
    print("[build_sample] Raw shape:", df_big.shape)

    # 4. Lấy sample reproducible
    if n_rows < len(df_big):
        print("[build_sample] Sampling...")
        df_sample = df_big.sample(n=n_rows, random_state=random_state)
    else:
        print("[build_sample] sample_n_rows >= số dòng, dùng toàn bộ dữ liệu.")
        df_sample = df_big

    # 5. Lưu sample
    df_sample.to_csv(sample_path, index=False)
    print(f"[build_sample] Saved sample {df_sample.shape} to {sample_path}")


if __name__ == "__main__":
    main()
