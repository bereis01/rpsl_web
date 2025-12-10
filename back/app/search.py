def search_dict(result, search):
    # Applies search over a dictionary
    if search:
        unfiltered_result = result
        result = {}
        for key in unfiltered_result.keys():
            keywords = search.split(",")
            contains_all = True
            for keyword in keywords:
                if not (
                    keyword.strip().lower()
                    in (str(key) + str(unfiltered_result[key])).lower()
                ):
                    contains_all = False
                    break
            if contains_all:
                result[key] = unfiltered_result[key]
    return result


def search_list(result, search):
    # Applies search over a list
    if search:
        unfiltered_result = result
        result = []
        for item in unfiltered_result:
            keywords = search.split(",")
            contains_all = True
            for keyword in keywords:
                if not (keyword.strip().lower() in str(item).lower()):
                    contains_all = False
                    break
            if contains_all:
                result.append(item)
    return result
