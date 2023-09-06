package main

import (
	"fmt"
	"log"
)

const coroCnt = 2

var (
	userName = ""
	password = ""
)

func main() {
	user := &User{
		UserName: userName,
		Password: password,
	}
	user.Login()
	courses := user.GetCourseList()
	for i, course := range courses {
		fmt.Println(i, course.Id, course.CourseName, course.TeacherName)
	}
	var index int
	fmt.Print("Please input the course index: ")
	fmt.Scanln(&index)
	var c = make(chan SignUpResponse, coroCnt*2)
	for i := 0; i < coroCnt; i++ {
		go func() {
			for {
				c <- user.SignUp(courses[index].Id)
			}
		}()
	}
	for {
		resp := <-c
		log.Println(resp)
		if resp.Data.IsSuccess {
			break
		}
	}
}
