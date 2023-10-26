# 이 함수는 주어진 보드의 특정 위치에 숫자를 배치할 수 있는지 여부를 확인
# 1. 해당 숫자가 이미 같은 행에 있는지.
# 2. 해당 숫자가 이미 같은 열에 있는지.
# 3. 해당 숫자가 현재 위치의 3x3 박스 내에 있는지.
import json


def is_valid(board, row, col, num):
    # Check if num is present in the specified row
    for x in range(9):
        if board[row][x] == num:
            return False

    # Check if num is present in the specified column
    for x in range(9):
        if board[x][col] == num:
            return False

    # Check if num is present in the specified 3x3 box
    startRow, startCol = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[i + startRow][j + startCol] == num:
                return False

    return True

# 이 함수는 재귀적으로 스도쿠 보드를 풉니다.
# 먼저, find_empty_location 함수를 사용하여 보드 상에서 빈 위치를 찾습니다.
# 빈 위치가 없다면 모든 칸이 채워진 것이므로 보드는 해결되었습니다.
# 빈 위치가 있다면, 해당 위치에 1부터 9까지의 숫자를 하나씩 시도해 봅니다.
# 만약 숫자가 해당 위치에 배치될 수 있다면 (is_valid 함수를 사용하여 확인), 해당 숫자를 배치하고 다음 빈 칸을 해결하기 위해 재귀적으로 solve_sudoku 함수를 호출합니다.
# 만약 이후의 칸들을 해결하는 데 실패한다면, 현재 칸의 숫자를 다시 0으로 바꾸어 초기화하고 (이것이 "백트래킹"입니다) 다른 숫자를 시도합니다.
def solve_sudoku(board):
    empty = find_empty_location(board)
    if not empty:
        return True
    row, col = empty

    for num in map(str, range(1, 10)):
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = '0'  # backtrack

    return False

# 보드에서 값이 '0'인 첫 번째 위치를 반환합니다. 만약 모든 칸이 채워져 있다면 None을 반환합니다.
def find_empty_location(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == '0':
                return i, j
    return None

# 이 두 함수는 주어진 스도쿠 문자열과 2D 리스트 형태의 보드 사이에서 변환을 수행합니다.
def string_to_board(s):
    return [list(s[i:i+9]) for i in range(0, 81, 9)]

def board_to_string(board):
    return ''.join(''.join(row) for row in board)

def get_easy_response_api(driver):
    logs = driver.get_log('performance')
    for entry in logs:
        log = json.loads(entry['message'])['message']

        if 'response' in log['params']:
            if log['method'] == 'Network.responseReceived' and log['params']['response'][
                'url'] == 'https://sudoku.com/api/level/easy':
                request_id = log['params']['requestId']
                # Network.getResponseBody를 사용하여 응답 본문 가져오기
                response_body = driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})

                # 응답 본문 변환
                json_data = json.loads(response_body['body'])

                return json_data