#  Copyright (C)  2021 Rage Uday Kiran
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.

import abstract as _ab


class _FFList:
    """
     A class represent a Fuzzy List of an element

    Attributes :
    ----------
         item: int
             the item name
         sumIUtil: float
             the sum of utilities of an fuzzy item in database
         sumRUtil: float
             the sum of resting values of a fuzzy item in database
         elements: list
             a list of elements contain tid,Utility and resting values of element in each transaction
    Methods :
    -------
        addElement(element)
            Method to add an element to this fuzzy list and update the sums at the same time.

        printElement(e)
            Method to print elements

    """

    def __init__(self, itemName):
        self.item = itemName
        self.sumIUtil = 0.0
        self.elements = []

    def addElement(self, element):
        """
            A Method that add a new element to FFList

            :param element: an element to be add to FFList
            :pram type: Element
        """
        self.sumIUtil += element.iUtils
        self.elements.append(element)

    def printElement(self):
        """
            A method to print elements
        """
        for ele in self.elements:
            print(ele.tid, ele.iUtils, ele.rUtils)


class _Element:
    """
        A class represents an Element of a fuzzy list

    Attributes:
    ----------
            tid : int
                keep tact of transaction id
            iUtils: float
                the utility of an fuzzy item in the transaction
            rUtils : float
                the  resting value of an fuzzy item in the transaction
    """

    def __init__(self, tid, iUtil):
        self.tid = tid
        self.iUtils = iUtil


class _Regions:
    """
        A class calculate the regions

    Attributes:
    ----------
            G : int
                G region value
            M: int
                M region value
            H : int
                H region values
        """

    def __init__(self, quantity, regionsNumber):
        self.G = 0
        self.M = 0
        self.UH = 0
        self.UH4SG = 0
        self.VUH = 0
        self.H = 0
        if regionsNumber == 6:  # if we have 3 regions
            # if 0 < quantity <= 1:
            #     self.G = 1
            #     self.H = 0
            #     self.M = 0
            # elif 1 < quantity <= 6:
            #     self.G = float((6 - quantity) / 5)
            #     self.M = float((quantity - 1) / 5)
            #     self.H = 0
            # elif 6 < quantity <= 11:
            #     self.G = 0
            #     self.M = float((11 - quantity) / 5)
            #     self.H = float((quantity - 6) / 5)
            # else:
            #     self.G = 0
            #     self.M = 0
            #     self.H = 1
            if 0 < quantity <= 10:
                self.G = 1
                self.H = 0
                self.M = 0
                self.UH = 0
                self.UH4SG = 0
                self.VUH = 0
            elif 11 < quantity <= 15:
                self.G = float((15 - quantity) / 4)
                self.M = float((quantity - 10) / 4)
                self.H = 0
                self.UH = 0
                self.UH4SG = 0
                self.VUH = 0
            elif 16 < quantity <= 35:
                self.G = 0
                self.M = float((35 - quantity) / 20)
                self.UH4SG = float((quantity - 15) / 20)
                self.H = 0
                self.UH = 0
                self.VUH = 0
            elif 36 < quantity <= 50:
                self.G = 0
                self.M = 0
                self.UH4SG = float((50 - quantity) / 15)
                self.UH = float((quantity - 35) / 15)
                self.H = 0
                self.VUH = 0
            elif 51 < quantity <= 70:
                self.G = 0
                self.M = 0
                self.UH4SG = 0
                self.UH = float((70 - quantity) / 20)
                self.VUH = float((quantity - 50) / 20)
                self.H = 0
            else:
                self.G = 0
                self.M = 0
                self.UH = 0
                self.VUH = 0
                self.UH4SG = 0
                self.H = 1


class _Pair:
    """
        A class to store item and it's quantity together
    """

    def __init__(self):
        self.item = 0
        self.quantity = 0


