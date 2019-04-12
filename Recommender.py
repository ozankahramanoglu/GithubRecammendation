from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from difflib import SequenceMatcher


class StaredRepoData:
    userID = ""
    repoIDArray = []

    def __init__(self, uid, rArray):
        self.userID = uid
        self.repoIDArray = rArray


class GithubRepository:
    repoId = ""
    repoName = ""
    repoURL = ""
    repoLanguage = ""

    def __init__(self, rid, name, url, lang):
        self.repoId = rid
        self.repoName = name
        self.repoURL = url
        self.repoLanguage = lang


class GithubUser:
    userID = ""
    userURL = ""
    username = ""

    def __init__(self, uid, url, name):

        self.userID = uid
        self.userURL = url
        self.username = name


class GUI:



    def setFilter(self):
        global programmingList, userFilter, currentVar
        userFilter = str(currentVar.get())
        self.Recommend_Repo()

    def Recommend_Repo(self):
        global starArray, repoArray, RecommendationTree, userFilter, currentVar
        if currentVar.get() == "None":
            userFilter = ""
        for i in RecommendationTree.get_children():
            RecommendationTree.delete(i)
        counter = 0
        tmpFirst = RecommendTree.focus()
        tmpSecond = RecommendTree.item(tmpFirst).get('values')
        for i in starArray:
            if int(i.userID) == tmpSecond[0]:
                for k in repoArray:
                    if (k.repoId in i.repoIDArray) & (counter != int(recommendNumberEntry.get())):
                        if (userFilter == "") | (userFilter == "None"):
                            RecommendationTree.insert('', 'end', text=k.repoName, values=(k.repoURL, 5))
                            counter += 1
                        else:
                            if(k.repoLanguage == userFilter):
                                RecommendationTree.insert('', 'end', text=k.repoName, values=(k.repoURL, 5))
                                counter += 1



    def similar(self, a, b,fastorslow):
        if fastorslow == "fast":
            return SequenceMatcher(None, a, b).ratio()
        else:
            return SequenceMatcher(None, a, b).real_quick_ratio()

    def Upload_Star_Data(self):

        file = open(filedialog.askopenfilename(title="Select file"), 'r')
        global starArray
        starArray = []
        for i in file:
            if '\n' in i:
                i = i[0:-1]
            tmpid = i.split("\t")
            tmpStarList = tmpid[1].split(",")
            newStarData = StaredRepoData(uid=tmpid[0], rArray=tmpStarList)
            starArray.append(newStarData)



    def Upload_Repo_Data(self):
        global repoArray
        repoArray = []
        langList = []

        file = open(filedialog.askopenfilename(title="Select file"), 'r')
        for i in file:
            if '\n' in i:
                i = i[0:-1]
            tmp = i.split(",")
            newRepo = GithubRepository(rid=tmp[0], name=tmp[1], url=tmp[2], lang=tmp[3])
            repoArray.append(newRepo)
            langList.append(newRepo.repoLanguage)

        langList = set(langList)
        langList = list(langList)
        langList = ["None"] + langList

        programmingList['values'] = list(langList)
        programmingList.current(0)

    def Upload_User_Data(self):
        userArray = []
        file = open(filedialog.askopenfilename(title="Select file"), 'r')
        for i in file:
            if '\n' in i:
                i = i[0:-1]

            tmp = (i.split(","))
            newUser = GithubUser(uid=tmp[0], url=tmp[1], name=tmp[2])
            userArray.append(newUser)
        userArray = (sorted(userArray, key=lambda GithubUser: GithubUser.username))
        for i in userArray:
            RecommendTree.insert('', 'end', text=i.username, values=i.userID)

    def __init__(self):
        window = Tk()
        window.title("Github Repository Recomender")

        mainframe = ttk.Frame(window, padding="3 3 12 12")
        mainframe.grid(column=7, row=20, sticky=(N, W, E, S))

        global RecommendTree, programmingList, RecommendationTree, recommendNumberEntry, currentVar

        DistanceLabel = Label(mainframe, text="Github Project Recommender", font=("Arial Bold", 20), anchor=W, padx=400)
        DistanceLabel.grid(column=0, row=0, sticky=(W, E, S), columnspan=7)

        userData = ttk.Button(master=mainframe, text="Upload User Data", command=self.Upload_User_Data)
        userData.grid(column=1, row=1, sticky=(W, E))

        repoData = ttk.Button(master=mainframe, text="Upload Repository Data", command=self.Upload_Repo_Data)
        repoData.grid(column=4, row=1, sticky=(W, E, S))

        starData = ttk.Button(master=mainframe, text="Upload Star Data", command=self.Upload_Star_Data)
        starData.grid(column=6, row=1, sticky=E)

        mainframe.grid_rowconfigure(3, minsize=40)

        col_count, row_count = mainframe.grid_size()

        for col in range(col_count-1):
            mainframe.grid_columnconfigure(col+1, minsize=40, weight=80)

        RecommendLabel = Label(mainframe, text="Recommend Repository for", font=("Arial Bold", 10))
        RecommendLabel.grid(column=1, row=4, sticky=(W, E, S))

        RecommendTree = ttk.Treeview(mainframe, columns='Username')
        RecommendTree.grid(column=1, row=5, sticky=(W, E, S), rowspan=10)


        RecommendTree.heading('#0', text='Username')
        RecommendTree.column("#0", minwidth=0, width=250, stretch=NO)
        RecommendTree.heading('#1', text='ID')
        RecommendTree.column("#1", minwidth=0, width=100, stretch=NO)

        RecommendationdLabel = Label(mainframe, text="Recommendations", font=("Arial Bold", 10))
        RecommendationdLabel.grid(column=5, row=3, sticky=(W, E, S), columnspan=3)

        RecommendationTree = ttk.Treeview(mainframe, height=16, columns=('URL', 'Score'))
        RecommendationTree.grid(column=5, row=4, sticky=(W, E, S), rowspan=16, columnspan=3)

        RecommendationTree.heading('#0', text='Name')
        RecommendationTree.column("#0", minwidth=0, width=50, stretch=NO)
        RecommendationTree.heading('#1', text='URL')
        RecommendationTree.column("#1", minwidth=0, width=200, stretch=NO)
        RecommendationTree.heading('#2', text='Score')
        RecommendationTree.column("#2", minwidth=0, width=50, stretch=NO)

        mainframe.grid_columnconfigure(2, minsize=40)

        recommendRepo = ttk.Button(master=mainframe, text="Recommend Repository", command=self.Recommend_Repo)
        recommendRepo.grid(column=3, row=11, sticky=(W, E, N))

        recommendUser = ttk.Button(master=mainframe, text="Recommend Github User")
        recommendUser.grid(column=3, row=12, sticky=(W, E, N))

        FilterLabel = Label(mainframe, text="Filter programming language:", font=("Arial Bold", 10))
        FilterLabel.grid(column=1, row=15, sticky=(W, E, S))

        currentVar = StringVar()
        programmingList = ttk.Combobox(master=mainframe)
        programmingList.config(textvariable=currentVar)
        programmingList.grid(column=1, row=16, sticky="N")
        programmingList.bind("<<ComboboxSelected>>", lambda e: self.setFilter())

        DistanceLabel = Label(mainframe, text="Distance algorithm:", font=("Arial Bold", 10))
        DistanceLabel.grid(column=1, row=17, sticky=(W, E, S))

        normalVar = IntVar()
        fastVar = IntVar()

        normalCheck = Checkbutton(mainframe, text="Normal", variable=normalVar)
        normalCheck.grid(column=1, row=18, sticky=(W, E, S))

        fastCheck = Checkbutton(mainframe, text="Fast", variable=fastVar)
        fastCheck.grid(column=1, row=19, sticky=(W, E, S))

        recommendNumberLabel = Label(mainframe, text="Number of recommendation:", font=("Arial Bold", 10))
        recommendNumberLabel.grid(column=1, row=20, sticky=(W, E, S))

        v = StringVar(mainframe, value='3')
        recommendNumberEntry = Entry(mainframe, width=1, textvariable=v)
        recommendNumberEntry.grid(column=2, row=20, sticky=(W, E))

        window.mainloop()

if __name__ == "__main__":
    gui = GUI()
