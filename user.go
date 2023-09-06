package main

import (
	"log"

	"github.com/go-resty/resty/v2"
)

var BaseUrl = "https://cpes.legym.cn"

type User struct {
	Client     *resty.Client
	UserName   string
	Password   string
	Id         string
	SchoolId   string
	SemesterId string
	Year       int
}

func (user *User) Login() {
	user.Client = resty.New()
	var resp LoginResponse
	BruteRequest(
		user.Client.
			R().
			SetBody(map[string]any{
				"entrance": 1,
				"userName": user.UserName,
				"password": user.Password,
			}).
			SetResult(&resp).
			Post,
		BaseUrl+"/authorization/user/manage/login",
	)

	log.Println(resp)
	user.Client.SetAuthToken(resp.Data.AccessToken)
	user.Client.SetHeader("Organization", resp.Data.SchoolId)
	user.Id = resp.Data.Id
	user.SchoolId = resp.Data.SchoolId
	user.Year = resp.Data.Year
	user.SemesterId = user.GetCurrentSemesterId()
}

func (user *User) GetCurrentSemesterId() string {
	var resp GetCurrentSemesterResponse
	BruteRequest(
		user.Client.
			R().
			SetResult(&resp).
			Get,
		BaseUrl+"/education/semester/getCurrent",
	)
	return resp.Data.Id
}

func (user *User) GetCourseList() []Course {
	var resp GetCourseListResponse
	BruteRequest(
		user.Client.
			R().
			SetBody(map[string]any{
				"semesterId": user.SemesterId,
				"userId":     user.Id,
				"year":       user.Year,
			}).
			SetResult(&resp).
			Post,
		BaseUrl+"/education/optional/course/newList",
	)
	return resp.Data
}

func (user *User) SignUp(courseId string) SignUpResponse {
	var resp SignUpResponse
	BruteRequest(
		user.Client.
			R().
			SetFormData(map[string]string{
				"courseId": courseId,
				"schoolId": user.SchoolId,
			}).
			SetResult(&resp).
			Post,
		BaseUrl+"/education/course/app/signUp",
	)
	return resp
}