class FFIMiner(_ab._fuzzyFrequentPattenrs):
    """
        Fuzzy Frequent  Pattern-Miner is desired to find all  frequent fuzzy patterns which is on-trivial and challenging problem
        to its huge search space.we are using efficient pruning techniques to reduce the search space.
    Reference :
    ---------
        https://www.researchgate.net/publication/286510908_A_fast_Algorithm_for_mining_fuzzy_frequent_itemSets

    Attributes :
    ----------
        iFile : string
            Name of the input file to mine complete set of fuzzy spatial frequent patterns
        oFile : string
               Name of the oFile file to store complete set of fuzzy spatial frequent patterns
        minSup : float
            The user given minimum support
        memoryRSS : float
                To store the total amount of RSS memory consumed by the program
        startTime:float
               To record the start time of the mining process
        endTime:float
            To record the completion time of the mining process
        itemsCnt: int
            To record the number of fuzzy spatial itemSets generated
        mapItemsGSum: map
            To keep track of G region values of items
        mapItemsMidSum: map
            To keep track of M region values of items
        mapItemsHSum: map
            To keep track of H region values of items
        mapItemSum: map
            To keep track of sum of Fuzzy Values of items
        mapItemRegions: map
            To Keep track of fuzzy regions of item
        jointCnt: int
            To keep track of the number of ffi-list that was constructed
        BufferSize: int
            represent the size of Buffer
        itemBuffer list
            to keep track of items in buffer
    Methods :
    -------
        startMine()
            Mining process will start from here
        getPatterns()
            Complete set of patterns will be retrieved with this function
        save(oFile)
            Complete set of frequent patterns will be loaded in to a output file
        getPatternsAsDataFrame()
            Complete set of frequent patterns will be loaded in to a dataframe
        getMemoryUSS()
            Total amount of USS memory consumed by the mining process will be retrieved from this function
        getMemoryRSS()
            Total amount of RSS memory consumed by the mining process will be retrieved from this function
        getRuntime()
            Total amount of runtime taken by the mining process will be retrieved from this function
        convert(value):
            To convert the given user specified value
        compareItems(o1, o2)
            A Function that sort all ffi-list in ascending order of Support
        FSFIMining(prefix, prefixLen, FSFIM, minSup)
            Method generate ffi from prefix
        construct(px, py)
            A function to construct Fuzzy itemSet from 2 fuzzy itemSets
        findElementWithTID(uList, tid)
            To find element with same tid as given
        WriteOut(prefix, prefixLen, item, sumIUtil)
            To Store the patten

    Executing the code on terminal :
    -------
        Format:
            python3 FFIMinerMiner.py <inputFile> <outputFile> <minSup> <separator>
        Examples:
            python3  FFIMinerMiner.py sampleTDB.txt output.txt 6  (minSup will be considered in support count or frequency)

            python3  FFIMinerMiner.py sampleTDB.txt output.txt 0.3 (minSup and maxPer will be considered in percentage of database)
                                                      (it will consider '\t' as a separator)

            python3  FFIMinerMiner.py sampleTDB.txt output.txt 6 , (it consider ',' as a separator)

    Sample run of importing the code:
    -------------------------------

        from PAMI.fuzzyFrequentPatterns import FFIMiner as alg

        obj = alg.FFIMiner("input.txt", 2)

        obj.startMine()

        fuzzyFrequentPatterns = obj.getPatterns()

        print("Total number of Fuzzy Frequent Patterns:", len(fuzzyFrequentPatterns))

        obj.save("outputFile")

        memUSS = obj.getMemoryUSS()

        print("Total Memory in USS:", memUSS)

        memRSS = obj.getMemoryRSS()

        print("Total Memory in RSS", memRSS)

        run = obj.getRuntime()

        print("Total ExecutionTime in seconds:", run)


    Credits:
    -------
        The complete program was written by B.Sai Chitra under the supervision of Professor Rage Uday Kiran.
    """
    _startTime = float()
    _endTime = float()
    _minSup = str()
    _maxPer = float()
    _finalPatterns = {}
    _iFile = " "
    _oFile = " "
    _memoryUSS = float()
    _memoryRSS = float()
    _sep = "\t"

    def __init__(self, iFile, minSup, sep="\t"):
        super().__init__(iFile, minSup, sep)
        self._startTime = 0
        self._endTime = 0
        self._itemsCnt = 0
        self._mapItemsGSum = {}
        self._mapItemsUHSum = {}
        self._mapItemsVUHSum = {}
        self._mapItemsUH4SGSum = {}
        self._mapItemsMidSum = {}
        self._mapItemsHSum = {}
        self._mapItemSum = {}
        self._mapItemRegions = {}
        self._joinsCnt = 0
        self._BufferSize = 200
        self._itemSetBuffer = []
        self._transactions = []
        self._fuzzyValues = []
        self._ts = []
        self._finalPatterns = {}
        self._dbLen = 0

    def _compareItems(self, o1, o2):
        """
            A Function that sort all ffi-list in ascending order of Support
        """
        compare = self._mapItemSum[o1.item] - self._mapItemSum[o2.item]
        if compare == 0:
            if o1.item < o2.item:
                return -1
            elif o1.item > o2.item:
                return 1
            else:
                return 0
        else:
            return compare

    def _convert(self, value):
        """
        To convert the given user specified value
        :param value: user specified value
        :return: converted value
        """
        if type(value) is int:
            value = int(value)
        if type(value) is float:
            value = (self._dbLen * value)
        if type(value) is str:
            if '.' in value:
                value = float(value)
                value = (self._dbLen * value)
            else:
                value = int(value)
        return value

    def _creatingItemsets(self):
        self._transactions, self._fuzzyValues, self._Database, self._ts = [], [], [], []
        if isinstance(self._iFile, _ab._pd.DataFrame):
            if self._iFile.empty:
                print("its empty..")
            i = self._iFile.columns.values.tolist()
            if 'Transactions' in i:
                self._transactions = self._iFile['Transactions'].tolist()
            if 'fuzzyValues' in i:
                self._fuzzyValues = self._iFile['fuzzyValues'].tolist()
            # print(self.Database)
        if isinstance(self._iFile, str):
            if _ab._validators.url(self._iFile):
                data = _ab._urlopen(self._iFile)
                for line in data:
                    line = line.decode("utf-8")
                    line = line.split("\n")[0]
                    parts = line.split(":")
                    parts[0] = parts[0].strip()
                    parts[2] = parts[2].strip()
                    items = parts[0].split(self._sep)
                    quantities = parts[2].split(self._sep)
                    self._transactions.append([x for x in items])
                    self._fuzzyValues.append([x for x in quantities])
            else:
                try:
                    with open(self._iFile, 'r', encoding='utf-8') as f:
                        count = 0
                        for line in f:
                            count += 1
                            # if count > 10000:
                            #     break
                            line = line.strip()
                            parts = line.split(":")
                            parts[0] = parts[0].strip()
                            parts[1] = parts[1].strip()
                            parts[2] = parts[2].strip()
                            times = parts[0].split(self._sep)
                            items = parts[1].split(self._sep)
                            quantities = parts[2].split(self._sep)
                            #print(times, items, quantities)
                            _time = [x for x in times if x]
                            items = [x for x in items if x]
                            quantities = [x for x in quantities if x]
                            tempList = []
                            for k in range(len(_time)):
                                ite = "(" + _time[k] + "," + items[k] + ")"
                                tempList.append(ite)
                            self._transactions.append([x for x in tempList])
                            self._fuzzyValues.append([x for x in quantities])
                except IOError:
                    print("File Not Found")
                    quit()

    def startMine(self):
        """
          fuzzy-Frequent pattern mining process will start from here
        """
        self._startTime = _ab._time.time()
        self._creatingItemsets()
        print(len(self._transactions))
        for line in range(len(self._transactions)):
            items = self._transactions[line]
            quantities = self._fuzzyValues[line]
            self._dbLen += 1
            for i in range(0, len(items)):
                regions = _Regions(float(quantities[i]), 6)
                item = items[i]
                if item in self._mapItemsGSum.keys():
                    G = self._mapItemsGSum[item]
                    G += regions.G
                    self._mapItemsGSum[item] = G
                else:
                    self._mapItemsGSum[item] = regions.G
                if item in self._mapItemsMidSum.keys():
                    mid = self._mapItemsMidSum[item]
                    mid += regions.M
                    self._mapItemsMidSum[item] = mid
                else:
                    self._mapItemsMidSum[item] = regions.M
                if item in self._mapItemsHSum.keys():
                    H = self._mapItemsHSum[item]
                    H += regions.H
                    self._mapItemsHSum[item] = H
                else:
                    self._mapItemsHSum[item] = regions.H
                if item in self._mapItemsUHSum.keys():
                    uh = self._mapItemsUHSum[item]
                    uh += regions.UH
                    self._mapItemsUHSum[item] = uh
                else:
                    self._mapItemsUHSum[item] = regions.UH
                if item in self._mapItemsVUHSum.keys():
                    VUH = self._mapItemsVUHSum[item]
                    VUH += regions.VUH
                    self._mapItemsVUHSum[item] = VUH
                else:
                    self._mapItemsVUHSum[item] = regions.VUH
                if item in self._mapItemsUH4SGSum.keys():
                    UH4SG = self._mapItemsUH4SGSum[item]
                    UH4SG += regions.UH4SG
                    self._mapItemsUH4SGSum[item] = UH4SG
                else:
                    self._mapItemsUH4SGSum[item] = regions.UH4SG
        listOfffilist = []
        mapItemsToFFLIST = {}
        #self._minSup = self._convert(self._minSup)
        # minSup = self.minSup
        for item1 in self._mapItemsGSum.keys():
            item = item1
            G = self._mapItemsGSum[item]
            mid = self._mapItemsMidSum[item]
            uh4sg = self._mapItemsUH4SGSum[item]
            uh = self._mapItemsUHSum[item]
            vuh = self._mapItemsVUHSum[item]
            H = self._mapItemsHSum[item]
            if G >= mid and G >= H and G >= uh4sg and G >= uh and G >= vuh:
                self._mapItemSum[item] = G
                self._mapItemRegions[item] = "G"
            elif mid >= G and mid >= H and mid >= uh4sg and mid >= uh and mid >= vuh:
                self._mapItemSum[item] = mid
                self._mapItemRegions[item] = "M"
            elif uh4sg >= G and uh4sg >= H and uh4sg >= mid and uh4sg >= uh and uh4sg >= vuh:
                self._mapItemSum[item] = uh4sg
                self._mapItemRegions[item] = "UH4SG"
            elif uh >= G and uh >= H and uh >= uh4sg and uh >= mid and uh >= vuh:
                self._mapItemSum[item] = uh
                self._mapItemRegions[item] = "UH"
            elif vuh >= G and vuh >= H and vuh >= uh4sg and vuh >= uh and vuh >= mid:
                self._mapItemSum[item] = vuh
                self._mapItemRegions[item] = "VUH"
            elif H >= G and H >= mid and H >= uh4sg and H >= uh and H >= vuh:
                self._mapItemRegions[item] = "H"
                self._mapItemSum[item] = H
            if self._mapItemSum[item] >= self._minSup:
                fuList = _FFList(item)
                mapItemsToFFLIST[item] = fuList
                listOfffilist.append(fuList)
        # for x, y in self._mapItemSum.items():
        #     print(x, y)
        #print(len(self._mapItemSum))
        listOfffilist.sort(key=_ab._functools.cmp_to_key(self._compareItems))
        tid = 0
        for line in range(len(self._transactions)):
            items = self._transactions[line]
            quantities = self._fuzzyValues[line]
            revisedTransaction = []
            for i in range(0, len(items)):
                pair = _Pair()
                pair.item = items[i]
                regions = _Regions(float(quantities[i]), 6)
                item = pair.item
                if self._mapItemSum[item] >= self._minSup:
                    if self._mapItemRegions[pair.item] == "G":
                        pair.quantity = regions.G
                    elif self._mapItemRegions[pair.item] == "M":
                        pair.quantity = regions.M
                    if self._mapItemRegions[pair.item] == "UH4SG":
                        pair.quantity = regions.UH4SG
                    if self._mapItemRegions[pair.item] == "UH":
                        pair.quantity = regions.UH
                    if self._mapItemRegions[pair.item] == "VUH":
                        pair.quantity = regions.VUH
                    elif self._mapItemRegions[pair.item] == "H":
                        pair.quantity = regions.H
                    if pair.quantity > 0:
                        revisedTransaction.append(pair)
            revisedTransaction.sort(key=_ab._functools.cmp_to_key(self._compareItems))
            for i in range(len(revisedTransaction) - 1, -1, -1):
                pair = revisedTransaction[i]
                if mapItemsToFFLIST.get(pair.item) is not None:
                    FFListOfItem = mapItemsToFFLIST[pair.item]
                    element = _Element(tid, pair.quantity)
                    FFListOfItem.addElement(element)
            tid += 1
        # for i in listOfffilist:
        #     print(i.item)
        self._FSFIMining(self._itemSetBuffer, 0, listOfffilist, self._minSup)
        self._endTime = _ab._time.time()
        process = _ab._psutil.Process(_ab._os.getpid())
        self._memoryUSS = float()
        self._memoryRSS = float()
        self._memoryUSS = process.memory_full_info().uss
        self._memoryRSS = process.memory_info().rss

    def _FSFIMining(self, prefix, prefixLen, FSFIM, minSup):
        """Generates ffi from prefix

        :param prefix: the prefix patterns of ffi
        :type prefix: len
        :param prefixLen: the length of prefix
        :type prefixLen: int
        :param FSFIM: the Fuzzy list of prefix itemSets
        :type FSFIM: list
        :param minSup: the minimum support of
        :type minSup:int
        """
        for i in range(0, len(FSFIM)):
            X = FSFIM[i]
            exULs = []
            if X.sumIUtil >= minSup:
                self._WriteOut(prefix, prefixLen, X.item, X.sumIUtil)
                for j in range(i + 1, len(FSFIM)):
                    Y = FSFIM[j]
                    exULs.append(self._construct(X, Y))
                    self._joinsCnt += 1
            self._itemSetBuffer.insert(prefixLen, X.item)
            self._FSFIMining(self._itemSetBuffer, prefixLen + 1, exULs, minSup)

    def getMemoryUSS(self):
        """Total amount of USS memory consumed by the mining process will be retrieved from this function

        :return: returning USS memory consumed by the mining process
        :rtype: float
        """

        return self._memoryUSS

    def getMemoryRSS(self):
        """Total amount of RSS memory consumed by the mining process will be retrieved from this function

        :return: returning RSS memory consumed by the mining process
        :rtype: float
       """
        return self._memoryRSS

    def getRuntime(self):
        """Calculating the total amount of runtime taken by the mining process


        :return: returning total amount of runtime taken by the mining process
        :rtype: float
       """
        return self._endTime - self._startTime

    def _construct(self, px, py):
        """
            A function to construct a new Fuzzy itemSet from 2 fuzzy itemSets

            :param px:the itemSet px
            :type px:ffi-List
            :param py:itemSet py
            :type py:ffi-List
            :return :the itemSet of pxy(px and py)
            :rtype :ffi-List
        """
        pxyUL = _FFList(py.item)
        for ex in px.elements:
            ey = self._findElementWithTID(py, ex.tid)
            if ey is None:
                continue
            eXY = _Element(ex.tid, min([ex.iUtils, ey.iUtils], key=lambda x: float(x)))
            pxyUL.addElement(eXY)
        return pxyUL

    def _findElementWithTID(self, uList, tid):
        """
            To find element with same tid as given
            :param uList: fuzzyList
            :type uList: ffi-List
            :param tid: transaction id
            :type tid: int
            :return: element  tid as given
            :rtype: element if exit or None
        """
        List = uList.elements
        first = 0
        last = len(List) - 1
        while first <= last:
            mid = (first + last) >> 1
            if List[mid].tid < tid:
                first = mid + 1
            elif List[mid].tid > tid:
                last = mid - 1
            else:
                return List[mid]
        return None

    def _WriteOut(self, prefix, prefixLen, item, sumIUtil):
        """
            To Store the patten

            :param prefix: prefix of itemSet
            :type prefix: list
            :param prefixLen: length of prefix
            :type prefixLen: int
            :param item: the last item
            :type item: int
            :param sumIUtil: sum of utility of itemSet
            :type sumIUtil: float

        """
        self._itemsCnt += 1
        res = ""
        for i in range(0, prefixLen):
            res += str(prefix[i]) + "." + str(self._mapItemRegions[prefix[i]]) + "\t"
        res += str(item) + "." + str(self._mapItemRegions.get(item))
        res1 = str(sumIUtil)
        self._finalPatterns[res] = res1

    def getPatternsAsDataFrame(self):
        """Storing final frequent patterns in a dataframe

        :return: returning frequent patterns in a dataframe
        :rtype: pd.DataFrame
        """

        dataFrame = {}
        data = []
        for a, b in self._finalPatterns.items():
            data.append([a.replace('\t', ' '), b])
            dataFrame = _ab._pd.DataFrame(data, columns=['Patterns', 'Support'])
        return dataFrame

    def getPatterns(self):
        """ Function to send the set of frequent patterns after completion of the mining process

        :return: returning frequent patterns
        :rtype: dict
        """
        return self._finalPatterns

    def save(self, outFile):
        """Complete set of frequent patterns will be loaded in to a output file

        :param outFile: name of the output file
        :type outFile: file
        """
        self._oFile = outFile
        writer = open(self._oFile, 'w+')
        for x, y in self._finalPatterns.items():
            patternsAndSupport = x.strip() + ":" + str(y)
            writer.write("%s \n" % patternsAndSupport)

    def printResults(self):
        print("Total number of Fuzzy Frequent Patterns:", len(self.getPatterns()))
        print("Total Memory in USS:", self.getMemoryUSS())
        print("Total Memory in RSS", self.getMemoryRSS())
        print("Total ExecutionTime in seconds:", self.getRuntime())


