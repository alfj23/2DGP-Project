
# layer 0: Background Objects
# layer 1: Foreground Objects
objects = [[],[]]


def add_object(o, layer): #게임월드에 객체 넣기
    objects[layer].append(o) # 몇번 레이언지 알려주기


def remove_object(o): #게임월드에서 객체 삭제하기
    for i in range(len(objects)): #리스트 안에 리스트가 있으므로 어디 있는지 찾아야함. len(object) = 2 임. 확장성있는 코드~
        if o in objects[i]:
            objects[i].remove(o)
            del o # 메모리 반환


def clear():
    for o in all_objects():
        del o
    objects.clear()


def all_objects(): # 중요 :
    for i in range(len(objects)): # 백그라운드 던져주고 -> 포어그라운드 던져줌.
        for o in objects[i]:
            yield o # 제너레이터 : 뭔가 계속해서 보내줌

