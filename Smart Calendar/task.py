# DO NOT CHECK THIS SOLUTION. IT'S REALLY MESSED UP CAUSE I'M TIRED OF FIXING IT :(

from datetime import datetime
import re


class Notification:
    def __init__(self, dt: datetime, text, birth=False):
        now = datetime.now()
        self.dt = dt
        delta = now - dt if birth else dt - now
        self.d = delta.days
        self.h = delta.seconds // 60 // 60
        self.m = delta.seconds // 60 % 60
        self.birth = birth
        self.text = text

    @classmethod
    def input_not(cls, i):
        while True:
            parsed = re.search(r'(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2})',
                               input(f'Enter date and time of note #{i} (in format «YYYY-MM-DD HH:MM»):'))
            if parsed is None:
                print('Incorrect format. Please try again (use the format «YYYY-MM-DD HH:MM»)')
                continue
            elif not 1 <= int(parsed[2]) <= 12:
                print('Incorrect month value. The month should be in 01-12.')
                continue
            elif not 0 <= int(parsed[4]) <= 23:
                print('Incorrect hour value. The hour should be in 00-23.')
                continue
            elif not 0 <= int(parsed[5]) <= 59:
                print('Incorrect minute value. The minutes should be in 00-59.')
                continue
            break
        year, month, day, hour, minute = [int(parsed.group(x)) for x in range(1, 6)]
        text = input(f'Enter text of note #{i}:')
        with open('notes.txt', 'a') as outfile:
            outfile.write(datetime(year, month, day, hour, minute).strftime('%Y*%m*%d*%H*%M*') + text + '*0' + '\n')
        return cls(datetime(year, month, day, hour, minute), text)

    @classmethod
    def input_birth(cls, i):
        while True:
            text = input(f'Enter the name of #{i}:')
            parsed = re.search(r'(\d{4})-(\d{2})-(\d{2})',
                               input(f'Enter the date of birth of #{i} (in format «YYYY-MM-DD»):'))
            if parsed is None:
                print('Incorrect format. Please try again (use the format «YYYY-MM-DD»)')
                continue
            elif not 1 <= int(parsed[2]) <= 12:
                print('Incorrect month value. The month should be in 01-12.')
                continue
            break
        year, month, day = [int(parsed.group(x)) for x in range(1, 4)]

        with open('notes.txt', 'a') as outfile:
            outfile.write(datetime(year, month, day, 0, 0).strftime('%Y*%m*%d*%H*%M*') + text + '*1' + '\n')
        return cls(datetime(year, month, day, 0, 0), text, True)

    @classmethod
    def from_line(cls, s):
        data = s.split('*')
        return cls(datetime(int(data[0]), int(data[1]), int(data[2]), int(data[3]), int(data[4])), data[5],
                   data[6][:-1] == '1')

    def __str__(self):
        if self.birth:
            days = (datetime.now() - datetime(datetime.now().year, self.dt.month, self.dt.day)).days
            years = datetime.now().year - self.dt.year
            years += 1 if days > 0 else 0
            days = 366 - days if days > 0 else abs(days)
            return f'{self.text}\'s birthday is {"today" if days == 0 else f"in {days} days"}. He (she) turns {years} years old.'
        else:
            return f'Before the event note "{self.text}" remained: {self.d} day(s), {self.h} hour(s) and {self.m} minute(s).'


print(f'Current date and time:\n{datetime.now()}')

notifications = []
with open('notes.txt', 'r') as file:
    for line in file.readlines():
        notifications.append(Notification.from_line(line))

cmd = ''
while cmd != 'exit':
    cmd = input('Enter the command (add, view, delete, exit):')
    match cmd:
        case 'add':
            tp = input('What do you want to add (note, birthday)?')
            if tp == "note":
                num = int(input('How many notes do you want to add?'))
                for i in range(num):
                    notifications.append(Notification.input_not(i + 1))
                print('Notes added!')
            else:
                num = int(input('How many dates of birth do you want to add?'))
                for i in range(num):
                    notifications.append(Notification.input_birth(i + 1))
                print('Birthdates added!')
        case 'exit':
            break
        case 'view':
            tp = input('What do you want to view (date, note, name)?')
            if tp == "date":
                arr = []
                notes, dates = 0, 0
                date = datetime.strptime(input('Enter date (in format «YYYY-MM-DD»):'), '%Y-%m-%d')
                for n in notifications:
                    if n.dt.month == date.month and n.dt.day == date.day:
                        arr.append(str(n))
                        if n.birth:
                            dates += 1
                        else:
                            notes += 1
                print(f'Found {notes} note(s) and {dates} date(s) of birth on this date:')
                print('\n'.join(arr))
            elif tp == "name":
                arr = []
                while True:
                    name = input('Enter name:')
                    arr = [str(n) for n in notifications if name == n.text]
                    if len(arr) == 0:
                        print('No such person found. Try again:')
                    else:
                        break
                print(f'Found {len(arr)} date of birth:')
                print('\n'.join(arr))
            else:
                arr = []
                while True:
                    txt = input('Enter text of note:')
                    arr = [str(n) for n in notifications if txt in n.text]
                    if len(arr) == 0:
                        print('No such note found. Try again:')
                    else:
                        break
                print(f'Found {len(arr)} note(s) that contain "{txt}":')
                print('\n'.join(arr))
        case 'delete':
            tp = input('What do you want to delete (date, note, name)?')
            if tp == "note":
                while True:
                    txt = input('Enter text of note you want to delete:')
                    if txt not in [n.text for n in notifications]:
                        print('No such note found. Try again:')
                        continue
                    else:
                        if input(f'Are you sure you want to delete "{txt}"?') == 'yes':
                            notifications = [n for n in notifications if n.text != txt]
                            print('Note deleted')
                        else:
                            print('Deletion canceled.')
                        break
            elif tp == "name":
                txt = input('Enter name of the person whose date of birthday you want to delete:')
                arr = [n for n in notifications if n.text == txt]
                if len(arr) == 0:
                    print('No such person found. Try again:')
                else:
                    if input(f'Are you sure you want to delete "{arr[0].text}"? {str(arr[0])}') == 'yes':
                        notifications.remove(arr[0])
                        print('Birthdate deleted')
                    else:
                        print('Deletion canceled.')
            else:
                arr = []
                notes, dates = 0, 0
                date = datetime.strptime(input('Enter date (in format «YYYY-MM-DD»):'), '%Y-%m-%d')
                for n in notifications:
                    if n.dt.month == date.month and n.dt.day == date.day:
                        arr.append(n)
                        if n.birth:
                            dates += 1
                        else:
                            notes += 1
                print(f'Found {notes} note(s) and {dates} date(s) of birth on this date:')
                for n in arr:
                    print(n)
                for n in arr:
                    if input(f'Are you sure you want to delete "{n.text}"?') == 'yes':
                        print(f'{"Note" if not n.birth else "Date of birth"} deleted')
                        notifications.remove(n)
                    else:
                        print('Deletion canceled.')
