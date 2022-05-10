import time
sentences = ["Python is cool", "python is good", "python is not python snake"]

def search_query(query):
    # Creating an empty list to store results
    search_result = []
    
    # Iterating over a list
    for sentence in sentences:

        # Checking if the sentence contains a query
        if query in sentence.lower():

            # If so, counting occurrences of query word in the sentence
            cnt = sentence.lower().count(query)

            # Appending to search_result
            search_result.append([sentence, cnt])

    # Sorting search_result according to maximum counts of words
    search_result.sort(key=lambda count: count[1], reverse=True)


    # Getting a current time of result

    result_time = time.time()

    # Printing result
    if len(search_result) > 0:

        # Printing how many results found and in how much time
        print(f"{len(search_result)} results found({result_time-query_time} seconds):")

        # Printing result sentences
        for result in search_result:
            print(result[0])
    else:
        print("No result found")



if __name__ == '__main__':

    # Getting user query
    query = input("Please input your query string: ")

    # Getting a current time of the query
    query_time = time.time()
    
    # Converting user input to lower case
    query = query.lower()
    search_query(query)


'''
import time
s1="computer science is awesome"
s2="you get to learn about programming and many more other cool stuff in computer science"
s3="computer science is a subject"
s4="i love python"
s5="cse stands for computer science engineering"
s6="python programming is awesome, python is used for various development tasks"
s7="hello and bye-bye"
sentences=[s1,s2,s3,s4,s5,s6,s7]
c=list()
relevance=0
b=list()
j=1

if __name__ == "__main__":
    text=input('Enter your query string: ')
    result=0

    for i in sentences:
        c=i.split()
        for t in c:
            if t.lower() == text.lower():
                if relevance >=2:
                    b.insert(0, i)
                    break
                else:
                    time.sleep(0.1)
                    b.insert(j, i)
                    j+=1

                result+=1
                relevance+=1

            else:
                time.sleep(0.01)
    b.pop(len(b) - 1)
    print(f'{result} results found: ')
    print(b)
'''
