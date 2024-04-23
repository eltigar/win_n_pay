from enum import Enum, StrEnum

class cmds(StrEnum):
    start = 'start'
    rules = 'rules'
    help = 'help'
    change_name = 'change_name'
    new = 'new'
    join = 'join'
    repeat = 'repeat'
    repeat_id = 'repeat {}'
    main_menu = 'main_menu'
    leave = 'leave'
    set_points = 'set_points'
    set_money = 'set_money'
    show_joined = 'show_joined'
    play = 'play'
    abort = 'abort'
    unexpected = 'unexpected'
    unknown = 'unknown'

class statuses(StrEnum): # not used probably not needed
    success = "success"

mydict = {
    cmds.new: 'new game is created'
}

# print(mydict[cmds.new])
# print(cmds.new.name == cmds.new)