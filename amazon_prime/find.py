
def find_str(s, char):
	index = 0
	if char in s:
		c = char[0]
		for ch in s:
			if ch == c:
				if s[index:index+len(char)] == char:
					return index
			index += 1
	return -1

with open('hi.txt', 'r') as myfile:
	data = myfile.read()

i=0
count =0
l=[]
while (i<len(data)):
	j=find_str(data[i:], 'data-asin=')
	if (j!=-1):
		id=data[i+j+10:i+j+23]
		count = count +1
		l.append(id)
		print(id)
		print('\n')
		i=i+j+15
	if (j==-1):
		break

#print(l)
print(count)

count2=0

l_name=[]
i=0
j=find_str(data[i:], 'data-asin=')

unique = data[j+23:j+430]
print(unique)
while (i<len(data)):

	j=find_str(data[i:], 'data-asin=')
	#print(j)
	if (j!=-1 and unique==data[i+j+23:i+j+430] ):
		k=find_str(data[i+j:], 'img alt=\"')
		j=j+k+9
		z=j
		flag=1
		id=""
		while flag==1:
			if(data[i+j]=='\"' or data[i+j:i+j+3+6+1] == ' - Season ' or data[i+j:i+j+8] == ' Season ' ):
				flag=0
			else:
				if(data[i+j]=='-'):
					id=id+data[i+j]
				else:
					id = id + data[i+j]
				j=j+1
		count2 = count2 +1
		l_name.append(id)
		print(id)
		j=z
		flag=1
		id=""
		while flag==1:
			if(data[i+j]=='\"'):
				flag=0
			else:
				if(1):#data[i+j]=='-'):
					id=id+data[i+j]#' '
				else:
					id = id + data[i+j]
				j=j+1
		count2 = count2 +1
		l_name.append(id)
		print(id)
		#print('\n')
		#i=i+j
		#print(i)
	if (j==-1):
		break
	i=i+j+10	

print(count2)		

i=0

j=0
unique = data[2760578+11:2760578+7+370-5]
print(unique)
while (i<len(data)):

	j=find_str(data[i:], 'data-asin=')
	if (j!=-1 and unique==data[i+j+10+12:i+j+10+373] ):

		j=j+374+10
		z=j
		#print(data[i+j:i+j+10])
		flag=1
		id=""
		while flag==1:
			if(data[i+j]=='\"' or data[i+j+3:i+j+3+6] == 'Season' or data[i+j+3:i+j+3+6] == 'season' ):
				flag=0
			else:
				if(data[i+j]=='-'):
					id=id+' '
				else:
					id = id + data[i+j]
				j=j+1
		count2 = count2 +1
		l_name.append(id)
		print(id)
		j=z
		flag=1
		id=""
		while flag==1:
			if(data[i+j]=='\"'):
				flag=0
			else:
				if(1):#data[i+j]=='-'):
					id=id+data[i+j]#' '
				else:
					id = id + data[i+j]
				j=j+1
		count2 = count2 +1
		l_name.append(id)
		print(id)
		#print('\n')
		#i=i+j
		#print(i)
	if (j==-1):
		break
	i=i+j+10	

print(count2)

i=0

j=0
unique = data[2815941+22:2815941+394]
print(unique)
while (i<len(data)):

	j=find_str(data[i:], 'data-asin=')
	if (j!=-1 and unique==data[i+j+10+12:i+j+394] ):

		j=j+394
		z=j
		#print(data[i+j:i+j+10])
		flag=1
		id=""
		while flag==1:
			if(data[i+j]=='\"' or data[i+j:i+j+3+6+1] == ' - Season ' or data[i+j:i+j+8] == ' Season ' ):
				flag=0
			else:
				if(1):#data[i+j]=='-'):
					id=id+data[i+j]#' '
				else:
					id = id + data[i+j]
				j=j+1
		count2 = count2 +1
		print(id)
		l_name.append(id)
		flag=1
		id=""
		j=z
		while flag==1:
			if(data[i+j]=='\"'):
				flag=0
			else:
				if(1):#data[i+j]=='-'):
					id=id+data[i+j]#' '
				else:
					id = id + data[i+j]
				j=j+1
		count2 = count2 +1
		l_name.append(id)
		print(id)
		#print(id)
		#print('\n')
		#i=i+j
		#print(i)
	if (j==-1):
		break
	i=i+j+10	

print(count2)

#print(l_name)
