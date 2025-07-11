
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import pandas as pd

def generate_eqsls_from_activation(activation_path: Path, callsign: str, output_dir: Path):
    qsl_photo_file = activation_path / "qsl_photo.txt"
    if not qsl_photo_file.exists():
        raise FileNotFoundError("qsl_photo.txt not found in activation path.")

    qsl_photo_name = qsl_photo_file.read_text().strip()
    background_path = activation_path / qsl_photo_name

    log_path = activation_path / "qsos.csv"
    if not log_path.exists():
        raise FileNotFoundError("qsos.csv not found in activation path.")

    qsos = pd.read_csv(log_path).to_dict(orient="records")
    output_dir.mkdir(parents=True, exist_ok=True)

    base_image = Image.open(background_path).convert("RGBA")
    width, height = base_image.size
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    font_large = ImageFont.truetype(font_path, 60)
    font_small = ImageFont.truetype(font_path, 24)

    for qso in qsos:
        img = base_image.copy()
        draw = ImageDraw.Draw(img)

        draw.text((50, 50), callsign, font=font_large, fill="white")

        table_top = height - 200
        table_left = 50
        cell_height = 40
        cell_padding = 10
        columns = ["TO STATION", "DATE", "FREQ", "MODE", "RST"]
        col_widths = [200, 150, 100, 100, 100]

        table_height = cell_height * 2
        table_width = sum(col_widths) + cell_padding * len(columns)
        overlay = Image.new("RGBA", (table_width, table_height), (255, 255, 255, 200))
        img.paste(overlay, (table_left, table_top), overlay)

        y = table_top + 8
        x = table_left
        for i, col in enumerate(columns):
            draw.text((x + cell_padding, y), col, font=font_small, fill="black")
            x += col_widths[i]

        y += cell_height
        x = table_left
        for i, col in enumerate(columns):
            value = str(qso.get(col, ""))
            draw.text((x + cell_padding, y), value, font=font_small, fill="black")
            x += col_widths[i]

        filename = f"eqsl_{qso['TO STATION']}.jpg"
        img.convert("RGB").save(output_dir / filename)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate eQSLs from activation folder.")
    parser.add_argument("--callsign", required=True, help="Activator callsign (e.g. EA3GNU)")
    parser.add_argument("--activation-path", required=True, help="Path to activation folder")
    parser.add_argument("--output-dir", default="output_eqsls", help="Output directory for eQSLs")
    args = parser.parse_args()

    generate_eqsls_from_activation(
        activation_path=Path(args.activation_path),
        callsign=args.callsign,
        output_dir=Path(args.output_dir)
    )
