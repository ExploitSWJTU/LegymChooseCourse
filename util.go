package main

import (
	"log"

	"github.com/go-resty/resty/v2"
)

func BruteRequest(request func(string) (*resty.Response, error), url string) {
	for {
		resp, err := request(url)
		if err != nil {
			log.Println(err.Error())
			continue
		}
		if resp.StatusCode() < 500 {
			return
		}
	}
}
