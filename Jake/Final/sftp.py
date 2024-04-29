import os

def main():
    os.system(r'sftp -b C:\Users\jarki\Desktop\sftp_commands.txt admin@192.168.1.12')
    print("Sent server output.csv")


if __name__ == "__main__":
    main()