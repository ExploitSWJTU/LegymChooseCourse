import asyncio
import aiohttp
import requests


#####################################################
username = '' # 用户名（手机号）
password = '' # 密码
#####################################################

CORO_CNT = 4

base_url = 'https://cpes.legym.cn'

api = {
    'login': base_url+'/authorization/user/manage/login',
    'semester': base_url+'/education/semester/getCurrent',
    'courses': base_url+'/education/optional/course/newList',
    'signup': base_url+'/education/course/app/signUp',
    'chosenCourse': base_url+'/education/optional/course/optionalPageList',
}

def request(method, url, **kwargs):
    while True:
        try:
            r = requests.request(method, url, **kwargs)
        except requests.RequestException:
            pass
        if r.status_code < 500:
            return r.json()

def get(url, **kwargs):
    return request('GET', url, **kwargs)

def post(url, **kwargs):
    return request('POST', url, **kwargs)

async def async_request(method, url, **kwargs):
    while True:
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, **kwargs) as r:
                if r.status < 500:
                    return await r.json()

async def async_post(url, **kwargs):
    return await async_request('POST', url, **kwargs)


class LegymUser():
    loop = None
    year = -1
    access_token = ''
    school_id = ''
    user_id = ''
    semester_id = ''
    headers = {}

    def __init__(self, username, password):
        self.loop = asyncio.get_event_loop()
        self.username = username
        self.password = password

    def login(self):
        json = {
            'entrance': '1',
            'password': self.password,
            'userName': self.username,
        }
        r = post(api['login'], json=json)
        print(r)
        self.access_token = r['data']['accessToken']
        self.school_id = r['data']['schoolId']
        self.headers = {
            'Organization': self.school_id,
            'Authorization': 'Bearer '+self.access_token
        }
        self.year = r['data']['year']
        self.user_id = r['data']['id']
        self.semester_id = self.get_current_semester()

    def get_current_semester(self):
        r = get(api['semester'], headers=self.headers)
        return r['data']['id']

    def get_courses(self):
        json = {
            'semesterId': self.semester_id,
            'userId': self.user_id,
            'year': self.year
        }
        r = post(api['courses'], json=json, headers=self.headers)
        return r['data']

    def choose_course(self, course_id):
        tasks = [self.loop.create_task(self.choose_course_coro(course_id)) for _ in range(CORO_CNT)]
        self.loop.run_until_complete(asyncio.wait(tasks))

    async def choose_course_coro(self, course_id):
        data = {
            'courseId': course_id,
            'schoolId': self.school_id,
        }
        while True:
            r = await async_post(api['signup'], data=data, headers=self.headers)
            print(r)


if __name__ == '__main__':
    user = LegymUser(username, password)
    user.login()
    courses = user.get_courses()
    for i, course in enumerate(courses):
        print('{}. {} {} {} {}'.format(
            i,
            course['id'],
            course['courseStatus'],
            course['courseName'],
            course['teacherName'],
        ))
    user.choose_course(courses[int(input('请输入要选择的课程序号：'))]['id'])
