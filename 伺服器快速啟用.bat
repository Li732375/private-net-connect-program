@ECHO OFF

ECHO �]�w����������������������m
cd C:\Users\?\Desktop\python�@�~

ECHO �Y�� ngrok �C�����}�ȥ����i������'('����TOKEN�P�ഫ�����}�C���۲�')'
ECHO ���O�p�U ����󤺮e
::ngrok authtoken <YOUR_AUTH_TOKEN>

ECHO �ܺ���(�p�U)�� google �b��n�J�A���o���� AUTH_TOKEN
ECHO ���}�p�U ����󤺮e
::https://dashboard.ngrok.com/auth/your-authtoken

ECHO �O�o���}�� ngrok �C���O ngrok http 8000
ECHO �Ұʦ��A���A�եγs�� localhost:8000
ECHO Ctrl + C �Y�i����
python -m http.server 8000 --bind 127.0.0.1

PAUSE

ECHO finish
