# A simple yet scalable (distributed) web crawler.

## Requirements
### Install RabbitMQ
for Mac run the following on terminal
`brew install rabbitmq`

### Install Redis

### Install the python packages
Navigate to the `requirements.txt` file and run
`pip install -r requirements.txt`

## How to run the cralwler 
###### Wirte the starting urls that you want to start with in seeds.txt file.
###### Run `RabbitMQ` and `Redis`
###### Run  `main.py` file. This will push the seeds to the Downloadable queue.
###### Run  `worker.py`
###### Run  `publisher.py`
###### Run  `local_publisher.py`


### To check if if everything is working go to `/simple_crawler/workers/content/` . Downloaded html files should be written here.

<img src="https://github.com/sajid1189/simple_crawler/blob/develop/structure.png">

## Arcitecture

The distrubuted model consists of a central schedular and n-number of distrubuted workers. The algorithm treats the web as a graph of pages (each referred uniquley by its url) and applies BFS (breadth first search) to traverse the entire graph. As shown in the second figure let us assume that our hypothetical web consists of 8 pages. Page1 one has links to page2, page3, page4. Once we download page1 we push the urls of page1, page2 and page3 into the queue. But before pushing them he schedular makes a lookup in the Redis DB if they are already marked. If they are not marked then only they are pushed to the queue. Let us assume that we have just started crawling and nothing has been downloaded yet. Hence the Redis DB is empty. The schedular will later pop each of them one by one (in the same order they were pushed into the queue -FIFO) and will deliver them to the workers (via another queue which the workers are listneing to) to download. The central schedular will also mark these urls (pag1, pag2, page3, page4) as 'taken care of'. This marking is done on the Redis. Let us assume that the a worker received url of page2. It downloads the page, stores it, parses the page finds outlinks page3, page5 and page6. The worker publishes these links to the queue which the central schedular is listening to. Note that later on when the scheduler gets page3 it does not push the url as it had already published page3 earlier and marked this on Redis DB. 


### Message:
A message is always list of urls (in JSON format).

### Queue:
A queue is always a RabbitMQ queue.

### The schedular:
It is a Python process. Keeps listening to OUTLINKS_QUEUE. Whenever there is a new messages on the queue (usually there could be a pool of messages on the queue already waiting to be consumed by the schedular), the scedular pops it and loads the JSON list and declares an empty list (. Let us call it 'bundle'). It then iterates over the list. For each url in the list, the scedular does the following: checks if the url is already marked in the Redis DB. If not then it appends the url to the 'bundle'. And at the end of the loop, it publishes the JSON formatted 'bundle' on 'DOWNLOADABLE_QUEUE'. This is a very simplied explanation of what the central schedular does, althogh it peroforms a few more things to optimize the performance. Note that both the queues, the Redis DB and the central schedular should lie on the same machine and no worker process should be executed on the this machine.

### Workers: 
A worker is a Python process that downloads a web page, parses it, stores the content, lists the outlinks (urls) on the downloaded page and publishes the outlinks to the central OUTLINKS_QUEUE

# To be continued...........
