# JPWO QA Automation (Python)

End-to-end test automation project for the JPWO course:
- API tests (pytest + requests)
- UI tests (pytest + selenium, headless Chrome)
- BDD refactor (pytest-bdd, Gherkin .feature files)
- Documentation: test plan, cases, and final test report
- Dockerized runner

System under test (SUT):
- Practice Software Testing (API + web UI)
- Repo: https://github.com/testsmith-io/practice-software-testing
- Default URLs (can be overridden in .env):
  - BASE_URL=https://api.practicesoftwaretesting.com
  - UI_BASE_URL=https://practicesoftwaretesting.com

## Stack
Python 3.12, pytest, requests, selenium, pytest-bdd, python-dotenv, Docker. Optional: allure-pytest for reports.

## Configuration
Copy .env.example to .env and set:
- BASE_URL          # API base (default: https://api.practicesoftwaretesting.com)
- AUTH_TOKEN        # optional bearer token if needed
- TIMEOUT           # request timeout in seconds
- UI_BASE_URL       # UI start URL (default: https://practicesoftwaretesting.com)
- HEADLESS=true     # recommended for Docker/CI


## Quick start
Local
1) pip install -r requirements.txt
2) pytest -q -m api        # run API tests
3) pytest -q -m ui         # run UI tests (needs Chrome/Chromedriver)
4) pytest -q -m bdd        # run BDD scenarios

Docker
1) docker build -t jpwo-qa .
2) docker run --rm --env-file .env jpwo-qa                 # all tests
   - docker run --rm --env-file .env jpwo-qa pytest -m api   # API only
   - docker run --rm --env-file .env jpwo-qa pytest -m ui    # UI only
