from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import mimetypes

@csrf_exempt
def Cryptography(request):
    result = ""
    if request.method == "POST":
        key = request.POST.get('key')
        iv = request.POST.get('iv')
        action = request.POST.get('action')
        uploaded_file = request.FILES.get('file')

        try:
            # Ensure the key and IV are correct lengths
            key = key.encode('utf-8')
            iv = iv.encode('utf-8')

            if len(key) not in [16, 24, 32]:
                raise ValueError("Key must be 16, 24, or 32 bytes long.")
            if len(iv) != 16:
                raise ValueError("IV must be 16 bytes long.")

            cipher = AES.new(key, AES.MODE_CBC, iv)

            if uploaded_file:
                file_data = uploaded_file.read()
                
                if action == "encrypt":
                    encrypted_data = cipher.encrypt(pad(file_data, AES.block_size))
                    response = HttpResponse(encrypted_data, content_type='application/octet-stream')
                    response['Content-Disposition'] = f'attachment; filename="encrypted_{uploaded_file.name}"'
                    return response

                elif action == "decrypt":
                    decrypted_data = unpad(cipher.decrypt(file_data), AES.block_size)
                    response = HttpResponse(decrypted_data, content_type='application/octet-stream')
                    response['Content-Disposition'] = f'attachment; filename="decrypted_{uploaded_file.name}"'
                    return response

            else:
                plaintext = request.POST.get('plaintext')
                if action == "encrypt":
                    # Encrypt the plaintext
                    plaintext_bytes = plaintext.encode('utf-8')
                    ciphertext = cipher.encrypt(pad(plaintext_bytes, AES.block_size))
                    result = base64.b64encode(ciphertext).decode('utf-8')

                elif action == "decrypt":
                    ciphertext = base64.b64decode(plaintext + '===')
                    plaintext_bytes = unpad(cipher.decrypt(ciphertext), AES.block_size)
                    result = plaintext_bytes.decode('utf-8')
                    
        except Exception as e:
            result = f"Error: {str(e)}"

    return render(request, 'Cryptography.html', {'result': result})


def homePage(request):
    return render(request, 'home.html')

def Aboutus(request):
    return render(request, 'aboutus.html')

def Read_more(request):
    return render(request, 'read_more.html')

def PrivacyPolicy(request):
    return render(request, 'privacypolicy.html')
