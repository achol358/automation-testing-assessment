# শুরু এখান থেকে — IntelliJ IDEA + Python

এই প্রোজেক্টটি **IntelliJ IDEA** দিয়ে খুলতে হবে; VS Code লাগবে না। Language আগের মতো **Python**। UI টেস্ট **Playwright + Pytest**, API টেস্ট **Postman + Newman**।

## ধাপ ১: Install

- Python: https://www.python.org/downloads/ — Windows-এ Python PATH-এ যুক্ত করতে পারলে ভালো।
- IntelliJ IDEA: https://www.jetbrains.com/idea/download/
- Node.js LTS: https://nodejs.org/
- Postman: https://www.postman.com/downloads/
- Git: https://git-scm.com/downloads
- GitHub account: https://github.com/

Command Prompt/PowerShell-এ চেক করুন: `py --version`, `node --version`, `npm --version`, `git --version`।

## ধাপ ২: IntelliJ-তে Python plugin

1. IntelliJ IDEA খুলুন।
2. **File > Settings** অথবা `Ctrl+Alt+S`।
3. **Plugins > Marketplace**।
4. **Python Community Edition** লিখে খুঁজুন, **Install**, তারপর **Restart**।
5. Ultimate subscription থাকলে **Python** plugin-ও ব্যবহার করা যায়; free environment-এ **Python Community Edition** দিয়ে শুরু করা সহজ।

## ধাপ ৩: Folder খুলুন

1. ZIP Extract করুন।
2. IntelliJ welcome screen > **Open** > `Automation-Testing-Starter` folder নির্বাচন।
3. উপরে **View > Tool Windows > Terminal** (`Alt+F12`)।
4. Terminal path যেন যে folder-এ `requirements.txt` আছে, সেই folder হয়।

## ধাপ ৪: Python virtual environment

Terminal-এ এক লাইন করে চালান (Windows):

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m playwright install chromium
```

এখানে `.venv` হলো প্রোজেক্টের আলাদা Python environment। একবার তৈরি করলেই হবে। Python interpreter সেটিংসে `.venv\Scripts\python.exe` নির্বাচন করুন।

## ধাপ ৫: প্রথম UI পরীক্ষা (Q1)

```powershell
.\.venv\Scripts\python.exe -m pytest ui_tests/test_saucedemo.py -k test_q1_locked_out_user_error --headed -v
```

Chromium browser খুলে `locked_out_user` দিয়ে login চেষ্টা করবে, error message verify করবে। সফল হলে terminal-এ `PASSED` দেখা যাবে।

## ধাপ ৬: Q2, Q3, তারপর সব একসঙ্গে

```powershell
.\.venv\Scripts\python.exe -m pytest ui_tests/test_saucedemo.py -k test_q2_standard_user_three_products --headed -v
.\.venv\Scripts\python.exe -m pytest ui_tests/test_saucedemo.py -k test_q3_performance_glitch_z_to_a --headed -v
.\.venv\Scripts\python.exe -m pytest ui_tests/test_saucedemo.py --headed -v
```

`pytest.ini`-তে HTML রিপোর্ট সেট করা আছে, তাই **প্রতিবার** test run-এর পর `reports/ui_report.html` update হবে। Browser দিয়ে খুলে দেখুন।

## ধাপ ৭: Postman collections import

Postman > **Import** > দুইটি collection JSON file import করুন:

- `postman/reqres_main.postman_collection.json`
- `postman/reqres_negative_data.postman_collection.json`

ReqRes account তৈরি করে নিজের API key সংগ্রহ করুন: https://reqres.in/docs । Postman environment-এ `api_key` variable দিন। Legacy `/api` endpoint / login response আজকের সার্ভিসে কীভাবে কাজ করে, আগে Send করে যাচাই করুন। POST login-এর response `token` থাকলে collection সেটা `authToken` variable-এ রাখে।

## ধাপ ৮: Newman CLI এবং API HTML report

```powershell
npm install -g newman newman-reporter-html
Copy-Item postman/reqres_environment.example.json postman/reqres_environment.local.json
```

`reqres_environment.local.json` file-এর `api_key`-তে নিজের key দিন; **GitHub-এ key দেবেন না**।

```powershell
newman run postman/reqres_main.postman_collection.json -e postman/reqres_environment.local.json -r cli,html --reporter-html-export reports/api_report.html
newman run postman/reqres_negative_data.postman_collection.json -e postman/reqres_environment.local.json -d postman/invalid_cases.json -r cli,html --reporter-html-export reports/negative_api_report.html
```

ReqRes-এর demo endpoints বা authentication behavior বদলে যেতে পারে। কোনো assertion fail হলে actual status/response বুঝে শুদ্ধ test লিখুন; **জোর করে PASS দেখাবেন না**। Public demo PUT/PATCH persistence নিশ্চয়তা দেয় না, তাই "অন্য field বদলায়নি" requirement সম্পূর্ণ validate করতে persistent project ও read-back GET দরকার হতে পারে।

## ধাপ ৯: README ও GitHub

Project-এর মূল `README.md` পড়ুন। Public GitHub repository তৈরি করে code push করুন। `postman/reqres_environment.local.json` GitHub-এ upload করবেন না (`.gitignore`-এ exclude করা আছে)।

```powershell
git init
git add .
git commit -m "Add IntelliJ Python UI and Postman API assessment"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/automation-testing-assessment.git
git push -u origin main
```

`YOUR_USERNAME` নিজের GitHub username দিন। Push করার আগে Git-এ author name/email configured থাকা লাগতে পারে। URL user-facing public হয়েছে কি না verify করুন।

## Troubleshooting

- **`py` not recognized:** Python install / Windows PATH check করে IntelliJ restart করুন। `python --version` চেষ্টা করুন।
- **`No module named pytest`:** `requirements.txt` install করার আগে/পরে `.venv`-র Python ব্যবহার করেছেন কি না দেখুন।
- **Playwright browser missing:** `.\.venv\Scripts\python.exe -m playwright install chromium` চালান।
- **`(.venv)` দেখাচ্ছে না:** সমস্যা নয়; উপরের সব command `.venv\Scripts\python.exe` সরাসরি ব্যবহার করে।
- **`requirements.txt` not found:** IntelliJ Terminal-এ project root folder-এ আসুন।
- **ReqRes 401/403:** API key/env header/current docs check করুন; key public করে ফেলবেন না।

বিস্তারিত explanation এবং scenario map দেখতে `README.md` পড়ুন।
