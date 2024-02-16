# Генерация паролей из содержимого дисковых объектов

Утилита командной строки для генерации паролей основываясь на дисковых объектах

## Установка

Для начала

Linux:

```sh
git clone https://github.com/Tumpa-Prizrak/ndtpProjectFeb.git
cd ndtpProjectFeb
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Windows (Powershell):

```powershell
git clone https://github.com/Tumpa-Prizrak/ndtpProjectFeb.git
cd ndtpProjectFeb
py -m venv venv
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Linux:

```sh
cd src
pyinstaller --clean -F passwgen.py --distpath ../output/dist --workpath ../output/build
cd ..
mv output/dist/passwgen /sbin/passwgen
chmod +x /sbin/passwgen
rm -rf output
rm src/passwgen.spec
```
