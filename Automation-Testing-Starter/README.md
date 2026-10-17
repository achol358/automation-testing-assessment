# Automation Testing Assessment — Beginner Starter

A learning-oriented starter for the assessment: **three SauceDemo UI tests** and **ReqRes API tests**. It is designed for Windows PowerShell inside IntelliJ IDEA, Python, Playwright, Pytest, Postman and Newman.

## 1. Install once

- Python: https://www.python.org/downloads/ (select **Add Python to PATH** on Windows)
- IntelliJ IDEA: https://www.jetbrains.com/idea/download/ (install the **Python Community Edition** plugin via Settings > Plugins > Marketplace)
- Node.js LTS: https://nodejs.org/
- Postman desktop: https://www.postman.com/downloads/
- Git: https://git-scm.com/downloads
- Sign up for a free ReqRes API key: https://app.reqres.in/ . Check their current API authentication guidance.

## 2. Open the project in IntelliJ IDEA

1. Open IntelliJ IDEA > Settings (`Ctrl+Alt+S`) > Plugins > Marketplace.
2. Search **Python Community Edition** and install it; restart IntelliJ IDEA if prompted. The Ultimate Python plugin is another option if your edition supports it.
3. From IntelliJ's welcome screen choose **Open**, not **New Project**. Select the extracted folder **Automation-Testing-Starter**.
4. Open **View > Tool Windows > Terminal** (or `Alt+F12`). Make sure the terminal working directory is your project folder containing `requirements.txt`.
5. Run the commands below in the terminal (PowerShell):

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m playwright install chromium
```

If PowerShell blocks activation, **do not change Windows security settings just for this**. Instead skip activation and run commands through ` .\.venv\Scripts\python.exe` (remove the initial space), for example:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m playwright install chromium
.\.venv\Scripts\python.exe -m pytest ui_tests/test_saucedemo.py --headed -v
```

For code intelligence in IntelliJ, select your Python interpreter in **File > Project Structure > SDKs** or Python Interpreter settings, pointing it to `.venv\Scripts\python.exe`. The exact UI label can vary by version. Under **Settings > Tools > Python Integrated Tools**, set **Default test runner = pytest** if you want IntelliJ's right-click test run behavior. However, terminal commands work without the IDE test runner configured.

## 3. Run UI tests one at a time

```powershell
python -m pytest ui_tests/test_saucedemo.py -k test_q1_locked_out_user_error --headed -v
python -m pytest ui_tests/test_saucedemo.py -k test_q2_standard_user_three_products --headed -v
python -m pytest ui_tests/test_saucedemo.py -k test_q3_performance_glitch_z_to_a --headed -v
```

All three, in the **same sequential run** (pytest is sequential unless parallelism is explicitly enabled):

```powershell
python -m pytest ui_tests/test_saucedemo.py --headed -v --slowmo 250
```

The `pytest.ini` file is configured to generate/overwrite `reports/ui_report.html` **on every UI pytest run**. You can also choose an explicit report path:

```powershell
python -m pytest ui_tests/test_saucedemo.py -v --html=reports/ui_report.html --self-contained-html --screenshot=only-on-failure
```

View `reports/ui_report.html` with your browser.

## 4. API: import Postman collections

1. Open Postman > Import.
2. Import both:
   - `postman/reqres_main.postman_collection.json`
   - `postman/reqres_negative_data.postman_collection.json`
3. Create Postman environment named `ReqRes Local` and add `api_key` with your own ReqRes key. Activate the environment.
4. Open main collection. Send the requests **one by one**. Read the **Scripts > Post-response** tests and check passed/failed assertions.
5. Run the main collection in the runner. Its requests execute in their listed order.

**Important:** ReqRes legacy login normally returns a JSON field named `token`. This starter captures it in a collection variable called `authToken` to match the assessment. A login token and ReqRes `x-api-key` are not the same thing.

**Important:** The ReqRes demo PUT/PATCH endpoints echo an updated response, but demo changes do not necessarily persist. The PATCH assertion verifies the requested field and the response shape; a truly persistent "other fields unchanged" assertion requires a persistent API/project and an additional read-back request. See https://reqres.in/docs.

## 5. Run Postman collection from the command line

Install Newman (Node.js must already be installed):

```powershell
npm install -g newman newman-reporter-html
```

Make a **private** local environment file:

```powershell
Copy-Item postman/reqres_environment.example.json postman/reqres_environment.local.json
```

Open `postman/reqres_environment.local.json`, set `api_key` to your ReqRes API key. This file is in `.gitignore`: **do not upload secrets to GitHub**.

Run main collection with an HTML report:

```powershell
newman run postman/reqres_main.postman_collection.json -e postman/reqres_environment.local.json -r cli,html --reporter-html-export reports/api_report.html
```

Run stored-data negative requests as 3 iterations:

```powershell
newman run postman/reqres_negative_data.postman_collection.json -e postman/reqres_environment.local.json -d postman/invalid_cases.json -r cli,html --reporter-html-export reports/negative_api_report.html
```

`invalid_cases.json` is a stored data file. Each row is a bad login scenario. `expected_status` is asserted by Postman's JavaScript tests. If the live API responds with a different contract/status, investigate and document the difference instead of falsely marking a failed test as a pass.

## 6. GitHub public repo

Create a public, **empty** GitHub repository named `automation-testing-assessment` and run:

```powershell
git init
git add .
git commit -m "Add UI and API automation assessment"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/automation-testing-assessment.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username. Later updates: `git add .`, `git commit -m "Improve tests"`, `git push`.

## 7. Submission checklist

- [ ] Q1: locked-out login gives the required error.
- [ ] Q2: reset, add any three, check names, prices, subtotal/total, finish, reset and logout.
- [ ] Q3: slow user, reset, sort descending, add first item, checkout, verify, reset and logout.
- [ ] Each UI test runs independently, plus all three run sequentially.
- [ ] `reports/ui_report.html` generated after a run.
- [ ] API login response `token` captured in `authToken`.
- [ ] GET user compares name/email against predefined expected data.
- [ ] PUT checks `updatedAt` plus returned data.
- [ ] PATCH checks one requested field and `updatedAt`; understand the demo persistence limitation.
- [ ] Bad requests have status assertions and stored-data iterations.
- [ ] Postman collection JSON(s) committed to GitHub.
- [ ] `README.md` instructions work on your own machine.
- [ ] Public GitHub repository URL submitted; **no API keys uploaded**.

### Expected results

On the current live services and configured credentials, tests are intended to pass. The files were **syntax-checked** as a starter; **live end-to-end execution has not been claimed**. Run them yourself and update selectors/expectations if the external sites change.