if __name__ == "__main__":
    _ap = str()
    if len(_ab._sys.argv) == 4 or len(_ab._sys.argv) == 5:
        if len(_ab._sys.argv) == 5:
            _ap = FFIMiner(_ab._sys.argv[1], _ab._sys.argv[3], _ab._sys.argv[4])
        if len(_ab._sys.argv) == 4:
            _ap = FFIMiner(_ab._sys.argv[1], _ab._sys.argv[3])
        _ap.startMine()
        print("Total number of Fuzzy-Frequent Patterns:", len(_ap.getPatterns()))
        _ap.save(_ab._sys.argv[2])
        print("Total Memory in USS:", _ap.getMemoryUSS())
        print("Total Memory in RSS", _ap.getMemoryRSS())
        print("Total ExecutionTime in seconds:", _ap.getRuntime())
    else:
        _ap = FFIMiner('IEEEFuzzySample_2023.txt', 1.5, ' ')
        _ap.startMine()
        print("Total number of Fuzzy-Frequent Patterns:", len(_ap.getPatterns()))
        _ap.save('Fuzzy2023_output.txt')
        print("Total Memory in USS:", _ap.getMemoryUSS())
        print("Total Memory in RSS", _ap.getMemoryRSS())
        print("Total ExecutionTime in seconds:", _ap.getRuntime())
        print("Error! The number of input parameters do not match the total number of parameters provided")
