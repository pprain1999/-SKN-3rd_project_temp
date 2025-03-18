from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import csv

code_datas = []

# 1. chrome 실행
driver = webdriver.Chrome()

# 2. 특정 URL 접근
driver.get("https://www.acmicpc.net/login?next=%2Fregister")  # 로그인 부터

# 여러분들의 아이디/ 비밀번호 정보를 넣으세요.
personal_id = "qkrdbwlsdl01"
personal_pw = "qkr01!01@01#01"

off_set = 30
count = 0  # count 변수를 초기화

# 3. 아이디/이메일 입력 필드 찾기
id_input_field = driver.find_element(By.NAME, "login_user_id")
password_input_field = driver.find_element(By.NAME, "login_password")

id_input_field.send_keys(personal_id)
time.sleep(0.5)
password_input_field.send_keys(personal_pw)
time.sleep(0.5)

# 로그인 
submit_button = driver.find_element(By.CSS_SELECTOR, "#submit_button")
submit_button.click()
time.sleep(off_set)

# 개인 성공문제로 들어가기 
top_right_bar = driver.find_elements(By.CSS_SELECTOR, "ul.loginbar.pull-right li")
top_right_bar[0].find_element(By.CSS_SELECTOR, "a").click()

time.sleep(1) 

# 3. 문제 리스트 접근
problem_list = driver.find_element(By.CSS_SELECTOR, "div.problem-list").find_elements(By.CSS_SELECTOR, 'a')

