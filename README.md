## Skład zespołu:

- Siarhei Drozd
- Natan Orzechowski

# Uruchamianie
```
python -m venv .venv
source .venv/bin/activate lub .\.venv\Scripts\activate
pip install -r requirements.txt
python run_scenario0.py
```
Przed uruchomieniem każdego scenariusza, konieczne jest wskazanie właściwego pliku z danymi wejściowymi z folderu inputs. Np. dla scenariusza 0, w pliku settings.json wskazujemy "INPUT_FILE": "./inputs.case0.json".