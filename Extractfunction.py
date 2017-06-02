import os
import sys
import subprocess
def CtagsParser(argv):
	with open('tags') as f:
		regf = open("regs.txt",'w')
		String=''
		for line in f:
			String += line.split()[3] +" " + line.split()[2]+" "+line.split()[0]+"\n"
		regf.write(String)
		regf.close()

def ParsingFunction(argv):
	DiffString = ["diff","--changed-group-format='%>'","--unchanged-group-format=''"]
	String = ''
	directories =  os.walk(sys.argv[1])
	split = argv[2].split('/')[0]
	for (path,dir,files) in directories:
		for filename in files:
			Path1 = path
			Path1 = split +'/'+ '/'.join(Path1.split('/')[1:]) +'/'+filename
			Path2 = os.path.join(path,filename)

			if (filename.split(".")[-1] != "cpp" or os.path.exists(Path1) != True ):
				continue
			DiffString.append(Path1)
			DiffString.append(Path2)
			DiffString.append("--new-line-format="+Path2+"' %dn %L'")
			Pipe = subprocess.Popen(DiffString,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
			DiffString = DiffString[:-3]
			String += Pipe.stdout.read().replace('\'','')

	String = String.split('\n')
	f = open('regs.txt')
	diff = float('inf')
	answer = []
	FunctionData = f.read().split('\n')
	for i in range(100):
		FileName2 = String[i].split()[0]
		DiffLine  = String[i].split()[1]
		for j in range(len(FunctionData)-1):
			FileName1 = FunctionData[j].split()[0]
			FunctionName = FunctionData[j].split()[2]
			FunctionLine = FunctionData[j].split()[1]
			if (FileName1 == FileName2):
				temp = int(DiffLine) - int(FunctionLine)
				if(temp > 0 and temp < diff):
					diff = temp
					answer.append(FunctionName+"\n")
		diff = float('inf')
	answer = list(set(answer))
	AnswerFile = open("answer.txt","w")
	AnswerFile.write(''.join(answer))
	AnswerFile.close()
	f.close()

def main(argv):
	CtagsParser(argv)
	ParsingFunction(argv)

if __name__ == "__main__":
	main(sys.argv)