# 문제 리스트를 순회하면서 각 문제 페이지를 새 창에서 열기
for problem in problem_list:
    url = problem.get_attribute("href")  # 문제의 URL을 미리 저장
    
    # 새 창을 열어서 문제 페이지로 이동
    driver.execute_script("window.open(arguments[0], '_blank');", url)
    time.sleep(1)  # 새 창이 열리도록 대기
        
    # 현재 열린 모든 창을 가져옵니다.
    all_windows = driver.window_handles
        
    # 새 창이 열렸는지 확인하고 새 창으로 전환
    if len(all_windows) > 1:
        new_window = all_windows[-1]  # 새 창의 핸들
        driver.switch_to.window(new_window)  # 새 창으로 전환

        # 문제 페이지로 들어옴
        top_button = driver.find_element(By.CSS_SELECTOR, 'ul.nav.nav-pills.no-print.problem-menu')
        problem_id = top_button.find_elements(By.CSS_SELECTOR, 'li')[0].text
        code_button = top_button.find_elements(By.CSS_SELECTOR, 'li')[5]

        problem_title = driver.find_element(By.CSS_SELECTOR, '#problem_title').text

        problem_info = driver.find_element(By.CSS_SELECTOR, '#problem-info')
        problem_solved = problem_info.find_elements(By.CSS_SELECTOR, 'td')[-1].text

        # 스크롤을 조금씩 내리며 #problem_tags를 찾기
        problem_tags = None
        max_scrolls = off_set  # 최대 스크롤 횟수
        for _ in range(max_scrolls):
            try:
                # #problem_tags 요소가 로딩될 때까지 기다립니다.
                problem_tags = WebDriverWait(driver, 2).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#problem_tags li'))
                )
                break  # 요소를 찾으면 루프를 종료
            except:
                # 요소를 못 찾으면 스크롤을 조금 내린다.
                driver.execute_script("window.scrollBy(0, 300);")  # 조금씩 내린다.
                time.sleep(1)  # 스크롤 후 대기

        if problem_tags:
            category = [tag.text for tag in problem_tags]
            # print('카테고리: ', ', '.join(category))
        else:
            print("카테고리 정보 로드 실패")

        # 문제 설명 부분에서 p 태그들을 모두 찾고 첫 번째 p 태그의 텍스트를 가져옵니다.
        paragraphs = driver.find_elements(By.XPATH, '//*[@id="problem_description"]/p')
            
        problem_description = ''

        for problem_script in paragraphs:
            problem_description += problem_script.text

        # <ul>이 존재할 경우에만 처리
        ul_elements = driver.find_elements(By.XPATH, '//*[@id="problem_description"]/ul')

        if ul_elements:  # <ul>이 존재한다면
            details = ul_elements[0].find_elements(By.CSS_SELECTOR, 'li')
                
            for detail in details:
                problem_description += detail.text  # <li> 태그의 텍스트 추가

        print('problem_description:', problem_description)

        time.sleep(1)

        code_button.click()

        language_button = driver.find_element(By.NAME, "language_id")

        # 4. 드롭다운 요소를 Select 객체로 감쌈
        select = Select(language_button)

        # 5. Python을 선택
        select.select_by_visible_text("Python") 

        submit_button = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary.btn-sm.margin-left-3.form-control")
        submit_button.click()

        time.sleep(1)

        # while 문 돌면서 내가 원하는 만큼 다음 버튼 클릭하면서 값 저장하기
        while True:  # 
            problem_table = driver.find_element(By.CSS_SELECTOR, "div.table-responsive").find_element(By.TAG_NAME, "tbody").find_elements(By.CSS_SELECTOR, "tr")
            
            for table_info in problem_table:
                info = table_info.find_elements(By.CSS_SELECTOR, "td")
                if len(info) > 1:
                    # user_id는 두 번째 td 안의 <a> 태그에서 가져옵니다.
                    submit_id = info[0].text
                    user_id = info[1].find_element(By.CSS_SELECTOR, "a").text
                    # 기존 코드에서 result를 추출하는 부분 수정
                    result = info[3].find_element(By.CSS_SELECTOR, 'td.result > span').text
                    memory = info[4].text
                    time_s = info[5].text
                    links = info[6].find_elements(By.CSS_SELECTOR, 'a')

                    time.sleep(1)

                    # 'a' 태그가 존재하는지 확인
                    if links:
                        #'a' 태그가 존재하는 경우
                        language = links[0].text
                        url_p = links[0].get_attribute('href')

                        # 새창을 열 수 있는 경우
                        driver.execute_script("window.open(arguments[0], '_blank');", url_p)

                        time.sleep(1)  # 새 창이 열리도록 대기

                        # 현재 열린 모든 창을 가져옵니다.
                        all_windows = driver.window_handles

                        # 새 창이 열렸는지 확인하고 새 창으로 전환
                        if len(all_windows) > 1:
                            new_window = all_windows[-1]  # 새 창의 핸들
                            driver.switch_to.window(new_window) 

                            # 문제 들고 오기
                            codes = [] # 리스트가 더 좋을 듯

                            code_lines = driver.find_elements(By.CSS_SELECTOR, "pre.CodeMirror-line")

                            for code_line in code_lines:
                                elements = code_line.find_elements(By.CSS_SELECTOR, "span") 
                                line = elements[0].text

                                codes.append(line)
                            time.sleep(1)
                            # 문제 들고 와서 값 저장하기 -> 나중엔 파일에 저장
                            code_datas.append(
                                {
                                    "problem_id" : problem_id,         # 문제 번호
                                    "problem_title" : problem_title,   # 문제 제목 
                                    "problem_solved" : problem_solved, # 문제 정답 비율 
                                    "category" : category,             # 문제 카테고리 
                                    "submit_id" : submit_id,
                                    "user_id" : user_id,               # 유저 아이디 
                                    "result" : result,                 # 정오답 결과 
                                    "memory" : memory,                 # 메모리 
                                    "time" : time_s,                   # 시간 
                                    "language" : language,             # 언어 
                                    "code" : codes,                    # 코드 
                                }                                      
                            )

                            print(code_datas[-1])

                        driver.close()

                        driver.switch_to.window(driver.window_handles[-1])
                else:
                    language = info[6].text
                    url_p = ''

                # print(user_id, result, memory, time_s, language, url_p)

                time.sleep(1)   

            # 다음 버튼 반복, while 문 빠져 나갈 수 있는 구문 작성 
            if count < 10:
                # print("count: ", count)
                next_button = driver.find_element(By.ID, "next_page")
                next_button.click()
                count += 1  # count 값을 증가시킴
            else:
                # print("한 문제 끝")
                driver.close()  # 새 창 닫기
                break
        
        # 문제 페이지에서 작업을 마친 후 새 창 닫기
            
        # 원래 창으로 돌아가기
        driver.switch_to.window(driver.window_handles[0])  # 원래 창으로 전환
    else:
        print("새 창이 열리지 않았습니다.")
        
    time.sleep(1)

# 4. 브라우저 종료
driver.quit()

# 'code_datas'를 CSV 파일로 저장
with open("code_data.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["problem_id", "problem_title", "problem_solved", "category", 
                                          "submit_id", "user_id", "result", "memory", "time", "language", "code"])
    
    # CSV 파일에 헤더 작성
    writer.writeheader()
    
    # code_datas에 있는 데이터들을 각 행으로 작성
    for code in code_datas:
        writer.writerow({
            "problem_id": code["problem_id"],
            "problem_title": code["problem_title"],
            "problem_solved": code["problem_solved"],
            "category": ', '.join(code["category"]),  # 카테고리는 리스트로 되어 있으므로 문자열로 변환
            "submit_id": code["submit_id"],
            "user_id": code["user_id"],
            "result": code["result"],
            "memory": code["memory"],
            "time": code["time"],
            "language": code["language"],
            "code": '\n'.join(code["code"])  # 코드 라인은 줄바꿈을 기준으로 합쳐서 저장
        })
