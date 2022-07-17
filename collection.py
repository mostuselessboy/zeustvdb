def collection_maker():
	collection_id = [1241,556, 10, 131292, 131296, 131295,264, 435259,645,748,151,87359,9485,295,328]
	collection = []
	for item in  collection_id:
		url = f'https://api.themoviedb.org/3/collection/{item}?api_key={12345}'
		b = (requests.get(url)).json()
		collection.append({'id':b['id'],
		'title':b['name'],
		'bio':b['overview'],
		'img':"https://image.tmdb.org/t/p/w300/"+ b['backdrop_path']})
	print(collection)
col_list = [{'id': '1241', 'title': 'Harry Potter Collection', 'bio': 'The Harry Potter films are a fantasy series based on the series of seven Harry Potter novels by British writer J. K. Rowling.', 'img': 'https://image.tmdb.org/t/p/w300//wfnMt6LGqYHcNyOfsuusw5lX3bL.jpg'}, {'id': '556', 'title': 'Spider-Man Collection', 'bio': 'A superhero film series based on the Marvel Comics character Spider-Man. The series is centered on Peter Parker, an academically gifted but socially inept freelance photographer who gets bitten by a genetically modified spider and gains spider-like abilities, all of which he uses to fight crime as a spider-masked vigilante, learning for himself that with great power comes great responsibility.', 'img': 'https://image.tmdb.org/t/p/w300//waZqriYTuBE3WqXI3SDGi3kfDQE.jpg'}, {'id': '10', 'title': 'Star Wars Collection', 'bio': 'An epic space-opera theatrical film series, which depicts the adventures of various characters "a long time ago in a galaxy far, far away…."', 'img': 'https://image.tmdb.org/t/p/w300//d8duYyyC9J5T825Hg7grmaabfxQ.jpg'}, {'id': '131292', 'title': 'Iron Man Collection', 'bio': 'A superhero film series based on the Marvel Comics character of the same name and part of the Marvel Cinematic Universe (MCU) series. Tony Stark AKA Iron Man, an industrialist and master engineer uses a powered exoskeleton to fight foes, with the aid of his personal assistant and love interest Pepper Potts.', 'img': 'https://image.tmdb.org/t/p/w300//rI8zOWkRQJdlAyQ6WJOSlYK6JxZ.jpg'}, {'id': '131296', 'title': 'Thor Collection', 'bio': 'A superhero film series based on the comic book character of the same name published by Marvel Comics, and part of the Marvel Cinematic Universe (MCU) film series. The series centers on Thor, the crown prince of Asgard.', 'img': 'https://image.tmdb.org/t/p/w300//3KL8UNKFWgIKXzLHjwY0uwgjzYl.jpg'}, {'id': '131295', 'title': 'Captain America Collection', 'bio': 'A superhero film series based on the Marvel Comics character Captain America, and part of the Marvel Cinematic Universe (MCU) series. The series is centered on Steve Rogers, a man from World War II era Brooklyn who is transformed into super-soldier Captain America.', 'img': 'https://image.tmdb.org/t/p/w300//ezEpSQhUQxVKdMx81zaSLsTHv7j.jpg'}, {'id': '264', 'title': 'Back to the Future Collection', 'bio': 'An American science fiction–comedy film series that follows the adventures of a high school student, Marty McFly and an eccentric scientist, Dr Emmett L. Brown as they use a DeLorean time machine to time travel to different periods in the history of Hill Valley, California.', 'img': 'https://image.tmdb.org/t/p/w300//AqQotqj7XOI6GjB28nhMMa8YzOT.jpg'}, {'id': '435259', 'title': 'Fantastic Beasts Collection', 'bio': 'The Fantastic Beasts films are a fantasy series based on and inspired by the textbook mentioned in the Harry Potter novels by British writer J. K. Rowling. Set in the same Wizarding World franchise, they follow the adventures of Newt Scamander, a self-proclaimed magizoologist, along with Porpentina "Tina" Goldstein, a MACUSA auror.', 'img': 'https://image.tmdb.org/t/p/w300//2Iripuf9j5vbROHNpkUUiWIIDxE.jpg'}, {'id': '645', 'title': 'James Bond Collection', 'bio': 'The James Bond film series is a British series of spy films based on the fictional character of MI6 agent James Bond, codename "007". With all of the action, adventure, gadgetry & film scores that Bond is famous for.  (We do not consider the 1954 release of Casino Royale for this series because it was actually a television episode and not a theatrical film.)', 'img': 'https://image.tmdb.org/t/p/w300//dOSECZImeyZldoq0ObieBE0lwie.jpg'}, {'id': '748', 'title': 'X-Men Collection', 'bio': 'A superhero film series about a team of mutant superheroes based on the Marvel Comics superheroes of the same name.', 'img': 'https://image.tmdb.org/t/p/w300//roZFGw3Rg6VOYty9y4r5WvgvXoC.jpg'}, {'id': '151', 'title': 'Star Trek: The Original Series Collection', 'bio': "Star Trek: Original Motion Picture Collection contains the first six Original Series films starring the U.S.S. Enterprise's cast and crew from the 1960s TV series of the same name.", 'img': 'https://image.tmdb.org/t/p/w300//9BQj9hq0aK6yM9Tm2NJ28jg572y.jpg'}, {'id': '87359', 'title': 'Mission: Impossible Collection', 'bio': 'Mission: Impossible is a series of a secret agent thriller films based on the popular television series. They chronicle the missions of a team of secret government agents known as the Impossible Missions Force (IMF) under the leadership of Hunt.', 'img': 'https://image.tmdb.org/t/p/w300//jYl0UuJFcmhymv9ZNO14lPLDY1Z.jpg'}, {'id': '9485', 'title': 'The Fast and the Furious Collection', 'bio': 'An action film series centered on illegal street racing and heists.', 'img': 'https://image.tmdb.org/t/p/w300//gC9BUFiROWtaMsluGYziZ6lR4OJ.jpg'}, {'id': '295', 'title': 'Pirates of the Caribbean Collection', 'bio': "A series of fantasy swashbuckler films based on Walt Disney's theme park ride of the same name. The films follow the adventures of Captain Jack Sparrow and take place in a fictional historical setting; a world ruled by the British Empire, the East India Trading Company and the Spanish Empire, with pirates representing freedom from the ruling powers.", 'img': 'https://image.tmdb.org/t/p/w300//wxgD3fB5lQ2sGJLog0rvXW049Pf.jpg'}, {'id': '328', 'title': 'Jurassic Park Collection', 'bio': 'An American science fiction adventure film series based on the novel of the same name by Michael Crichton. The films center on the fictional Isla Nublar near Costa Rica in the Central American Pacific Coast, where a billionaire philanthropist and a small team of genetic scientists have created an amusement park of cloned dinosaurs.', 'img': 'https://image.tmdb.org/t/p/w300//njFixYzIxX8jsn6KMSEtAzi4avi.jpg'}]
