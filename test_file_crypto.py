import requests
import os

# Configuration
BASE_URL = "http://127.0.0.1:8000"
ENCRYPT_URL = f"{BASE_URL}/crypto/"  # Adjust if the URL path is different
TEST_FILE = "test_image.png"
ENCRYPTED_FILE = "encrypted_" + TEST_FILE
DECRYPTED_FILE = "decrypted_" + TEST_FILE
KEY = "SixteenByteKey!!"  # 16 bytes
IV = "SixteenByteInitV"   # 16 bytes

def create_dummy_file():
    from PIL import Image
    img = Image.new('RGB', (100, 100), color = 'red')
    img.save(TEST_FILE)
    print(f"Created dummy file: {TEST_FILE}")

def test_encryption():
    print("Testing Encryption...")
    with open(TEST_FILE, 'rb') as f:
        files = {'file': f}
        data = {
            'key': KEY,
            'iv': IV,
            'action': 'encrypt'
        }
        response = requests.post(ENCRYPT_URL, files=files, data=data)
    
    if response.status_code == 200:
        with open(ENCRYPTED_FILE, 'wb') as f:
            f.write(response.content)
        print(f"Encryption successful. Saved to {ENCRYPTED_FILE}")
        return True
    else:
        print(f"Encryption failed: {response.status_code} - {response.text}")
        return False

def test_decryption():
    print("Testing Decryption...")
    with open(ENCRYPTED_FILE, 'rb') as f:
        files = {'file': f}
        data = {
            'key': KEY,
            'iv': IV,
            'action': 'decrypt'
        }
        response = requests.post(ENCRYPT_URL, files=files, data=data)
    
    if response.status_code == 200:
        with open(DECRYPTED_FILE, 'wb') as f:
            f.write(response.content)
        print(f"Decryption successful. Saved to {DECRYPTED_FILE}")
        return True
    else:
        print(f"Decryption failed: {response.status_code} - {response.text}")
        return False

def verify_content():
    print("Verifying content...")
    with open(TEST_FILE, 'rb') as f1, open(DECRYPTED_FILE, 'rb') as f2:
        if f1.read() == f2.read():
            print("SUCCESS: Decrypted file matches original file!")
        else:
            print("FAILURE: Decrypted file does not match original file.")

if __name__ == "__main__":
    try:
        create_dummy_file()
        if test_encryption():
            if test_decryption():
                verify_content()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Cleanup
        for f in [TEST_FILE, ENCRYPTED_FILE, DECRYPTED_FILE]:
            if os.path.exists(f):
                os.remove(f)
                pass
