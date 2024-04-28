import os

def main():
    os.system("sftp -b /home/jarkin/Iot-Project/transfer_commands.txt admin@192.168.1.12")


if __name__ == "__main__":
    main()