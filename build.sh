python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd src
pyinstaller --clean -F passwgen.py --distpath ../output/dist --workpath ../output/build
cd ..
mv output/dist/passwgen /sbin/passwgen
chmod +x /sbin/passwgen
rm -rf output
rm src/passwgen.spec