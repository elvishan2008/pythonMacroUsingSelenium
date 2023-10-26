# maindriver=None time
import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from browsermobproxy import Server
import json
import subprocess
import time
import sudokuSolver
import requests

import macro_config as mc

driver_path = "C:/Program Files/Google/Chrome/Application/chromedriver.exe"

subprocess.Popen(
    r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chromeCookie"')

# bmp_path = 'C:/Program Files/browsermob-proxy-2.1.4/bin/browsermob-proxy'
# server = Server(bmp_path)
# server.start()
# proxy = server.create_proxy()

logging_prefs = {
    'browser': 'ALL',
    'driver': 'ALL',
    'performance': 'ALL'
}

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--ignore-certificate-errors')
# chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy))
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
chrome_options.add_experimental_option('perfLoggingPrefs', {'enableNetwork': True})
chrome_options.set_capability('goog:loggingPrefs', logging_prefs)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


# proxy.new_har("sudoku")

# 반응 속도 테스트 매크로
def run_ex1(driver):
    driver.get(mc.ex1_url)
    driver.maximize_window()  # 창 크게 만들기

    time_duration = 1
    time.sleep(time_duration)

    element = driver.find_element(By.ID, 'start')
    element.click()
    for i in range(50, 0, -1):
        print(i)
        element = driver.find_element(By.XPATH, f'/html/body/ul/li/div/div[1]/button[{i}]/b')
        element.click()
        time_duration = 0.05
        time.sleep(time_duration)

    time_duration = 10
    time.sleep(time_duration)
    driver.quit()


def run_wrong_ex2(driver):
    driver.get(mc.ex2_url)
    try:
        driver.maximize_window()  # 창 크게 만들기
    except selenium.common.exceptions.WebDriverException:
        pass  # 이미 창이 최대화된 상태이므로, 이 오류를 무시합니다.

    wait = WebDriverWait(driver, 10)  # 10초 기다림
    wait.until(EC.presence_of_element_located((By.ID, 'new-game-button')))  # 페이지 로딩 기다림

    mission = None

    # 해당 웹사이트에서 쿠키 가져오기
    cookies = driver.get_cookies()

    all_cookies = driver.get_cookies()
    cookies = {cookie['name']: cookie['value'] for cookie in all_cookies}

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "X-Easy-Locale": "ko",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://sudoku.com/ko",
        "Accept": "*/*",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin"
    }

    response = requests.get("https://sudoku.com/api/level/easy", headers=headers, cookies=cookies)
    # 가져온 데이터를 출력합니다.
    if response.status_code == 200:
        data = response.json()
    else:
        print("Failed to retrieve data:", response.status_code)

    mission = data['mission']
    print(mission)

    board = sudokuSolver.string_to_board(mission)

    # 스도쿠 풀기
    sudokuSolver.solve_sudoku(board)

    # string으로 변환
    solved = sudokuSolver.board_to_string(board)
    print(solved)

    time_duration = 10
    time.sleep(time_duration)
    driver.quit()


