import re

COMMANDS = ['exit', 'add students']

pts = {'Python': 600, 'DSA': 400, 'Databases': 480, 'Flask': 550}

NOTIFICATION = '''To: {email}
Re: Your Learning Progress
Hello, {name}! You have accomplished our {course} course!'''


class Student:
    def __init__(self, s):
        s = re.search(r'(([a-zA-Z\'\- ]+ ){2,})([a-zA-Z\.0-9]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+)', s)
        self.initials = s.group(1)
        self.email = s.group(len(s.groups()))
        self.full = s
        self.id = str(abs(hash(self.email)))
        self.progress = {'Python': 0, 'DSA': 0, 'Databases': 0, 'Flask': 0}
        self.tasks = {'Python': 0, 'DSA': 0, 'Databases': 0, 'Flask': 0}
        self.completed = {'Python': False, 'DSA': False, 'Databases': False, 'Flask': False}

    def __str__(self):
        return f'{self.id} points: Python={self.progress["Python"]}; ' \
               f'DSA={self.progress["DSA"]}; ' \
               f'Databases={self.progress["Databases"]}; ' \
               f'Flask={self.progress["Flask"]}'

    def add_points(self, lst):
        self.progress['Python'] += int(lst[0])
        self.tasks['Python'] += 1 if lst[0] != '0' else 0
        self.progress['DSA'] += int(lst[1])
        self.tasks['DSA'] += 1 if lst[1] != '0' else 0
        self.progress['Databases'] += int(lst[2])
        self.tasks['Databases'] += 1 if lst[2] != '0' else 0
        self.progress['Flask'] += int(lst[3])
        self.tasks['Flask'] += 1 if lst[3] != '0' else 0


def check_credentials(s, arr):
    parts = s.split(' ')
    if 3 > len(parts):
        return 'Incorrect credentials.', False
    if not re.match(r'^[a-zA-Z\'\-]{2,}$', parts[0]) or parts[0][0] in ['\'', '-'] or parts[0][-1] in ['\'', '-'] \
            or any(x in parts[0] for x in ['\'-', '-\'', '\'\'', '--', ]):
        return 'Incorrect first name.', False
    surname = ''.join(parts[1:-1])
    if not re.match(r'^[a-zA-Z\'\-]{2,}$', surname) or surname[0] in ['\'', '-'] or surname[-1] in ['\'', '-'] \
            or any(x in surname for x in ['\'-', '-\'', '\'\'', '--', ]):
        return 'Incorrect last name.', False
    if not re.match(r'^[a-zA-Z\.0-9]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+$', parts[-1]):
        return 'Incorrect email.', False
    if len(list(filter(lambda x: x.email == parts[-1], arr))) > 0:
        return 'This email is already taken.', False
    return "The student has been added.", True


def check_points(s, arr):
    parts = s.split(' ')
    if len(parts) != 5 or any(not x.isnumeric() for x in parts[1:]):
        return 'Incorrect points format.', None
    try:
        st = list(filter(lambda x: x.id == parts[0], arr))[0]
        return 'Points updated.', st.id
    except:
        return f'No student is found for id={parts[0]}.', None


def stats_by_course(arr, c):
    arr2 = sorted(sorted(arr, key=lambda student: student.id), key=lambda student: student.progress[c], reverse=True)
    return ''.join(list(
        map(lambda
                x: f'{x.id}\t{x.progress[c]}\t{round(x.progress[c] / pts[c] * 1000) / 10}%\n' if x.progress != 0 else '',
            arr2)))


print("Learning Progress Tracker")
students = []
while True:
    cmd = input()
    if len(cmd) == 0 or cmd.isspace():
        print('No input.')
        continue
    match cmd:
        case 'exit':
            print('Bye!')
            break
        case 'add students':
            print("Enter student credentials or 'back' to return:")
            inp = input()
            prev = len(students)
            while inp != 'back':
                feedback, success = check_credentials(inp, students)
                print(feedback)
                if success:
                    students.append(Student(inp))
                try:
                    inp = input()
                except UnicodeEncodeError:
                    # Workaround :(
                    print('Incorrect first name.')
                    print('Incorrect last name.')
                    inp = input()
            print(f'Total {len(students) - prev} students have been added.')
        case 'back':
            print("Enter 'exit' to exit the program.")
        case 'list':
            if len(students) == 0:
                print('No students found')
            else:
                print("Students:\n" + '\n'.join([str(s.id) for s in students]))
        case 'add points':
            print("Enter an id and points or 'back' to return:")
            points = input()
            while points != 'back':
                feedback, student_id = check_points(points, students)
                print(feedback)
                if student_id is not None:
                    for s in students:
                        if s.id == student_id:
                            s.add_points(points.split(' ')[1:])
                points = input()
        case 'find':
            print("Enter an id or 'back' to return:")
            student_id = input()
            while student_id != 'back':
                try:
                    st = list(filter(lambda x: x.id == student_id, students))[0]
                    print(st)
                except IndexError:
                    print(f'No student is found for id={student_id}.')
                student_id = input()
        case 'statistics':
            print("Type the name of a course to see details or 'back' to quit:")
            popularity = {x: sum([1 if s.progress[x] != 0 else 0 for s in students]) for x in pts.keys()}
            if all([x == 0 for x in popularity.values()]):
                print('Most popular: n/a\nLeast popular: n/a\nHighest activity: n/a\n'
                      'Lowest activity: n/a\nEasiest course: n/a\nHardest course: n/a')
            else:
                activity = {x: sum([s.tasks[x] for s in students]) for x in pts.keys()}
                difficulty = {x: sum([s.progress[x] for s in students]) / activity[x] for x in pts.keys()}
                most_popular = [x for x in popularity.keys() if popularity.get(x) == max(popularity.values())]
                least_popular = set(pts.keys()) - set(most_popular) if len(most_popular) != 4 else ['n/a']
                highest_activity = [x for x in activity.keys() if activity.get(x) == max(activity.values())]
                lowest_activity = set(pts.keys()) - set(highest_activity) if len(highest_activity) != 4 else ['n/a']
                print(
                    f'Most popular: {", ".join(most_popular)}\n'
                    f'Least popular: {", ".join(least_popular)}\n'
                    f'Highest activity: {", ".join(highest_activity)}\n'
                    f'Lowest activity: {", ".join(lowest_activity)}\n'
                    f'Easiest course: {max(difficulty, key=difficulty.get)}\n'
                    f'Hardest course: {min(difficulty, key=difficulty.get)}')

            course = input()
            while course != 'back':
                if course.lower() not in list(map(lambda x: x.lower(), pts.keys())):
                    print('Unknown course')
                else:
                    print(course + '\nid\tpoints\tcompleted\n' + stats_by_course(students, course))
                course = input()
        case 'notify':
            notified = 0
            for student in students:
                should_be_notified = False
                for crs in pts.keys():
                    if student.progress[crs] >= pts[crs] and not student.completed[crs]:
                        student.completed[crs] = True
                        should_be_notified = True
                        print(NOTIFICATION.format(email=student.email, name=student.initials, course=crs))
                notified += 1 if should_be_notified else 0
            print(f'Total {notified} students have been notified')
        case _:
            print('Error: unknown command!')
