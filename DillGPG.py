import gnupg
import dill
import sys


class DillGPG:
    def __init__(self,gpghome='~/.gnupg',algo='AES256'):
        self.gpg = gnupg.GPG(gnupghome=gpghome,use_agent=True)
        self.algo = algo

    def save(self, obj, filename, passwd):
        serialized_string = dill.dumps(obj)
        encrypted_data = self.gpg.encrypt(serialized_string,None,
                symmetric=self.algo,passphrase=passwd)
        if encrypted_data.ok != True:
            print("Error saving encrypted data:")
            print(encrypted_data.status)
            sys.exit(1)
        else:
            with open(filename,"w") as file_out:
                file_out.write(encrypted_data.data)

    def open(self, filename, passwd):
        with open(filename,"r") as file_in:
            decrypted_data = self.gpg.decrypt(file_in.read(),passphrase=passwd)
            if decrypted_data.ok != True:
                print("Error opening encrypted data:")
                print(decrypted_data.status)
                sys.exit(1)
            else:
                obj = dill.loads(decrypted_data.data)
                return obj


def test():
    dgpg = DillGPG()
    obj = {"test": 5, "blah": [1,3,5]}
    dgpg.save(obj,"test")
    obj2 = dgpg.open("test")
    print(obj2)
    


if __name__ == '__main__':
    test()