def run_ex2(driver):
    driver.get(mc.ex2_url)
    try:
        driver.maximize_window()  # 창 크게 만들기
    except selenium.common.exceptions.WebDriverException:
        pass  # 이미 창이 최대화된 상태이므로, 이 오류를 무시합니다.

    wait = WebDriverWait(driver, 10)  # 10초 기다림
    wait.until(EC.presence_of_element_located((By.ID, 'new-game-button')))  # 페이지 로딩 기다림

    mission_value = None
    solution_value = None

    time_duration = 1
    time.sleep(time_duration)

    # 1. 원하는 데이터 추출하기
    json_data = sudokuSolver.get_easy_response_api(driver)

    # 원하는 respomse가 없을 때 새 게임 버튼 클릭
    if json_data == None:
        element = driver.find_element(By.XPATH, f'/ html / body / div[2] / div / div[1] / div[6] / div[3] / nav / div[1] / div[1]')
        element.click()

        time_duration = 1
        time.sleep(time_duration)

        element = driver.find_element(By.XPATH, f'/html/body/div[2]/div/div[1]/div[6]/div[3]/nav/div[1]/div[2]/div[2]/div/a[1]')
        element.click()

        time_duration = 1
        time.sleep(time_duration)

        json_data = sudokuSolver.get_easy_response_api(driver)

    # 스도쿠의 문제와 정답 추출
    mission_value = json_data['mission']
    solution_value = json_data['solution']

    print(mission_value)
    print(solution_value)

    canvas = driver.find_element(By.XPATH, f'/ html / body / div[2] / div / div[1] / div[6] / div[2] / div[6] / canvas')
    location = canvas.location
    size = canvas.size
    print("Canvas location : ", location, ", Canvas size : ", size)

    # 각 셀의 크기 계산
    cell_width = size['width'] / 9
    cell_height = size['height'] / 9

    # 2. 숫자 입력
    for row in range(9):
        for col in range(9):
            index = row * 9 + col

            # mission_value의 해당 위치에 0이 있으면 스도쿠 보드의 빈칸 위치를 클릭
            if mission_value[index] == '0':
                # 기존의 cell_x, cell_y 계산
                cell_x = (col * cell_width) + (cell_width / 2)  # 셀의 중앙 x 좌표
                cell_y = (row * cell_height) + (cell_height / 2)  # 셀의 중앙 y 좌표

                # 새로운 좌표 계산
                new_cell_x = (col * cell_width) - (size['width'] / 2) + (cell_width / 2)
                new_cell_y = (row * cell_height) - (size['height'] / 2) + (cell_height / 2)

                #move_to_element_with_offset의 canvas는 element의 중앙을 기준으로 x,y 좌표 offset
                action = ActionChains(driver)
                action.move_to_element_with_offset(canvas, new_cell_x, new_cell_y).click().perform()

                time_duration = 0.1
                time.sleep(time_duration)

                # solution_value의 숫자를 가져와 해당 숫자 클릭 요소 찾기
                number_to_click = solution_value[index]
                print('x : ', col, 'y : ', row, 'digit : ', number_to_click)
                element = driver.find_element(By.XPATH,f'/ html / body / div[2] / div / div[1] / div[6] / div[3] / nav / div[3] / div / div[{number_to_click}]')
                action.click(element).perform()


def run_main(driver):
    driver.get(mc.mian_url)
    try:
        driver.maximize_window()  # 창 크게 만들기
    except selenium.common.exceptions.WebDriverException:
        pass  # 이미 창이 최대화된 상태이므로, 이 오류를 무시

    wait = WebDriverWait(driver, 10)  # 10초 기다림
    wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/app/div[2]/div[2]/bk-beauty/div/div/div[2]/div[1]/div[1]/bk-select-schedule/div')))  # 페이지 로딩 기다림

    element = driver.find_element(By.XPATH, f'/html/body/app/div[2]/div[2]/bk-beauty/div/div/div[2]/div[1]/div[1]/bk-select-schedule/div/table/tbody[1]/tr[1]/td/div/a[2]')
    element.click()

    time_duration = 0.3
    time.sleep(time_duration)

    element = driver.find_element(By.XPATH, f'/html/body/app/div[2]/div[2]/bk-beauty/div/div/div[2]/div[1]/div[1]/bk-select-schedule/div/table/tbody[1]/tr[2]/td[7]/a')
    element.click()

    time_duration = 0.3
    time.sleep(time_duration)

    element = driver.find_element(By.XPATH, f'/html/body/app/div[2]/div[2]/bk-beauty/div/div/div[2]/div[1]/div[1]/div/bk-select-condition/bk-select-time/div/div[2]/div/ul/li[1]/a')
    element.click()

    time_duration = 0.3
    time.sleep(time_duration)

    action = ActionChains(driver)
    element = driver.find_element(By.XPATH, f'/html/body/app/div[2]/div[2]/bk-beauty/div/div/div[2]/div[1]/bk-select-options/div/ul[2]/li[2]/label/span')
    action.click(element).perform()

    time_duration = 0.3
    time.sleep(time_duration)

    element = driver.find_element(By.XPATH, f'/html/body/app/div[2]/div[2]/bk-beauty/div/div/div[2]/bk-submit/div/button')
    element.click()

# run_ex1(driver)
# run_wrong_ex2(driver)
run_ex2(driver)
# run_main(driver)
