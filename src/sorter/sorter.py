import difflib


def get_similarity(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2).ratio()


def sort_by_search_key(course_list, search_key):
    # info[0] == course_platform
    # info[1] == course_name
    # info[2] == course_link
    # info[3] == course_college
    return sorted(course_list, key=lambda info: get_similarity(search_key, info[0] + info[1] + info[3]), reverse=True)


def sort_by_name(course_list):
    filtered_course_list = list(filter(lambda info: info[1] != '', course_list))
    return sorted(filtered_course_list, key=lambda info: info[1])


def sort_by_platform(course_list):
    filtered_course_list = list(filter(lambda info: info[0] != '', course_list))
    return sorted(filtered_course_list, key=lambda info: info[0])


def sort_by_college(course_list):
    filtered_course_list = list(filter(lambda info: info[3] != '', course_list))
    return sorted(filtered_course_list, key=lambda info: info[3])


if __name__ == '__main__':
    key = input()
    lst = [('计算机组成', '', '王道考研', '北航'), ('计算机组成123', '', '王道考研', '清华'),
           ('计算机组成777', '', '满分考研', '')]
    sorted_list = sort_by_search_key(lst, key)
    print(sorted_list)
