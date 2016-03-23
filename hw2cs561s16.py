import sys
import copy
def CreateArgList(ArgRaw):
    index2=ArgRaw.find('(')
    index3=ArgRaw.find(')')
    argumentsraw=ArgRaw[index2:index3+1]
    comacount=argumentsraw.count(',')
    argumentcount=comacount+1
    argi=0
    ArgList=[]
    while(argi<argumentcount):
            if (argumentsraw.find(',') != -1):
                indexcoma=argumentsraw.find(',')
                argument=argumentsraw[1:indexcoma]
                ArgList.append(argument)
                argumentsraw=argumentsraw[indexcoma+1:]
            elif (argumentsraw.find(',') == -1):
                ArgList.append(argumentsraw[1:-1])
            argi+=1
    return ArgList
def isVariable(text):
    if text[0].isupper()==0 :
       return True
def isConstant(text):
    if text[0].isupper()==1 :
        return True
def Join(FnctnName,ArgList):
    strsentence  = ''
    strsentence += FnctnName + '('
    strsentence += ArgList[0]
    for a in ArgList[1:]:
        strsentence += ', ' + a
    strsentence += ')'
    return strsentence
m=700
def RBRSTD(sentence):
    list=[]
    global m
    CombinedArgList=[]
    temp=[]
    if (sentence.find('&&') == -1 ):
      index=sentence.find('(')
      GoalPredicate=sentence[0:index]
      temp.append(GoalPredicate)
      arguments=sentence[index:sentence.find(')')+1]
      arglist=CreateArgList(arguments)
      CombinedArgList.append(arglist)
      rest=sentence[sentence.find(')')+1:]
      if (rest.find('=>') != -1):
        index4=rest.find('=>')
        index5=rest.find('(')
        index6=rest.find(')')
        arguments2=rest[index5:index6+1]
        arglist2=CreateArgList(arguments2)
        CombinedArgList.append(arglist2)
        g=rest[index4+3:index5]
        temp.append(g)
    else :
      count=sentence.count('&&')
      nop=count+1
      index=sentence.find('(')
      index7=sentence.find(')')
      temp.append(sentence[0:index])
      arglist3=CreateArgList(sentence[index:index7+1])
      CombinedArgList.append(arglist3)
      rest=sentence[index7+1:]
      j=1
      while(j<nop):
        temp1=rest.find('&&')
        temp2=rest.find('(')
        temp3=rest.find(')')
        temp.append(rest[temp1+3:temp2])
        arglist4=CreateArgList(rest[temp2:temp3+1])
        CombinedArgList.append(arglist4)
        rest=rest[temp3+1:]
        j+=1
      index2=rest.find('=>')
      index3=rest.find('(')
      index8=rest.find(')')
      temp.append(rest[index2+3:index3])
      arglist5=CreateArgList(rest[index3:index8+1])
      CombinedArgList.append(arglist5)
    predList=copy.deepcopy(temp)
    localm={}
    x=0
    while x<len(CombinedArgList):
        y=0
        while(y<len(CombinedArgList[x])):
            if (isVariable(CombinedArgList[x][y])):
                if CombinedArgList[x][y] in localm:
                    CombinedArgList[x][y]=localm[CombinedArgList[x][y]]
                else:
                    localm[CombinedArgList[x][y]]=CombinedArgList[x][y]+str(m)
                    CombinedArgList[x][y]=CombinedArgList[x][y]+str(m)
                    m+=1
            y+=1
        x+=1
    SentenceMerged=''
    if len(CombinedArgList)==0:
        SentenceMerged=''
    elif len(CombinedArgList)==1:
        SentenceMerged=Join(predList[0],CombinedArgList[0])
    elif len(CombinedArgList)==2:
        SentenceMerged=Join(predList[0],CombinedArgList[0])+' => '+Join(predList[1],CombinedArgList[1])
    else :
        g=0
        while(g<len(CombinedArgList)-1):
            SentenceMerged+=Join(predList[g],CombinedArgList[g])
            SentenceMerged+=' && '
            g+=1
        SentenceMerged=SentenceMerged[:-4]
        SentenceMerged+=' => '
        SentenceMerged+=Join(predList[len(predList)-1],CombinedArgList[len(CombinedArgList)-1])
    print SentenceMerged,'Se'
    return SentenceMerged

def SUBST(Sentence,theta):
    index=Sentence.find('(')
    GoalPredicate=Sentence[0:index]
    arguments=Sentence[index:Sentence.find(')')+1]
    arglist=CreateArgList(arguments)
    i=0
    print arglist,theta,'abcdefghij'
    while(i<len(arglist)):
        if arglist[i] in theta:
            print arglist[i],'--------'
            arglist[i]=theta[arglist[i]]
            print arglist[i]
        i+=1
    print arglist
    SentenceMerged=Join(GoalPredicate,arglist)
    return SentenceMerged

