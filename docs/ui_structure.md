# UI Structure

### Root
```
root
-> header
-> content
```

### Courses
```
content
-> CourseList
	-> Course
		-> LectureList
			-> LectureListItem<small>
				-> LectureThumb
				-> LectureItemInfo
			...
	...
```

### Course
```
content
-> LectureList
	-> LectureListItem<large>
		-> LectureThumb
		-> LectureItemInfo
	...
```

### Lecture
```
content
-> BreadCrumbs
-> LectureInfo
-> MediaWrapper
	-> MediaCollection
		-> MediaComponent<Video|Image>
		...
	-> MediaThumbCollection
		-> MediaThumb
	-> MediaController
```