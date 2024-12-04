import urllib.request, time, os
import multiprocessing
def imageFinder(file,limit=200,starting_index=0):
    st = time.time()
    images = []
    c = starting_index
    start = 0
    while True:
        start = file.find('<img',start+1)

        if start == -1:
            break

        end = start+1
        while True:
            if file[end] == '>':
                break
            else:
                end += 1

        new_file = file[start:end]
        if not 'https://' in new_file:
            continue
        new_file = new_file.split('src="')[-1].split(' ')[0]
        #new_file = new_file.replace('"','').replace(">",'')
        if new_file in images:
            continue
        images.append(new_file)
        c += 1
        if c >= limit+starting_index:
            break
    print('time spent:',time.time()-st)
    return images

def saveimg(images,pathname):
    c = 0
    processes = []
    if not os.path.exists(pathname):
        os.makedirs(pathname)
    for img in images:
        c+=1
        newPath = pathname+'/'+pathname+' '+str(c)+'.jpg'

        p = multiprocessing.Process(target=urllib.request.urlretrieve,args=(img,newPath))
        p.start()
        processes.append(p)

        print(str(c)+'th process is started')

    for p in processes:
        p.join()
        print('one process is done')
    print('all process is done')

if __name__ == '__main__':
    with open('body.txt', 'r',encoding='utf-8') as file:
        file = file.read()

    saveimg(imageFinder(file,limit=400,starting_index=1),'cats')
