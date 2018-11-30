from django.db.models import QuerySet

from searcher.models import Exploit


def search_exploits_in_db(search_text):
    words = str(search_text).split()
    if words[0] == '--exact' and '--in' in words:
        return search_exploits_exact(words[1:])

    if is_number(search_text):
        return search_exploits_numerical(search_text)
    else:
        queryset = search_exploits_for_description(search_text)
        if len(queryset) > 0:
            return queryset
        else:
            queryset = search_exploits_for_file(search_text)
            if len(queryset) > 0:
                return queryset
            else:
                return search_exploits_for_author_platform_type_port(search_text)


def search_exploits_numerical(search_text):
    search_string = 'select * from exploits where ' + 'id = ' + search_text + ' or file like \'%' + search_text + '%\' or description like \'%' + search_text + '%\' or port = ' + search_text
    return Exploit.objects.raw(search_string)


def search_exploits_for_description(search_text):
    words_list = str(search_text).split()
    search_string = 'select * from exploits where (description like \'%' + words_list[0].upper() + '%\''
    for word in words_list[1:]:
        search_string = search_string + ' and description like \'%' + word.upper() + '%\''
    search_string = search_string + ') or ((file like \'%' + words_list[0].upper() + '%\''
    for word in words_list[1:]:
        search_string = search_string + ' or file like \'%' + word.upper() + '%\''
    if not is_number(words_list[0]):
        search_string = search_string + ') and (description like \'%' + words_list[0].upper() + '%\''
        first_alpha = True
    else:
        search_string = search_string + ') and ('
        first_alpha = False
    for word in words_list[1:]:
        if not is_number(word) and first_alpha:
            search_string = search_string + ' or description like \'%' + word.upper() + '%\''
        elif not is_number(word) and not first_alpha:
            search_string = search_string + 'description like \'%' + word.upper() + '%\''
            first_alpha = True
    search_string = search_string + '))'
    print(search_string)
    return Exploit.objects.raw(search_string)


def search_exploits_for_file(search_text):
    words_list = str(search_text).split()
    search_string = 'select * from exploits where (file like \'%' + words_list[0].upper() + '%\''
    for word in words_list[1:]:
        search_string = search_string + ' or file like \'%' + word.upper() + '%\''
    search_string = search_string + ')'
    print(search_string)
    return Exploit.objects.raw(search_string)


def search_exploits_for_author_platform_type_port(search_text):
    words_list = str(search_text).split()
    search_string = 'select * from exploits where (author like \'%' + words_list[0].upper() + '%\''
    for word in words_list[1:]:
        search_string = search_string + ' or author like \'%' + word.upper() + '%\''
    search_string = search_string + ') or (platform like \'%' + words_list[0].upper() + '%\''
    for word in words_list[1:]:
        search_string = search_string + ' or platform like \'%' + word.upper() + '%\''
    search_string = search_string + ') or (exploit_type like \'%' + words_list[0].upper() + '%\''
    for word in words_list[1:]:
        search_string = search_string + ' or platform like \'%' + word.upper() + '%\''
    search_string = search_string + ')'
    print(search_string)
    return Exploit.objects.raw(search_string)


def search_exploits_exact(words):
    accepted_fileds = ['file', 'description', 'author', 'type', 'platform']
    search_string = words[0]
    words_index = 1
    for word in words[1:]:
        if word != '--in':
            search_string = search_string + ' ' + word
            words_index = words_index + 1
        else:
            if words[words_index + 1] not in accepted_fileds:
                words[words_index + 1] = 'description'
                search_string = 'blablabla'
            if words[words_index + 1] == 'type':
                words[words_index + 1] = 'exploit_type'
            print('select * from exploits where ' + words[words_index + 1] + ' = \'%' + search_string.upper() + '%\'')
            return Exploit.objects.raw('select * from exploits where ' + words[words_index + 1] + ' like \'%' + search_string.upper() + '%\'')


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