def UNIFY(x,y,Theta):
    print x,'<----x'
    print y,'<----y'
    print'entered theta'
    print x,'xintheta'
    print y,'yintheta'
    if Theta is None:
        print 'entered nono'
        return None
    elif x==y:
        print 'hi'
        return Theta
    elif(type(x)!=list and isVariable(x)):
        print x,'x'
        return UNIFYVAR(x,y,Theta)
    elif(type(y)!=list and isVariable(y)):
        print x,'x'
        print y,'y'
        return UNIFYVAR(y,x,Theta)
    elif (type(x)==list):
        x1=x[0]
        print x1,'x1'
        x.pop(0)
        y1=y[0]
        y.pop(0)
        return UNIFY(x,y,UNIFY(x1,y1,Theta))
    elif (x.find('(')!=-1 and y.find('(')!=-1):
        goal=x[:x.find('(')]
        xarg=CreateArgList(x)
        pred=y[:y.find('(')]
        yarg=CreateArgList(y)
        return UNIFY(xarg,yarg,Theta)
    else:
        print 'entered here hhhhhhhhhhhhhhhhhhhh'
        return None
def UNIFYVAR(var,x,Theta):
    print x,'hereeeee'
    if var in Theta:
        print var,'var in theta'
        print Theta[var]
        return UNIFY(Theta[var],x,Theta)
    elif x in Theta:
        print x
        return UNIFY(var,Theta[x],Theta)
    else :
        print Theta
        print var,x
        Thetacopy=Theta.copy()
        Thetacopy[var]=x
        print Thetacopy
        return Thetacopy

def FOLBCASK(KB,Goal):
    #output_file.write('Ask: '+GoalQuery+'\n')
    Theta={}
    print 'in ask'
    return FOLBCOR(KB,Goal,Theta)

def FOLBCOR(KB,Goal,Theta):
    i=0
    #print 'in or '
    print Goal,'sss'
    GoalPred=Goal[:Goal.find('(')]
    for rule in KB:
        if(rule.find('=>')!=-1):
          rhs=rule[rule.find('=>')+3:]
        else:
          rhs=rule
        rhspred=rhs[:rhs.find('(')]
        if GoalPred==rhspred :
            stdrule=RBRSTD(rule)
            if(stdrule.find('=>')!=-1):
                lhs=stdrule[:stdrule.find('=>')]
                rhs=stdrule[stdrule.find('=>')+3:]
            else:
                lhs='khatam'
                rhs=stdrule
            for theta1 in FOLBCAND(KB,lhs,UNIFY(rhs,Goal,Theta)):
                yield theta1


def FOLBCAND(KB,GoalList,Theta):
    print Theta
    print 'entered and'
    if Theta is None:
       pass
    elif GoalList=='khatam' :
        print 'I ENTERED HERE FINALLY'
        yield Theta
    else:
        if GoalList.find('&&')!=-1:
          first=GoalList[:GoalList.find('&&')]
          rest=GoalList[GoalList.find('&&')+3:]
        else:
          first=GoalList
          rest='khatam'
        print first,rest,'SABZIIIIIIIII'
        for theta1 in FOLBCOR(KB,SUBST(first,Theta),Theta):
                for theta2 in FOLBCAND(KB,rest,theta1):
                    yield theta2

def main():
    global noc
    global output_file
    global GoalQueryList
    #input_file = open(sys.argv[2], 'r')
    input_file=open('sample03.txt','r')
    output_file=open('sample01output.txt','w')
    query=input_file.readline()
    noc=input_file.readline()
    print query
    print noc
    ClauseList=[]
    for line in input_file:
        clause=line.rstrip('\n')
        ClauseList.append(clause)
    print ClauseList
    GoalQueryList=[]
    if (query.find('&&') == -1):
        print query
        index=query.find(')')
        firstgoal=query[0:index+1]
        GoalQueryList.append(firstgoal)
    elif (query.find('&&') != -1):
        count=query.count('&&')
        nop=count+1
        index=query.find(')')
        GoalQueryList.append(query[0:index+1])
        rest=query[index+1:]
        i=1
        while(i<nop):
            temp1=rest.find('&&')
            temp2=rest.find(')')
            GoalQueryList.append(rest[temp1+3:temp2+1])
            rest=rest[temp2+1:]
            i+=1
    print GoalQueryList,'this'
    for i in FOLBCASK(ClauseList,GoalQueryList[0]):
           print i,'this'
           break
if __name__ == '__main__':
    main()