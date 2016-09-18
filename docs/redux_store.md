# Redux Store Design

```
{
	user: {
		...general user info	
	},
	courses: {
		course_key: {
			...general course info,
			lectures: [...lecture_compound_keys]
		},
		...
	},
	lectures: {
		lecture_compound_key: {
			...general lecture info
		},
		...
	},
	media: {
		lecture_compound_key: {
			computer: {
				index: [...timestamps],
				...
			},
			whiteboard: {
				index: [...timestamps],
				...
			}
		},
		...
	},
	lecture_current: {
		lecture_compound_key,
		indices: {
			computer: {
				index: pointer,
				...
			},
			whiteboard: {
				index: pointer,
				...
			}
		}
	}
}
```