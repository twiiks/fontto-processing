# fontto-processing
> Message Queue for fontto with RabbitMQ

[INFO](http://redmine.twiiks.co/projects/processing-server/wiki#테스트용-publisher)

## How Work
1. pull from rabbitMQ (with multithread)
2. processing
    - pass deep neural network
    - noise reduction
    - svg conversion
    - ttf conversion
3. request to fontto-server 

## Usage
### **test-publisher**
#### help
```
node test-publisher/publisher.js --help
```
#### install dependency
```
cd test-publisher
npm install
```
#### run test publisher
```
node test-publisher/publisher.js --amqp-url amqp://<host>:5672 --queue <queue name> --interval 2000
```

### **python subscriber**
#### help
```
python index.py --help
```
#### install dependency
```
pip install -r requirements.txt
```
#### run subscriber
```
python index.py --amqp-url amqp://<host>:5672 --queue <queue> --log-path output.log --thread-num 2
```
