class Util(object):
    @classmethod
    def nestedTupleToList(cls, a):
        outList = []
        for item in a:
            if type(item) == tuple:
                outList.append(cls.nestedTupleToList(item))
            else:
                outList.append(item)
        return outList

    @classmethod
    def nestedListToTuple(cls, a):
        outList = []
        for item in a:
            if type(item) == list:
                outList.append(cls.nestedListToTuple(item))
            else:
                outList.append(item)
        return tuple(outList)