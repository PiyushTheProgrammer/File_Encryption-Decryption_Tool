from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

class CryptoUtils:
    @staticmethod
    def generate_key():
        """Generate a new Fernet key"""
        return Fernet.generate_key().decode()

    @staticmethod
    def get_fernet_key(key: str):
        """Convert a password/key into a valid Fernet key using PBKDF2"""
        salt = b'datacrypt_salt'  # In production, use a random salt and store it with the file
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key_bytes = key.encode()
        key = base64.urlsafe_b64encode(kdf.derive(key_bytes))
        return Fernet(key)

    @staticmethod
    def get_project_dir():
        """Get the project directory"""
        # Get the directory where the script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Return the parent directory (project directory)
        return os.path.dirname(script_dir)

    @staticmethod
    def encrypt_file(file_path: str, key: str, delete_original: bool = False) -> tuple[bool, str]:
        """
        Encrypt a file using Fernet encryption
        Returns: (success: bool, message: str)
        """
        try:
            # Get the directory of the original file
            file_dir = os.path.dirname(file_path)

            # Get the original filename
            original_filename = os.path.basename(file_path)

            # Create encrypted file path with 'encrypted_' prefix in the same directory
            encrypted_path = os.path.join(file_dir, "encrypted_" + original_filename)

            # Get Fernet instance
            fernet = CryptoUtils.get_fernet_key(key)

            # Read and encrypt file
            with open(file_path, 'rb') as file:
                file_data = file.read()

            encrypted_data = fernet.encrypt(file_data)

            # Write encrypted data
            with open(encrypted_path, 'wb') as file:
                file.write(encrypted_data)

            # Delete original if requested
            if delete_original:
                os.remove(file_path)

            return True, "File encrypted successfully!"

        except Exception as e:
            return False, f"Encryption failed: {str(e)}"

    @staticmethod
    def decrypt_file(file_path: str, key: str, delete_encrypted: bool = False) -> tuple[bool, str]:
        """
        Decrypt a file using Fernet encryption
        Returns: (success: bool, message: str)
        """
        try:
            # Get the directory of the encrypted file
            file_dir = os.path.dirname(file_path)

            # Get the original filename (remove 'encrypted_' prefix if present)
            original_filename = os.path.basename(file_path)
            if original_filename.startswith("encrypted_"):
                decrypted_filename = original_filename[len("encrypted_"):]
            else:
                decrypted_filename = "decrypted_" + original_filename

            # Create decrypted file path in the same directory
            decrypted_path = os.path.join(file_dir, decrypted_filename)

            # Get Fernet instance
            fernet = CryptoUtils.get_fernet_key(key)

            # Read and decrypt file
            with open(file_path, 'rb') as file:
                encrypted_data = file.read()

            try:
                decrypted_data = fernet.decrypt(encrypted_data)
            except Exception:
                return False, "Invalid key or corrupted file"

            # Write decrypted data
            with open(decrypted_path, 'wb') as file:
                file.write(decrypted_data)

            # Delete encrypted file if requested
            if delete_encrypted:
                os.remove(file_path)

            return True, "File decrypted successfully!"

        except Exception as e:
            return False, f"Decryption failed: {str(e)}"