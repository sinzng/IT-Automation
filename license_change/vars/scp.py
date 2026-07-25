import pexpect
import os


def scp_send(local_file, remote_file_path, remote_host, remote_user, remote_password, port):    
    # scp 명령어 실행
    command = f'scp -P{port} ' \
          f'-o "HostKeyAlgorithms=+ssh-rsa" ' \
          f'-o "HostKeyAlgorithms=+ssh-dss" ' \
          f'-o "KexAlgorithms=+diffie-hellman-group-exchange-sha1" ' \
          f'-o "KexAlgorithms=+diffie-hellman-group1-sha1" ' \
          f'-o "KexAlgorithms=+diffie-hellman-group14-sha1" ' \
          f'{local_file} {remote_user}@{remote_host}:{remote_file_path}'

    try: 
        # scp 명령어 실행 및 expect로 패스워드 입력
        child = pexpect.spawn(command)

        # "connecting" 프롬프트 대기
        index = child.expect(['continue connecting', pexpect.TIMEOUT], timeout=5)

        # connecting 프롬프트가 나오면 'yes' 입력
        if index == 0:
            child.sendline('yes')

        # 패스워드 입력
        child.expect('password:')
        child.sendline(remote_password)

        # 파일 전송 완료 대기
        child.expect(pexpect.EOF)
        print(f"파일 전송 완료: {local_file}")
    
    except pexpect.ExceptionPexpect as e:
        print(f"파일 전송 중 오류 발생: {e}")


# 로컬 파일 (환경변수)
sh_file = os.environ.get('script_path', '')
jeus_file = os.environ.get('jeus_zip_path')
webtob_file = os.environ.get('webtob_zip_path')

# 대상 경로 및 접속 정보 (환경변수)
remote_file_path = os.environ.get('output_path', '')
remote_host = os.environ.get('host_ip')
remote_user = os.environ.get('user', '')
remote_password = os.environ.get('password', '')
port = os.environ.get('port', '')

# 파일별 전송 (환경변수가 설정된 경우만)
for label, file_path in [('스크립트', sh_file), ('JEUS', jeus_file), ('WEBTOB', webtob_file)]:
    if file_path:
        print(f"[SEND] {label} 파일 전송 시작")
        scp_send(file_path, remote_file_path, remote_host, remote_user, remote_password, port)
    else:
        print(f"[SKIP] {label} 파일이 정의되지 않아 전송 생략됨")