import requests
import json
import threading


class chooseClassThread:
    def __init__(self, school_id, access_token, semester_id, course_id):
        self.school_id = school_id
        self.access_token = access_token
        self.semester_id = semester_id
        self.course_id = course_id
        self.thread = threading.Thread(target=self.choose_class)
        self.thread.start()

    def choose_class(self):
        choose_course(self.school_id, self.access_token, self.course_id)


api = {
    "login": "https://cpes.legym.cn/authorization/user/manage/login",
    "semester": "https://cpes.legym.cn/education/semester/getCurrent",
    "courses": "https://cpes.legym.cn/education/optional/course/newList",
    "signup": "https://cpes.legym.cn/education/course/app/signUp",
    "chosenCourse": "https://cpes.legym.cn/education/optional/course/optionalPageList",
    "changeCourse": "https://cpes.legym.cn/course/app/change",
}

def login(username, password):
    headers = {
        "Content-Type": "application/json",
    }
    data = {
        "entrance":"1",
        "password":"{}".format(password),
        "userName":"{}".format(username),
    }
    data = json.dumps(data)
    r = requests.post(api["login"], data=data, headers=headers)
    print(r.status_code)
    return r.json()


def get_current_semester(school_id, access_token):
    headers = {
        "Content-Type": "application/json",
        "Organization": "{}".format(school_id),
        "Authorization": "Bearer {}".format(access_token),
    }
    st_code = 500
    while st_code != 200:
        try:
            req = requests.get(api["semester"], headers=headers, timeout=2)
            st_code = req.status_code
            if st_code == 200:
                return req.json()
        except Exception as e:
            print(e)
            pass

def get_courses(school_id, access_token, semester_id, user_id, year):
    headers = {
        "Content-Type": "application/json",
        "Organization": "{}".format(school_id),
        "Authorization": "Bearer {}".format(access_token),
    }
    data = {
        "semesterId":semester_id,
        "userId": user_id,
        "year": year
        }
    data = json.dumps(data)
    req = requests.post(api["courses"], data=data, headers=headers)
    print(req.text)
    return req.json()

def choose_course(school_id, access_token, course_id):
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Organization": "{}".format(school_id),
        "Authorization": "Bearer {}".format(access_token),
        "Date": "Tue, 01 Sept 2022 00:00:00 GMT",
    }
    data = {
        "courseId": "{}".format(course_id),
        "schoolId": "{}".format(school_id),
    }
    # data = json.dumps(data)
    while True:
        try:
            req = requests.post(api["signup"], data=data, headers=headers, timeout=10)
            print(req.text)
            if "成功" in req.text:
                print("成功")
                exit()
        except Exception as e:
            print(e)
            pass
    return True

def change_course(school_id, access_token, old_course_id, new_course_id):
    header = {
        "Content-Type": "application/json",
        "Organization": "{}".format(school_id),
        "Authorization": "Bearer {}".format(access_token),
        
    }
    data = {
        "newCourse": "{}".format(new_course_id),
        "oldCourse": "{}".format(old_course_id),
    }

    data = json.dumps(data)
    req = requests.post(api["changeCourse"], data=data, headers=header)
    print(req.status_code)
    return req.json()


def get_current_chosen_course(semester_id, user_id, school_id, access_token):
    headers = {
        "Content-Type": "application/json",
        "Organization": "{}".format(school_id),
        "Authorization": "Bearer {}".format(access_token),
    }
    data = {
        "semesterId": "{}".format(semester_id),
        "userId": "{}".format(user_id),
    }
    data = json.dumps(data)
    req = requests.post(api["chosenCourse"], data=data, headers=headers)
    print(req.status_code)
    return req.json()


if __name__ == "__main__":
    # username = input("username: ")
    # password = input("password: ")

    #####################################################
    username = "" # 用户名
    password = "" # 密码
    year = 2022 # 入学年份
    #####################################################


    j = login(username, password)
    print(j)
    access_token = j['data']["accessToken"]
    school_id = j['data']["schoolId"]
    user_id = j['data']['id']
    current_semester_id = get_current_semester(school_id, access_token)['data']['id']
    print(current_semester_id)

    # get current chosen course
    flag = 0
    try:
        current_chosen_course = get_current_chosen_course(current_semester_id, user_id, school_id, access_token)['data']['courseMap']['{}'.format(year)]['courseList'][0]
        current_id = current_chosen_course['id']
        print("你已经选了课程：{}, id: {}".format(current_chosen_course['courseName'], current_id))
        flag = 1
    except Exception as e:
        print(e)
        pass



    courses = get_courses(school_id, access_token, current_semester_id, user_id, year)['data']
    print(courses)
    for idx in range(len(courses)):
        print("{}. id:{} name:{} teacher: {} status: {}".format(idx, courses[idx]['id'], 
        courses[idx]['courseName'], courses[idx]['teacherName'],
        courses[idx]['courseStatus']))

    # exit()
    course_idx = input("请输入要选择的课程index: ")
    # course_idx = 28
    course_id = courses[int(course_idx)]['id']

    print("你將要选择课程id:{} {}".format(course_id, courses[int(course_idx)]['courseName']))

    if flag == 1:
        print("你已经选了课程，是否要更改课程？y/n")
        choice = input()
        if choice == "y":
            for i in range(10):
                res = change_course(school_id, access_token, current_id, course_id)
                print(res)
            exit()
        else:
            print("不更改课程")


    # 10线程同时选课
    print(school_id, access_token, current_semester_id, course_id)
    for i in range(3):
        for j in courses:
            chooseClassThread(school_id, access_token, current_semester_id, j['id'])
