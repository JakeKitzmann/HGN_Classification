import PupilTracker
import paramiko

def send_file_to_pi(local_path, remote_path, pi_address, pi_username, pi_password):
    # Create an SSH client
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the Raspberry Pi
        ssh_client.connect(pi_address, username=pi_username, password=pi_password)

        # Use SCP to transfer the file
        scp_client = ssh_client.open_sftp()
        scp_client.put(local_path, remote_path)
        scp_client.close()

        print("File transferred successfully.")

    except Exception as e:
        print("An error occurred:", str(e))

    finally:
        # Close the SSH connection
        ssh_client.close()

def main():

    # create object
    pt = PupilTracker.PupilTracker()

    # live run
    #pt.runLive('Jake/Final/output.csv')

    # record video
    #pt.record('Jake/Final/test.mp4')

    # process recording
    pt.runVideo(video = 'GUI/videoTests/longTest.mp4', threshold = 115, output = 'Jake/Final/output.csv')

    local_path = "Jake/Final/output.csv"
    remote_path = "/home/admin/Project"
    pi_ip = "192.168.1.9"
    pi_username = "admin"
    pi_password = "admin1"

    send_file_to_pi(local_path, remote_path, pi_ip, pi_username, pi_password)


if __name__ == "__main__":
    main()
    