import os

from app.models import File

HOME = '/Users/karuhanga/'


def run(starting_at=HOME):
    for root, dirs, files in os.walk(starting_at):
        for name in files:
            file = File.objects.get_or_create(path=os.path.join(root, name),
                                              name=name)
            if file[1]:
                print('Saved ' + name + '.')
        for name in dirs:
            dir = File.objects.get_or_create(path=os.path.join(root, name),
                                             name=name)
            if dir[1]:
                print('Saved ' + name + '.')


def save_relevant():
    for dir in ['Documents', 'Videos', 'Downloads', 'Music']:
        print("Running on " + dir)
        run(HOME + dir)


if __name__ == '__main__':
    run(HOME)
