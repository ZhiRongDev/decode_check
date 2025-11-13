import sys
import base64
from Crypto.Cipher import DES3
from Crypto.Util.Padding import unpad
import os


def main():
    """
    Example usage: python decode.py input_file.json
    """
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <input_file.json>")
        sys.exit(1)

    input_file = sys.argv[1]
    base_name, ext = os.path.splitext(input_file)
    output_file = f"{base_name}_out.json"

    # === Step 1: Read JSON file content ===
    with open(input_file, "r") as f:
        b64_data = f.read().strip()

    # === Step 2: Base64 decode ===
    cipher_bytes = base64.b64decode(b64_data)

    # === Step 3: Compose key ===
    key_str = "CB" + "".join(
        chr(i) for i in range(67, 89)
    )  # "CBCDEFGHIJKLMNOPQRSTUVWX"
    key = key_str.encode("utf-8")

    # === Step 4: Try decryption ===
    iv = b"20160808"
    try:
        cipher = DES3.new(key, DES3.MODE_CBC, iv)
        decrypted = cipher.decrypt(cipher_bytes)
        # Attempt to remove padding
        try:
            decrypted_text = unpad(decrypted, DES3.block_size).decode("utf-8")
        except ValueError:
            decrypted_text = decrypted.decode("utf-8", errors="ignore")

        # === Step 5: Write to output file ===
        with open(output_file, "w", encoding="utf-8") as f_out:
            f_out.write(decrypted_text)

        print(f"Decrypted content written to {output_file}")

    except Exception as e:
        print(f"Decryption failed: {e}")


if __name__ == "__main__":
    main()
