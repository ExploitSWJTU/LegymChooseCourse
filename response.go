package main

type LoginResponse struct {
	Code    int               `json:"code"`
	Message interface{}       `json:"message"`
	Data    LoginResponseData `json:"data"`
}

type LoginResponseData struct {
	Id                     string        `json:"id"`
	UuasId                 interface{}   `json:"uuasId"`
	OrganizationVerified   int           `json:"organizationVerified"`
	Identity               string        `json:"identity"`
	OrganizationId         string        `json:"organizationId"`
	OrganizationName       string        `json:"organizationName"`
	SchoolId               string        `json:"schoolId"`
	SchoolName             string        `json:"schoolName"`
	OrganizationUserNumber string        `json:"organizationUserNumber"`
	NickName               string        `json:"nickName"`
	RealName               string        `json:"realName"`
	Avatar                 interface{}   `json:"avatar"`
	Gender                 int           `json:"gender"`
	BirthDay               int           `json:"birthDay"`
	Height                 int           `json:"height"`
	Weight                 int           `json:"weight"`
	FaceId                 interface{}   `json:"faceId"`
	CampusId               string        `json:"campusId"`
	Year                   int           `json:"year"`
	AccountNumber          string        `json:"accountNumber"`
	Mobile                 string        `json:"mobile"`
	Authorities            []interface{} `json:"authorities"`
	AccessToken            string        `json:"accessToken"`
	TokenType              string        `json:"tokenType"`
	RefreshToken           string        `json:"refreshToken"`
	UserId                 interface{}   `json:"userId"`
	SemesterId             interface{}   `json:"semesterId"`
	CampusName             interface{}   `json:"campusName"`
	AccessTokenExpires     int           `json:"accessTokenExpires"`
	FaceImage              interface{}   `json:"faceImage"`
	FaceStatus             int           `json:"faceStatus"`
}

type GetCurrentSemesterResponse struct {
	Code    int                            `json:"code"`
	Message interface{}                    `json:"message"`
	Data    GetCurrentSemesterResponseData `json:"data"`
}

type GetCurrentSemesterResponseData struct {
	OrganizationId string      `json:"organizationId"`
	StartDate      int         `json:"startDate"`
	EndDate        int         `json:"endDate"`
	YearRange      string      `json:"yearRange"`
	Current        interface{} `json:"current"`
	Index          int         `json:"index"`
	WeekIndex      int         `json:"weekIndex"`
	UpdateStatus   interface{} `json:"updateStatus"`
	Id             string      `json:"id"`
}

type GetCourseListResponse struct {
	Code    int      `json:"code"`
	Message string   `json:"message"`
	Data    []Course `json:"data"`
}

type Course struct {
	CourseStatus           int    `json:"courseStatus"`
	Id                     string `json:"id"`
	CourseName             string `json:"courseName"`
	Type                   int    `json:"type"`
	ProjectId              string `json:"projectId"`
	ProjectName            string `json:"projectName"`
	Year                   int    `json:"year"`
	TeacherId              string `json:"teacherId"`
	TeacherName            string `json:"teacherName"`
	WeekLabel              string `json:"weekLabel"`
	WeekRange              string `json:"weekRange"`
	WeekLabelType          int    `json:"weekLabelType"`
	StartTimeStr           string `json:"startTimeStr"`
	Address                string `json:"address"`
	StartDateStr           string `json:"startDateStr"`
	EndDateStr             string `json:"endDateStr"`
	CampusId               string `json:"campusId"`
	CampusName             string `json:"campusName"`
	LimitPeopleNumberStr   string `json:"limitPeopleNumberStr"`
	StartTime              int    `json:"startTime"`
	EndTime                int    `json:"endTime"`
	CreateDateTime         int    `json:"createDateTime"`
	StartDate              int    `json:"startDate"`
	EndDate                int    `json:"endDate"`
	RegisterStartTime      int    `json:"registerStartTime"`
	RegisterEndTime        int    `json:"registerEndTime"`
	LimitPeopleNumber      int    `json:"limitPeopleNumber"`
	RegisteredPeopleNumber int    `json:"registeredPeopleNumber"`
}

type SignUpResponse struct {
	Code    int                `json:"code"`
	Message interface{}        `json:"message"`
	Data    SignUpResponseData `json:"data"`
}

type SignUpResponseData struct {
	IsSuccess bool   `json:"isSuccess"`
	State     int    `json:"state"`
	Reason    string `json:"reason"`
}
