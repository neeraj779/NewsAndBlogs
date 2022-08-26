# News and Blogs Website

---

“News and Blogs” web application in Python using Django web development framework. Logged-in users can view News clips cards (and click on a particular news article to view the details in a separate page). Additionally, the users can create, delete blogs from their dashboard. The site administrator can perform CRUD operations on blogs using API calls only.

Material: For fetching news articles, made usage of the following news API: https://newsapi.org/

---- 

Web app development

Authentication 
a) User login, logout

b) User registration 

c) Standard password validation 

d) Forgot password validation

---

API calls, JSON handling, Dashboard 
a) Fetch and display News image, title in home page (after logging-in) 

b) Redirect user to detailed user article on clicking news clip image 

c) User creates blog-blog title, content, date created(automatic) 

d) User delete his/her own blogs from dashboard

e) User gets email regarding blog updates

---

Serializers - Django REST Framework 

a) Site-administrator can view existing blogs list in json format through api endpoint only 

b) Site-admin can delete, update, create blogs through api endpoints only

---

Deployment Heroku - https://news-and-blogs.herokuapp.com